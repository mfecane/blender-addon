import bpy

### SNIPPETS ###

# tools = bpy.context.workspace.tools
# active_tool = tools.from_space_view3d_mode(bpy.context.mode).idname
# active_tool = bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname

# area = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]
# override_context = bpy.context.copy()
# override_context['window'] = bpy.context.window
# override_context['screen'] = bpy.context.screen
# override_context['area'] = area
# override_context['region'] = area.regions[-1]
# override_context['scene'] = bpy.context.scene
# override_context['space_data'] = area.spaces.active

class TestPanel(bpy.types.Panel):
   bl_label = "Test Panel"
   bl_idname = "PT_TestPanel"
   bl_space_type = 'VIEW_3D'
   bl_region_type = 'UI'
   bl_category = 'My 1st Addon'
   
   def draw(self, context):
       layout = self.layout
       
       row = layout.row()
       row.label(text = "Sample Text", icon = "CUBE")
       row = layout.row()
       row.operator("object.tweak_command")
        
class TweakCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.tweak_command"
    bl_label = "Tweak mode"
    
#    @classmethod
#    def poll(cls, context):
#        return context.active_object is not None
    
    def execute(self, context):
        # area = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]
        # override_context = bpy.context.copy()
        # override_context['window'] = bpy.context.window
        # override_context['screen'] = bpy.context.screen
        # override_context['area'] = area
        # override_context['region'] = area.regions[-1]
        # override_context['scene'] = bpy.context.scene
        # override_context['space_data'] = area.spaces.active

        bpy.ops.wm.tool_set_by_id(name='builtin.select')
        # list(override_context.workspace.tools)

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.wm.tool_set_by_id(name='builtin.select')
        # list(bpy.context.workspace.tools)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(TestPanel)
    bpy.utils.register_class(TweakCommand)
    
def unregister():
    bpy.utils.unregister_class(TestPanel)
    bpy.utils.unregister_class(TweakCommand)
    
if __name__ == "__main__":
    register()
    
    bpy.ops.object.tweak_command()

# info
# hotkey file C:\Users\Mfecane\AppData\Roaming\Blender Foundation\Blender\2.92\scripts\presets\keyconfig