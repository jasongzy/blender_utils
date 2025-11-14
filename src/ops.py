import bpy

from .bu import (
    Mode,
    get_all_armature_obj,
    remove_all,
    remove_collection,
    remove_empty,
    remove_unused_actions,
    set_rest_bones,
    update,
)


class BUShowImport(bpy.types.Operator):
    """Show code for importing the helper module `bu` in console/script"""

    bl_idname = "bu.show_import"
    bl_label = "Show Importing Code"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        cmd = f"from {__package__.split('.')[0]} import bu"
        self.report({"INFO"}, cmd)
        return {"FINISHED"}


class BUUpdateView(bpy.types.Operator):
    """Update view"""

    bl_idname = "bu.update_view"
    bl_label = "Update View"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        update(context)
        self.report({"INFO"}, "Updated successfully")
        return {"FINISHED"}


class BURemoveUnusedActions(bpy.types.Operator):
    """Remove unused actions"""

    bl_idname = "bu.remove_unused_actions"
    bl_label = "Remove Unused Actions"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        remove_unused_actions()
        self.report({"INFO"}, "Removed unused actions")
        return {"FINISHED"}


class BURemoveEmpty(bpy.types.Operator):
    """Remove all empty objects"""

    bl_idname = "bu.remove_empty"
    bl_label = "Remove Empty Objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        remove_empty()
        remove_collection("glTF_not_exported")
        self.report({"INFO"}, "Removed empty objects")
        return {"FINISHED"}


class BURemoveAll(bpy.types.Operator):
    """Remove all objects"""

    bl_idname = "bu.remove_all"
    bl_label = "Remove Everything"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        remove_all()
        self.report({"INFO"}, "Removed all objects")
        return {"FINISHED"}


class BUToggleLang(bpy.types.Operator):
    """Toggle between `Chinese` and `English` language"""

    bl_idname = "bu.toggle_lang"
    bl_label = "Toggle Chinese/English"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.preferences.view.language in ("zh_HANS", "en_US")

    def execute(self, context):
        if context.preferences.view.language == "zh_HANS":
            context.preferences.view.language = "en_US"
        elif context.preferences.view.language == "en_US":
            context.preferences.view.language = "zh_HANS"
        return {"FINISHED"}


class BUToggleTimelineAction(bpy.types.Operator):
    """Toggle between `Timeline` and `Action Editor`"""

    bl_idname = "bu.toggle_timeline_action"
    bl_label = "Toggle Timeline/Action Editor"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return any(area.ui_type in ("TIMELINE", "DOPESHEET") for area in context.screen.areas)

    def execute(self, context):
        for area in context.screen.areas:
            if area.ui_type == "TIMELINE":
                area.ui_type = "DOPESHEET"
                area.spaces[0].ui_mode = "ACTION"
                break
            elif area.ui_type == "DOPESHEET":
                area.ui_type = "TIMELINE"
                break
        return {"FINISHED"}


class BUToggleBoneMode(bpy.types.Operator):
    """Toggle `Pose` mode (select the target Armature first)"""

    bl_idname = "bu.toggle_bone"
    bl_label = "Toggle Bone Mode"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return (
            context.object is not None
            and context.object.type == "ARMATURE"
            and context.area.ui_type == "VIEW_3D"
            and context.mode in ("OBJECT", "POSE")
        )

    def execute(self, context):
        bpy.ops.object.posemode_toggle()
        if context.mode == "OBJECT":
            context.space_data.shading.show_xray = False
        elif context.mode == "POSE":
            context.space_data.shading.show_xray = True
        return {"FINISHED"}


class BUToggleWeightMode(bpy.types.Operator):
    """Toggle `Weight Paint` mode (select the target Mesh first)"""

    bl_idname = "bu.toggle_weight"
    bl_label = "Toggle Weight Mode"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return (
            context.object is not None
            and context.object.type == "MESH"
            and context.area.ui_type == "VIEW_3D"
            and context.mode in ("OBJECT", "PAINT_WEIGHT")
        )

    def execute(self, context):
        bpy.ops.paint.weight_paint_toggle()
        context.scene.tool_settings.vertex_group_user = "ACTIVE"
        return {"FINISHED"}


class BUToggleScreenshotMode(bpy.types.Operator):
    """Toggle screenshot mode (change `Viewpoint Shading` to `Solid` mode first)"""

    bl_idname = "bu.toggle_screenshot"
    bl_label = "Toggle Screenshot Mode"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.area.ui_type == "VIEW_3D" and context.space_data.shading.type == "SOLID"

    def execute(self, context):
        if context.space_data.overlay.show_floor:
            context.space_data.overlay.show_floor = False
            context.space_data.overlay.show_cursor = False
            context.space_data.overlay.show_axis_x = False
            context.space_data.overlay.show_axis_y = False
            context.space_data.overlay.show_axis_z = False
            context.space_data.overlay.show_object_origins = False
            context.space_data.shading.color_type = "TEXTURE"
            context.space_data.shading.light = "MATCAP"
            context.space_data.shading.background_type = "VIEWPORT"
            context.space_data.shading.background_color = (1, 1, 1)
            context.space_data.show_object_viewport_light = False
            context.space_data.show_object_viewport_camera = False
        else:
            context.space_data.overlay.show_floor = True
            context.space_data.overlay.show_cursor = True
            context.space_data.overlay.show_axis_x = True
            context.space_data.overlay.show_axis_y = True
            context.space_data.overlay.show_object_origins = True
            context.space_data.shading.color_type = "MATERIAL"
            context.space_data.shading.light = "STUDIO"
            context.space_data.shading.background_type = "THEME"
            context.space_data.shading.background_color = (0.05, 0.05, 0.05)
            context.space_data.show_object_viewport_light = True
            context.space_data.show_object_viewport_camera = True
        return {"FINISHED"}


