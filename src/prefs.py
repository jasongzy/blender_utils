import os
import subprocess
import sys
from enum import Enum
from importlib.util import find_spec

import bpy


class CudaResult(Enum):
    SUCCESS = 1
    NOT_FOUND = 2


class CudaDetect:
    """Checks Cuda version installed in the system"""

    def __init__(self):
        self.result = None
        self.major = 0
        self.minor = 0
        self.micro = 0
        self.has_cuda_hardware = False

        self.has_cuda_device()
        self.detect_cuda_ver()

    @staticmethod
    def get_cuda_path():
        try:
            return os.environ["CPATH"]
        except KeyError:
            pass

        where_cmd = "where" if sys.platform.startswith("win") else "whereis"
        result = subprocess.check_output([where_cmd, "nvcc"]).decode("UTF-8")

        if "\n" in result:
            nvcc_path = result.split("\n", 1)[0]
        else:
            nvcc_path = result.split("\t", 1)[0]

        nvcc_dir, _ = os.path.split(nvcc_path)
        cuda_dir = os.path.dirname(nvcc_dir)

        return cuda_dir

    def has_cuda_device(self):
        """Checks for cuda hardware in cycles preferences"""
        prefs = bpy.context.preferences
        cprefs = prefs.addons["cycles"].preferences

        if bpy.app.version[0] > 2:
            # devices are iterated differently in blender 3.0/blender 2.9
            cprefs.refresh_devices()

            def get_dev():
                for dev in cprefs.devices:
                    yield dev

        else:

            def get_dev():
                for dev in cprefs.get_devices(bpy.context):
                    for dev_entry in dev:
                        yield dev_entry

        for device in get_dev():
            if device.type == "CUDA":
                self.has_cuda_hardware = True
                return

    def detect_cuda_ver(self):
        """Try execute the cuda compiler with the --version flag"""
        try:
            nvcc_out = subprocess.check_output(["nvcc", "--version"])
        except FileNotFoundError:
            self.result = CudaResult.NOT_FOUND
            return

        nvcc_out = str(nvcc_out)
        ver = nvcc_out.rsplit(" V", 1)[-1]
        ver = ver.strip("'\\r\\n")
        ver_ends = next((i for i, c in enumerate(ver) if not (c.isdigit() or c == ".")), len(ver))
        ver = ver[:ver_ends]

        self.major, self.minor, self.micro = ver.split(".", 2)
        self.result = CudaResult.SUCCESS


class BUPrefs(bpy.types.AddonPreferences):
    bl_idname = __package__.split(".")[0]

    _cuda_info: CudaDetect = None
    _added_paths = []
    missing_modules = []

    @staticmethod
    def check_cuda():
        BUPrefs._cuda_info = CudaDetect()

    @staticmethod
    def add_module_paths():
        BUPrefs.reset_module_paths()
        env_path = bpy.context.preferences.addons[__package__.split(".")[0]].preferences.modules_path

        if not os.path.isdir(env_path):
            return False

        if sys.platform.startswith("linux"):
            lib_path = os.path.join(env_path, "lib")
            py_subdir = [
                p for p in os.listdir(lib_path) if os.isdir(os.path.join(lib_path, p)) and p.startswith("python3.")
            ]
            if py_subdir:
                py_subdir = sorted(py_subdir)[-1]
            sitepackages = os.path.join(lib_path, py_subdir, "site-packages")
        else:
            lib_path = os.path.join(env_path, "Lib")
            sitepackages = os.path.join(lib_path, "site-packages")

        if not os.path.isdir(sitepackages):
            # not a python path, but the user might be still typing
            return False

        platformpath = os.path.join(sitepackages, sys.platform)
        platformlibs = os.path.join(platformpath, "lib")

        mod_paths = [lib_path, sitepackages, platformpath, platformlibs]
        if sys.platform.startswith("win"):
            mod_paths.append(os.path.join(env_path, "DLLs"))
            mod_paths.append(os.path.join(sitepackages, "Pythonwin"))

        for mod_path in mod_paths:
            if not os.path.isdir(mod_path):
                # print(f"{mod_path} not a directory, skipping")
                continue
            if mod_path not in sys.path:
                print(f"Adding to path: {mod_path}")
                sys.path.append(mod_path)
                BUPrefs._added_paths.append(mod_path)

        BUPrefs.check_modules()
        return True

    @staticmethod
    def reset_module_paths():
        # FIXME: even if we do this, additional modules are still available
        for mod_path in BUPrefs._added_paths:
            print(f"Removing module path: {mod_path}")
            sys.path.remove(mod_path)
        BUPrefs._added_paths.clear()

    def update_modules(self, context):
        self.add_module_paths()

    modules_path: bpy.props.StringProperty(
        name="Environment path",
        description="Path to additional modules (e.g., torch), typically a directory containing 'lib/site-packages'",
        subtype="DIR_PATH",
        update=update_modules,
        default=os.path.join(os.path.expanduser("~"), "anaconda3", "envs", "blender"),
    )  # type: ignore

    modules_found: bpy.props.BoolProperty(
        name="Required Modules", description="Whether required modules have been found or not"
    )  # type: ignore

    @staticmethod
    def check_modules():
        BUPrefs.missing_modules.clear()
        required_modules = []
        for mod_name in required_modules:
            if not find_spec(mod_name):
                BUPrefs.missing_modules.append(mod_name)

        preferences = bpy.context.preferences.addons[__package__.split(".")[0]].preferences
        preferences.modules_found = len(BUPrefs.missing_modules) == 0

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        info = BUPrefs._cuda_info
        if info:
            py_ver = sys.version_info
            row = column.row()
            row.label(text=f"Python Version: {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
            if info.result == CudaResult.SUCCESS:
                row = column.row()
                row.label(text=f"CUDA Version: {info.major}.{info.minor}.{info.micro}")
            elif info.result == CudaResult.NOT_FOUND:
                row = column.row()
                row.label(text="CUDA Toolkit not found", icon="ERROR")

                if info.has_cuda_hardware:
                    row = column.row()
                    split = row.split(factor=0.1, align=False)
                    split.column()
                    col = split.column()
                    col.label(text="CUDA hardware is present. Please make sure that CUDA Toolkit is installed.")
                    op = col.operator("wm.url_open", text="nVidia Downloads", icon="URL")
                    op.url = "https://developer.nvidia.com/downloads"

        if self.missing_modules:
            row = column.row()
            row.label(text=f"Modules not found: {','.join(self.missing_modules)}", icon="ERROR")

        box = column.box()
        col = box.column()

        row = col.row()
        split = row.split(factor=0.8, align=False)
        sp_col = split.column()
        sp_col.prop(self, "modules_path", text="Modules Path")


def register():
    bpy.utils.register_class(BUPrefs)
    BUPrefs.check_cuda()
    if not BUPrefs.add_module_paths():
        print("Modules path not found, please set in addon preferences")
    BUPrefs.check_modules()


def unregister():
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        pass

    BUPrefs.reset_module_paths()
    bpy.utils.unregister_class(BUPrefs)
