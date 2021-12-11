import bpy
from bl_ui.space_toolsystem_common import ToolSelectPanelHelper

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        # Set the cursor tool
        bpy.ops.wm.tool_set_by_id(name = "builtin.select")
        # Get the tool
        tool = ToolSelectPanelHelper.tool_active_from_context(context)
        props = tool.operator_properties('view3d.select')

        # Print all properties
        print (dir(props))
        # [...'mode', 'radius', 'rna_type', 'wait_for_input', 'x', 'y']
        
        # Set the properties
        props.mode = 'SUB'
        props.radius = 50
        
        return {'FINISHED'}


addon_keymaps = []

def register():
    bpy.utils.register_class(SimpleOperator)

    # Add a shortcut
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            SimpleOperator.bl_idname, type='C', value='PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(SimpleOperator)

    # Remove the shortcut
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()