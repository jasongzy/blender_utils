bl_info = {
    "name": "Blender Utils",
    "author": "jasongzy",
    "version": (1, 2, 0),
    "blender": (4, 2, 0),
    "location": "",
    "description": "Useful helpers",
    "warning": "",
    "doc_url": "https://github.com/jasongzy/blender_utils",
    "tracker_url": "",
    "category": "Development",
}

from .src import bu, ops, prefs, ui


def register():
    prefs.register()
    ops.register()
    ui.register()


def unregister():
    prefs.unregister()
    ops.unregister()
    ui.unregister()


if __name__ == "__main__":
    register()
