import bpy

# split meshes and add keys for 3d printing

config = {
    'collections': {
        'target': 'target',
        'cutters': 'split'
    }
}

# TODO ::: detect direction of the mesh
# ? IDEA: get bounding boxes,
# check for volume of intersection boxes
# TODO ::: make copy of everything non destructive

def apply_modifiers(meshname, modifiername):
    bpy.ops.object.select_all(action='DESELECT')
    mesh = bpy.data.objects[meshname]
    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.modifier_apply(
        modifier=modifiername
    )


def seperate_loose(meshname):
    mesh = bpy.data.objects[meshname]
    mesh.select_set(True)

    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.select_all(action='DESELECT')

def prepare_cutter(mesh): 
    if mesh.name.startswith('thin_'):
        thickenMod = mesh.modifiers.new('thicken1', 'SOLIDIFY')
        thickenMod.offset = -1
        thickenMod.offset = 0.005
    apply_modifiers(mesh.name, thickenMod.name)


def triangulate(mesh): 
    triangulateMod = mesh.modifiers.new('triangulate1', 'TRIANGULATE')
    apply_modifiers(mesh.name, triangulateMod.name)


class SplitMesh(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.split_mesh"
    bl_label = "SplitMesh"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')

        collection = bpy.data.collections.new('result')
        context.scene.collection.children.link(collection)
        target_mesh = None

        for obj in bpy.data.collections[config['collections']['target']].objects:
            copy = obj.copy()
            copy.data = obj.data.copy()
            collection.objects.link(copy)
            target_mesh = copy

        # prepare cutters
        # TODO pre split all cutters
        # join all cutters
        tmp_cutters = []
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.collections[config['collections']['cutters']].objects:
            copy = obj.copy()
            copy.data = obj.data.copy()
            collection.objects.link(copy)
            prepare_cutter(copy)
            tmp_cutters.append(copy)
            bpy.context.view_layer.objects.active = copy 

        for obj in tmp_cutters:
            obj.select_set(True)

        bpy.ops.object.join()
        cutter_mesh = context.object
        
        booleanMod = target_mesh.modifiers.new('booolean1', 'BOOLEAN')
        booleanMod.object = cutter_mesh
        booleanMod.operation = 'DIFFERENCE'

        apply_modifiers(target_mesh.name, booleanMod.name)
        seperate_loose(target_mesh.name)

        bpy.data.objects.remove(cutter_mesh, do_unlink=True)

        # that's bull..

        bpy.context.view_layer.layer_collection.children.get(config['collections']['target']).hide_viewport = True
        bpy.context.view_layer.layer_collection.children.get(config['collections']['cutters']).hide_viewport = True

        for obj in collection.objects:
            obj.select_set(True)

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete_loose()
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.vert_connect_concave()
        bpy.ops.mesh.vert_connect_nonplanar()
        bpy.ops.mesh.fill_holes()

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        for obj in collection.objects:
            triangulate(obj)

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}
