import bpy
class OBJECT_PT_Mfecane_tools(bpy.types.Panel):
   bl_label = "Mfecane toolset"
   bl_idname = "PT_TestPanel"
   bl_space_type = 'VIEW_3D'
   bl_region_type = 'UI'
   bl_category = 'Mfecane toolset'
   
   def draw(self, context):
       layout = self.layout
       
       row = layout.row()
       row.label(text = "Manipulation", icon = "CUBE")
       row = layout.row()
       row.operator("object.tweak_command")

class ObjectMode(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.object_mode"
    bl_label = "Object mode"
    
    def execute(self, context):

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.wm.tool_set_by_id(name='builtin.select')

        return {'FINISHED'}
class TweakCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.tweak_command"
    bl_label = "Tweak mode"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.wm.tool_set_by_id(name='builtin.select')

        return {'FINISHED'}

mfecane_keymaps = []

def disable_default_kmi(km=None, idname=None, retries=10):
    wm = bpy.context.window_manager

    if not (km and idname) or retries < 1:
        return # failed

    # the default keyconfig
    kc = wm.keyconfigs['blender']
    for kmi in kc.keymaps[km].keymap_items:
        print(kmi)
        if kmi.idname == idname:
            kmi.active = False
            print("Disabled", kmi.name)
            return

    print("Retrying..")
    # add some delay
    bpy.app.timers.register(
        lambda: disable_default_kmi(km, idname, retries - 1),
        first_interval=0.1)

def register():
    bpy.utils.register_class(OBJECT_PT_Mfecane_tools)
    bpy.utils.register_class(TweakCommand)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(TweakCommand.bl_idname, type='T', value='PRESS', ctrl=False)
        mfecane_keymaps.append((km, kmi))
    
def unregister():
    bpy.utils.unregister_class(OBJECT_PT_Mfecane_tools)
    bpy.utils.unregister_class(TweakCommand)
    
if __name__ == "__main__":
    register()
    
    bpy.ops.object.tweak_command()