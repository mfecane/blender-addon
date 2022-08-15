import bpy


class CopyArmature(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.copy_armature"
    bl_label = "Copy Armature"

    def execute(self, context):
        print('CopyArmature')
        return {'FINISHED'}