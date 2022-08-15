import bpy
import bmesh

# TODO ::: snap with single click ?


mfecane_keymaps = []


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
        print('face selection')

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
        bpy.ops.mesh.select_mode(
            use_extend=False, use_expand=False, type='VERT')
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


class CutCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.cut_command"
    bl_label = "Cut"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.wm.tool_set_by_id(name="builtin.knife")
        return {'FINISHED'}


class LoopCutCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.loop_cut_command"
    bl_label = "Loop cut"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.wm.tool_set_by_id(name="builtin.loop_cut")
        return {'FINISHED'}


class ExtrudeCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.extrude_command"
    bl_label = "Extrude command"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.view3d.edit_mesh_extrude_move_normal()
        return {'FINISHED'}


class BridgeCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.bridge_command"
    bl_label = "Bridge command"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.bridge_edge_loops()
        return {'FINISHED'}


class AddCommand(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.add_command"
    bl_label = "Add command"

    def execute(self, context):
        bpy.ops.wm.call_menu(name="VIEW3D_MT_add")
        return {'FINISHED'}

# class SnapOnCommand(bpy.types.Operator):
#     """Tooltip"""
#     bl_idname = "mfecane_tools.snap_on_command"
#     bl_label = "Snap on command"

#     def execute(self, context):

#         return {'FINISHED'}

# class SnapOffCommand(bpy.types.Operator):
#     """Tooltip"""
#     bl_idname = "mfecane_tools.snap_off_command"
#     bl_label = "Snap off command"

#     def execute(self, context):

#         return {'FINISHED'}


class Subsurf1(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.subsurf1_command"
    bl_label = "Set subsurf to 0"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.subdivision_set(level=0, relative=False)
        return {'FINISHED'}


class Subsurf2(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.subsurf2_command"
    bl_label = "Set subsurf to 1"

    def execute(self, context):
        bpy.ops.object.subdivision_set(level=1, relative=False)
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        return {'FINISHED'}


class Subsurf3(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.subsurf3_command"
    bl_label = "Set subsurf to 2"

    def execute(self, context):
        print('3')
        bpy.ops.object.subdivision_set(level=2, relative=False)
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        return {'FINISHED'}


class SaneDelete(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.sane_delete"
    bl_label = "Sane delete"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.delete(use_global=False)
            return {'FINISHED'}

        selectedFaces = [
            f for f in context.active_object.data.polygons if f.select]
        if len(selectedFaces):
            bpy.ops.mesh.delete(type='FACE')
            return {'FINISHED'}

        selectedEdges = [
            e for e in context.active_object.data.edges if e.select]
        if len(selectedEdges):
            bpy.ops.mesh.dissolve_edges()
            return {'FINISHED'}

        selectedVerts = [
            v for v in context.active_object.data.vertices if v.select]
        if len(selectedVerts):
            bpy.ops.mesh.dissolve_verts()
            return {'FINISHED'}

        return {'FINISHED'}


class EdgeSlide(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.edge_slide"
    bl_label = "Edge Slide"

    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name='builtin.edge_slide')
        return {'FINISHED'}


class SnapToCenterX(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.snap_to_center_x"
    bl_label = "Snap To Center X"

    def execute(self, context):
        object = context.object
        bm = bmesh.from_edit_mesh(object.data)
        for v1 in bm.verts:
            if v1.select:
                v1.co[0] = 0
        bm.select_flush_mode()
        bmesh.update_edit_mesh(object.data)

        # selectedVerts = [
        #     v for v in context.active_object.data.vertices if v.select]
        # if len(selectedVerts):
        #     for v in selectedVerts:
        #         print(v.co[0])
        #         v.co[0] = 0
        #     bmesh.update_edit_mesh(context.active_object.data)

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
        row.label(text="Manipulation", icon="CUBE")

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
        row = layout.row()
        row.operator("mfecane_tools.cut_command")
        row = layout.row()
        row.operator("mfecane_tools.loop_cut_command")
        row = layout.row()
        row.operator("mfecane_tools.subsurf1_command")
        row = layout.row()
        row.operator("mfecane_tools.subsurf2_command")
        row = layout.row()
        row.operator("mfecane_tools.subsurf3_command")
        row = layout.row()
        row.operator("mfecane_tools.sane_delete")
        row = layout.row()
        row.operator("mfecane_tools.snap_to_center_x")

        row = layout.row()
        row.label(text="Rigging", icon="NLA")
        row = layout.row()
        row.operator("mfecane_tools.copy_armature")


def print_kmi(km, kmi):
    print("removing keymap item")
    print("\tkm: ", km.name, " ", end='')
    print("kmi: ", kmi.name, " ", end='')
    print("kmi.type: ", kmi.type, " ", end='')
    print("kmi.ctrl: ", kmi.ctrl, " ", end='')
    print("kmi.shift: ", kmi.shift, " ", end='')
    print("kmi.alt: ", kmi.alt, " ", end='')
    print("kmi.any: ", kmi.any, " ", end='')
    print("")


def disable_default_key(type=None, ctrl=False, shift=False, alt=False,  retries=3):
    wm = bpy.context.window_manager

    if not type or retries < 1:
        return

    # the default keyconfig
    kc = wm.keyconfigs['Blender']
    km_list = ["3D View", "3D View Generic", "Mesh", "Object Mode"]
    # , "Transform Modifier"

    success = False
    for km in km_list:
        for kmi in kc.keymaps[km].keymap_items:
            if kmi.type == type and \
                ((kmi.ctrl == ctrl and
                  kmi.shift == shift and
                  kmi.alt == alt) or
                 kmi.any == True):
                kmi.active = False
                print_kmi(kc.keymaps[km], kmi)
                success = True

    if success:
        return

    print("retrying.. ", end="")

    # add some delay
    bpy.app.timers.register(
        lambda: disable_default_key(type, ctrl, shift, alt, retries - 1),
        first_interval=0.5)


def desable_rest(retries=10):
    if not type or retries < 1:
        return

    km = bpy.context.window_manager.keyconfigs['Blender'].keymaps['Grease Pencil']
    for kmi in km.keymap_items:
        if kmi.type == 'LEFTMOUSE' and \
                kmi.key_modifier == 'D':
            print_kmi(km, kmi)
            kmi.active = False
            success = True

    if success:
        return

    print("retrying.. ", end="")

    # add some delay
    bpy.app.timers.register(
        lambda: desable_rest(retries - 1),
        first_interval=0.5)


def debug_log_keymaps():
    print('DEBUGGING_SHIT')
    k = bpy.context.window_manager.keyconfigs['Blender'].keymaps['Mesh'].keymap_items
    for kmi in k:
        if kmi.type == 'R':
            print("\n")
            print(dir(kmi))
            print("\n")
            print(kmi.to_string())
            print("kmi.name", kmi.name)
            print("kmi.map_type", kmi.map_type)
            print("kmi.rna_type", kmi.rna_type)
            print("kmi.type", kmi.type)
            print("kmi.value", kmi.value)
            print("kmi.properties", kmi.properties)
            print("kmi.propvalue", kmi.propvalue)
            print("\n")
            prop = kmi.properties
            print("prop", dir(prop))
    print('DEBUGGING_SHIT DONE')


def setup_hotkeys():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = wm.keyconfigs.addon.keymaps.new(
            name='3D View', space_type='VIEW_3D')

        debug_log_keymaps()

        disable_default_key(type='Q')
        disable_default_key(type='W')
        disable_default_key(type='E')
        disable_default_key(type='R')
        disable_default_key(type='T')
        disable_default_key(type='S')
        disable_default_key(type='D')
        disable_default_key(type='D Left Mouse')
        disable_default_key(type='F')
        disable_default_key(type='X')
        disable_default_key(type='X', ctrl=True)
        disable_default_key(type='R', ctrl=True)
        disable_default_key(type='C')
        disable_default_key(type='C', shift=True)
        disable_default_key(type='E', ctrl=True)
        disable_default_key(type='A', ctrl=True)
        disable_default_key(type='ONE')
        disable_default_key(type='TWO')
        disable_default_key(type='THREE')
        desable_rest()

        kmi = km.keymap_items.new(
            ObjectSelect.bl_idname, type='Q', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            MoveCommand.bl_idname, type='W', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            RotateCommand.bl_idname, type='E', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            ScaleCommand.bl_idname, type='R', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            TweakCommand.bl_idname, type='T', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            VertexSelect.bl_idname, type='S', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            EdgeSelect.bl_idname, type='D', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            FaceSelect.bl_idname, type='F', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            SaneDelete.bl_idname, type='X', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            CutCommand.bl_idname, type='C', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            LoopCutCommand.bl_idname, type='C', value='PRESS', shift=True)
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            ExtrudeCommand.bl_idname, type='E', value='PRESS', ctrl=True)
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            BridgeCommand.bl_idname, type='B', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            AddCommand.bl_idname, type='A', value='PRESS', ctrl=True)
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            Subsurf1.bl_idname, type='ONE', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            Subsurf2.bl_idname, type='TWO', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            Subsurf3.bl_idname, type='THREE', value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            EdgeSlide.bl_idname, type='R', ctrl=True, value='PRESS')
        mfecane_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            'transform.vert_slide', type='LEFTMOUSE', ctrl=True, shift=True, value='PRESS')
        mfecane_keymaps.append((km, kmi))

        # kmi = km.keymap_items.new(
        #     'transform.translate', type='MIDDLEMOUSE', ctrl=True, value='PRESS')
        # mfecane_keymaps.append((km, kmi))

        # wm.tool_set_by_id
        # builtin.edge_slide

        # km2 = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        # kmi = km.keymap_items.new(Subsurf3.bl_idname, type='X', value='PRESS')
        # kmi = km.keymap_items.new(Subsurf3.bl_idname, type='X', value='RELEASE')
        # mfecane_keymaps.append((km2, kmi))


def remove_hotkeys():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in mfecane_keymaps:
            km.keymap_items.remove(kmi)
    mfecane_keymaps.clear()
