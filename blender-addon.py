import bpy

class ObjectSelect(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.object_select"
    bl_label = "Object select"
    
    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.wm.tool_set_by_id(name='builtin.select_box')

        return {'FINISHED'}
        
class VertexSelect(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.vertex_select"
    bl_label = "Vertex select"
    
    def execute(self, context):

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.wm.tool_set_by_id(name='builtin.select_box')

        return {'FINISHED'}

class EdgeSelect(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.edge_select"
    bl_label = "Edge select"
    
    def execute(self, context):

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_mode(type="EDGE")
        bpy.ops.wm.tool_set_by_id(name='builtin.select_box')

        return {'FINISHED'}
        
class FaceSelect(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.face_select"
    bl_label = "Face select"
    
    def execute(self, context):

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.wm.tool_set_by_id(name='builtin.select_box')

        return {'FINISHED'}

class TweakCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.tweak_command"
    bl_label = "Tweak"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.wm.tool_set_by_id(name='builtin.select')

        return {'FINISHED'}

class MoveCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.move_command"
    bl_label = "Move"
    
    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name='builtin.move')
        return {'FINISHED'}

class RotateCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.rotate_command"
    bl_label = "Rotate"
    
    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name='builtin.rotate')
        return {'FINISHED'}

class ScaleCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.scale_command"
    bl_label = "Scale"
    
    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name='builtin.scale')
        return {'FINISHED'}

class OBJECT_PT_Mfecane_tools(bpy.types.Panel):
   bl_label = "Mfecane toolset"
   bl_idname = "OBJECT_PT_Mfecane_tools"
   bl_space_type = 'VIEW_3D'
   bl_region_type = 'UI'
   bl_category = 'Mfecane toolset'
   
   def draw(self, context):
       layout = self.layout
    
       row = layout.row()
       row.label(text = "Manipulation", icon = "CUBE")

       row = layout.row()
       row.operator("mfecane_tools.object_select")
       row = layout.row()
       row.operator("mfecane_tools.vertex_select")
       row = layout.row()
       row.operator("mfecane_tools.edge_select")
       row = layout.row()
       row.operator("mfecane_tools.face_select")
       row = layout.row()
       row.operator("mfecane_tools.move_command")
       row = layout.row()
       row.operator("mfecane_tools.rotate_command")
       row = layout.row()
       row.operator("mfecane_tools.scale_command")
       row = layout.row()
       row.operator("mfecane_tools.tweak_command")

mfecane_keymaps = []

def disable_default_key(type=None, ctrl=False, retries=10):
    wm = bpy.context.window_manager
    
    if not type or retries < 1:
        return

    # the default keyconfig
    kc = wm.keyconfigs['blender']
    km_list = ['3D View', '3D View Generic']
    
    for km in km_list:
        for kmi in kc.keymaps[km].keymap_items:
            if kmi.type == type:
                kmi.active = False
                print("Disabled registered key: ", kmi.type, kmi.ctrl, "in", kc.keymaps[km].name)
                return

    print("Retrying..")

    # add some delay
    bpy.app.timers.register(
        lambda: disable_default_key(type, ctrl, retries - 1),
        first_interval=0.1)

def setup_hotkeys():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        disable_default_key(type='Q')
        kmi = km.keymap_items.new(ObjectSelect.bl_idname, type='Q', value='PRESS', ctrl=False)
        disable_default_key(type='W')
        kmi = km.keymap_items.new(MoveCommand.bl_idname, type='W', value='PRESS', ctrl=False)
        disable_default_key(type='E')
        kmi = km.keymap_items.new(RotateCommand.bl_idname, type='E', value='PRESS', ctrl=False)
        disable_default_key(type='R')
        kmi = km.keymap_items.new(ScaleCommand.bl_idname, type='R', value='PRESS', ctrl=False)
        disable_default_key(type='T')
        kmi = km.keymap_items.new(TweakCommand.bl_idname, type='T', value='PRESS', ctrl=False)
        disable_default_key(type='S')
        kmi = km.keymap_items.new(VertexSelect.bl_idname, type='S', value='PRESS', ctrl=False)
        disable_default_key(type='D')
        kmi = km.keymap_items.new(EdgeSelect.bl_idname, type='D', value='PRESS', ctrl=False)
        disable_default_key(type='F')
        kmi = km.keymap_items.new(FaceSelect.bl_idname, type='F', value='PRESS', ctrl=False)

        mfecane_keymaps.append((km, kmi))

classes = [
    ObjectSelect,
    VertexSelect,
    EdgeSelect,
    FaceSelect,
    MoveCommand,
    RotateCommand,
    ScaleCommand,
    TweakCommand,
    OBJECT_PT_Mfecane_tools,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    setup_hotkeys()
    
def unregister():
    for c in reversed(classes):
        bpy.utils.register_class(c)
    
if __name__ == "__main__":
    register()
