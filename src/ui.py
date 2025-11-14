import bpy
from bpy.props import BoolProperty, PointerProperty, StringProperty


class BasicPanel(bpy.types.Panel):
    bl_label = "Basic Utils"
    bl_idname = "BU_PT_basic"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "Utils"
    bl_order = 0
    bl_ui_units_x = 0

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("bu.show_import", icon="FILE_SCRIPT")
        row = layout.row()
        row.operator("bu.update_view", icon="VIEW3D")
        row = layout.row()
        row.operator("bu.remove_unused_actions", icon="UNLINKED")
        row = layout.row()
        row.operator("bu.remove_empty", icon="EMPTY_DATA")
        row = layout.row()
        row.operator("bu.remove_all", icon="WARNING_LARGE")


class VisPanel(bpy.types.Panel):
    bl_label = "Vis Utils"
    bl_idname = "BU_PT_vis"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "Utils"
    bl_order = 1
    # bl_options = {"HIDE_HEADER"}
    bl_ui_units_x = 0

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("bu.toggle_lang", icon="FONT_DATA")
        row = layout.row()
        row.operator("bu.toggle_timeline_action", icon="TIME")

        layout.separator(type="LINE")

        row = layout.row()
        row.operator("bu.toggle_bone", icon="BONE_DATA")
        row = layout.row()
        row.operator("bu.toggle_weight", icon="WPAINT_HLT")
        row = layout.row()
        row.operator("bu.toggle_screenshot", icon="RESTRICT_RENDER_OFF")


class MeshPanel(bpy.types.Panel):
    bl_label = "Mesh Utils"
    bl_idname = "BU_PT_mesh"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "Utils"
    bl_order = 2
    # bl_options = {"HIDE_HEADER"}
    bl_ui_units_x = 0

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("bu.clear_all_vgroups", icon="VERTEXSEL")
        row = layout.row()
        row.operator("bu.transfer_vgroups", icon="MOD_DATA_TRANSFER")
        row = layout.row()
        row.operator("bu.clear_all_shapekeys", icon="SHAPEKEY_DATA")
        row = layout.row()
        row.operator("bu.transfer_shapekeys", icon="AUTOMERGE_ON")


class PosePanel(bpy.types.Panel):
    bl_label = "Pose Utils"
    bl_idname = "BU_PT_pose"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ""
    bl_category = "Utils"
    bl_order = 3
    # bl_options = {"HIDE_HEADER"}
    bl_ui_units_x = 0

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        row = layout.row()
        row.operator("bu.toggle_rest", icon="ARMATURE_DATA")
        row = layout.row()
        row.operator("bu.reset_pose", icon="OUTLINER_OB_ARMATURE")
        row = layout.row()
        row.operator("bu.copy_pose", icon="PASTEDOWN")
        row = layout.row()
        row.operator("bu.reset_rest", icon="MOD_ARMATURE")

        layout.separator(type="LINE")

        layout.label(text="Batch Rename Bones")
        row = layout.row()
        row.prop(wm, "bu_rename_text_block", text="")
        row = layout.row()
        row.operator("bu.load_bones_to_text", icon="FILE_TEXT")
        row = layout.row()
        row.operator("bu.rename_bones_from_text", icon="BONE_DATA")

        layout.separator(type="LINE")

        layout.label(text="Retarget Shortcut")
        row = layout.row()
        row.prop(wm, "bu_retarget_src", text="Source", icon="ARMATURE_DATA")
        row = layout.row()
        row.prop(wm, "bu_retarget_tgt", text="Target", icon="ARMATURE_DATA")
        row = layout.row()
        row.prop(wm, "bu_retarget_root", text="Root", icon="OBJECT_ORIGIN")
        row = layout.row()
        row.prop(wm, "bu_retarget_inplace", text="In-Place Retarget")
        row = layout.row()
        row.operator("bu.retarget", icon="PLAY")


def register():
    bpy.utils.register_class(BasicPanel)
    bpy.utils.register_class(VisPanel)
    bpy.utils.register_class(MeshPanel)
    bpy.utils.register_class(PosePanel)
    bpy.types.WindowManager.bu_rename_text_block = PointerProperty(
        type=bpy.types.Text,
        name="Bone Names Text",
        description="Text block to use for batch renaming bones",
    )
    bpy.types.WindowManager.bu_retarget_src = PointerProperty(
        type=bpy.types.Object,
        name="Source Armature",
        description="Armature with desired animation",
        poll=lambda self, obj: obj is not None and obj.type == "ARMATURE",
    )
    bpy.types.WindowManager.bu_retarget_tgt = PointerProperty(
        type=bpy.types.Object,
        name="Target Armature",
        description="Armature to be animated",
        poll=lambda self, obj: obj is not None and obj.type == "ARMATURE",
    )
    bpy.types.WindowManager.bu_retarget_root = StringProperty(
        name="Root Name",
        description="Name of root bone of the target armature",
        default="mixamorig:Hips",
    )
    bpy.types.WindowManager.bu_retarget_inplace = BoolProperty(
        name="In-place Retarget",
        description="Retarget animation in-place",
        default=True,
    )


def unregister():
    bpy.utils.unregister_class(BasicPanel)
    bpy.utils.unregister_class(VisPanel)
    bpy.utils.unregister_class(MeshPanel)
    bpy.utils.unregister_class(PosePanel)
    del bpy.types.WindowManager.bu_rename_text_block
    del bpy.types.WindowManager.bu_retarget_src
    del bpy.types.WindowManager.bu_retarget_tgt
    del bpy.types.WindowManager.bu_retarget_root
    del bpy.types.WindowManager.bu_retarget_inplace