class BUToggleRest(bpy.types.Operator):
    """Toggle rest/pose position (select the target Armature first)"""

    bl_idname = "bu.toggle_rest"
    bl_label = "Toggle Rest Pose"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == "ARMATURE" and context.area.ui_type == "VIEW_3D"

    def execute(self, context):
        if context.object.data.pose_position == "POSE":
            context.object.data.pose_position = "REST"
        elif context.object.data.pose_position == "REST":
            context.object.data.pose_position = "POSE"
        return {"FINISHED"}


class BUResetPose(bpy.types.Operator):
    """Reset pose to rest position (select the target Armature first)"""

    bl_idname = "bu.reset_pose"
    bl_label = "Reset Pose to Rest"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == "ARMATURE" and context.area.ui_type == "VIEW_3D"

    def execute(self, context):
        with Mode("POSE", context.object):
            for b in context.object.data.bones:
                b.select = True
            bpy.ops.pose.transforms_clear()
        return {"FINISHED"}


class BUCopyPose(bpy.types.Operator):
    """Copy pose from one Armature to another"""

    bl_idname = "bu.copy_pose"
    bl_label = "Copy and Paste Pose"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (
            context.object is not None
            and context.object.type == "ARMATURE"
            and context.area.ui_type == "VIEW_3D"
            and len(get_all_armature_obj(context.selected_objects)) == 2
        )

    def execute(self, context):
        target_armature = context.object
        selected_armatures = [
            obj for obj in context.selected_objects if obj.type == "ARMATURE" and obj != target_armature
        ]
        assert len(selected_armatures) == 1, "Please select exactly two Armatures"
        source_armature = selected_armatures[0]

        with Mode("POSE", source_armature):
            for b in source_armature.data.bones:
                b.select = True
            bpy.ops.pose.copy()
        with Mode("POSE", target_armature):
            for b in target_armature.data.bones:
                b.select = True
            bpy.ops.pose.paste(flipped=False)
        return {"FINISHED"}


class BUResetRest(bpy.types.Operator):
    """Apply current pose as rest pose (select the target Armature first)"""

    bl_idname = "bu.reset_rest"
    bl_label = "Set Current Pose as Rest"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == "ARMATURE"

    def execute(self, context):
        set_rest_bones(context.object, reset_as_rest=True)
        self.report({"INFO"}, "Rest pose is reset")
        return {"FINISHED"}


class BURetarget(bpy.types.Operator):
    """Retarget selected armature (Auto-Rig Pro must be installed)"""

    bl_idname = "bu.retarget"
    bl_label = "Retarget"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        wm = context.window_manager
        return "arp_active_tab" in dir(context.scene) and None not in (wm.bu_retarget_src, wm.bu_retarget_tgt)

    def execute(self, context):
        wm = context.window_manager
        scn = context.scene
        scn.source_rig = wm.bu_retarget_src.name
        scn.arp_retarget_in_place = wm.bu_retarget_inplace
        scn.target_rig = wm.bu_retarget_tgt.name
        bpy.ops.arp.auto_scale()
        bpy.ops.arp.build_bones_list()
        root = scn.bones_map_v2[wm.bu_retarget_root]
        scn.bones_map_index = list(scn.bones_map_v2).index(root)
        root.set_as_root = True
        return bpy.ops.arp.retarget("INVOKE_DEFAULT")


def register():
    bpy.utils.register_class(BUShowImport)
    bpy.utils.register_class(BUUpdateView)
    bpy.utils.register_class(BURemoveAll)
    bpy.utils.register_class(BURemoveEmpty)
    bpy.utils.register_class(BURemoveUnusedActions)
    bpy.utils.register_class(BUToggleLang)
    bpy.utils.register_class(BUToggleTimelineAction)
    bpy.utils.register_class(BUToggleBoneMode)
    bpy.utils.register_class(BUToggleWeightMode)
    bpy.utils.register_class(BUToggleScreenshotMode)
    bpy.utils.register_class(BUToggleRest)
    bpy.utils.register_class(BUResetPose)
    bpy.utils.register_class(BUCopyPose)
    bpy.utils.register_class(BUResetRest)
    bpy.utils.register_class(BURetarget)


def unregister():
    bpy.utils.unregister_class(BUShowImport)
    bpy.utils.unregister_class(BUUpdateView)
    bpy.utils.unregister_class(BURemoveAll)
    bpy.utils.unregister_class(BURemoveEmpty)
    bpy.utils.unregister_class(BURemoveUnusedActions)
    bpy.utils.unregister_class(BUToggleLang)
    bpy.utils.unregister_class(BUToggleTimelineAction)
    bpy.utils.unregister_class(BUToggleBoneMode)
    bpy.utils.unregister_class(BUToggleWeightMode)
    bpy.utils.unregister_class(BUToggleScreenshotMode)
    bpy.utils.unregister_class(BUToggleRest)
    bpy.utils.unregister_class(BUResetPose)
    bpy.utils.unregister_class(BUCopyPose)
    bpy.utils.unregister_class(BUResetRest)
    bpy.utils.unregister_class(BURetarget)
