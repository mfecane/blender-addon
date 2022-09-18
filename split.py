import bpy

# split meshes and add keys for 3d printing

def apply_modifiers(meshname, modifiername):
    bpy.ops.object.select_all(action='DESELECT')
    mesh = bpy.data.objects[meshname]        
    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.modifier_apply(
        modifier=modifiername
    )

class SplitMesh(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.split_mesh"
    bl_label = "SplitMesh"

    def execute(self, context):
        # simple split with thinly extruded plane

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')

        mesh = bpy.data.objects['mesh']
        # TODO ::: make copy
        split = bpy.data.objects['split1']
        # TODO ::: generate keys
        key_mesh = bpy.data.objects['key1']
        mesh.select_set(True)

        thickenMod = split.modifiers.new('thicken1', 'SOLIDIFY')
        thickenMod.offset = -1
        thickenMod.offset = 0.005

        booleanMod = mesh.modifiers.new('booolean1', 'BOOLEAN')
        booleanMod.object = split
        booleanMod.operation = 'DIFFERENCE'

        bpy.context.view_layer.objects.active = mesh
        bpy.ops.object.modifier_apply(
            modifier='booolean1'
        )
        
        bpy.ops.object.select_all(action='DESELECT')
        mesh.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')

        target_mesh1 = bpy.data.objects['mesh']
        target_mesh1.name = 'split_result_1'
        target_mesh2 = bpy.data.objects['mesh.001']
        target_mesh2.name = 'split_result_2'

        # TODO ::: detect direction of the mesh

        # IDEA get bounding boxes,
        # check for volume of intersection boxes

        booleanMod2 = target_mesh1.modifiers.new('booolean2', 'BOOLEAN')
        booleanMod2.object = key_mesh
        booleanMod2.operation = 'UNION'

        booleanMod3 = target_mesh2.modifiers.new('booolean3', 'BOOLEAN')
        booleanMod3.object = key_mesh
        booleanMod3.operation = 'DIFFERENCE'

        apply_modifiers(target_mesh1.name, booleanMod2.name)
        apply_modifiers(target_mesh2.name, booleanMod3.name)

        return {'FINISHED'}
