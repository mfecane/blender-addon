import bpy

# split meshes and add keys for 3d printing


class SplitMesh(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.split_mesh"
    bl_label = "SplitMesh"

    def execute(self, context):
        # simple split with plane
        # fails if it has 2 intersections

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.select_all(action='DESELECT')

        mesh = bpy.data.objects['mesh']
        split = bpy.data.objects['split']
        mesh.select_set(True)

        mesh2 = mesh.copy()
        mesh2.data = mesh2.data.copy()
        context.collection.objects.link(mesh2)

        booleanMod = mesh.modifiers.new('booolean1', 'BOOLEAN')
        booleanMod.object = split
        booleanMod.operation = 'DIFFERENCE'

        booleanMod2 = mesh2.modifiers.new('booolean2', 'BOOLEAN')
        booleanMod2.object = split
        booleanMod2.operation = 'INTERSECT'

        bpy.context.view_layer.objects.active = mesh
        bpy.ops.object.modifier_apply(
            modifier='booolean1'
        )

        bpy.context.view_layer.objects.active = mesh2
        bpy.ops.object.modifier_apply(
            modifier='booolean2'
        )

        return {'FINISHED'}
