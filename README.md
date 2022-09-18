# install

    With extension Blender Development

        Blender: Start
        Blender: Reload Addons

# How to develop


# Snippets

        if obj.type == 'MESH':



        deleteList = [b for b in arm.data.edit_bones if b.name.startswith('DEF')]
        arm['selected_objects'] = deleteList
        arm.select_set(deleteList)
        bpy.ops.armature.delete()

        override = context.copy()
        override["selected_objects"] = list(context.scene.objects)
        with context.temp_override(**override):
            bpy.ops.object.delete()




        import bpy
        from mathutils import *

        def signed_angle(vector_u, vector_v, normal):
            # Normal specifies orientation
            angle = vector_u.angle(vector_v)
            if vector_u.cross(vector_v).angle(normal) < 1:
                angle = -angle
            return angle

        def get_pole_angle(base_bone, ik_bone, pole_location):
            pole_normal = (ik_bone.tail - base_bone.head).cross(pole_location - base_bone.head)
            projected_pole_axis = pole_normal.cross(base_bone.tail - base_bone.head)
            return signed_angle(base_bone.x_axis, projected_pole_axis, base_bone.tail - base_bone.head)

        base_bone = bpy.context.active_object.pose.bones["BASE_BONE_NAME"]
        ik_bone = bpy.context.active_object.pose.bones["IK_BONE_NAME"]
        pole_bone = bpy.context.active_object.pose.bones["POLE_BONE_NAME"]

        pole_angle_in_radians = get_pole_angle(base_bone,
                                            ik_bone,
                                            pole_bone.matrix.translation)
        pole_angle_in_deg = round(180*pole_angle_in_radians/3.141592, 3)
        print(pole_angle_in_deg)


        'CAMERA_SOLVER', 'FOLLOW_TRACK', 'OBJECT_SOLVER', 'COPY_LOCATION', 'COPY_ROTATION', 'COPY_SCALE', 'COPY_TRANSFORMS', 'LIMIT_DISTANCE', 'LIMIT_LOCATION', 'LIMIT_ROTATION', 'LIMIT_SCALE', 'MAINTAIN_VOLUME', 'TRANSFORM', 'TRANSFORM_CACHE', 'CLAMP_TO', 'DAMPED_TRACK', 'IK', 'LOCKED_TRACK', 'SPLINE_IK', 'STRETCH_TO', 'TRACK_TO', 'ACTION', 'ARMATURE', 'CHILD_OF', 'FLOOR', 'FOLLOW_PATH', 'PIVOT', 'SHRINKWRAP'

        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-9.31323e-10, 0, -0.0586262), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((-0.26011, -0.942515, 0.209782), (0.602502, 0.0113487, 0.798037), (-0.754542, 0.333972, 0.564915)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable_only":False, "use_snap_to_same_target":False, "snap_face_nearest_steps":1, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})


# Hotkeys

    "." in outliner to highlight

## Armature

    Shift+N Recalculate roll


bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(7.45058e-09, 1.26578, 0), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((-0.996347, -0.000874098, -0.0853886), (0.0850589, 0.0782194, -0.993301), (0.00754729, -0.996936, -0.0778594)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1.77156, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":True, "use_accurate":False, "use_automerge_and_split":False})


## Object

        def duplicate(obj, data=True, actions=True, collection=None):
            obj_copy = obj.copy()
            if data:
                obj_copy.data = obj_copy.data.copy()
            if actions and obj_copy.animation_data:
                obj_copy.animation_data.action = obj_copy.animation_data.action.copy()
            collection.objects.link(obj_copy)
            return obj_copy


        bpy.context.view_layer.objects.active = mesh 

copy objects

        mesh2 = mesh.copy()
        mesh2.data = mesh2.data.copy()
        context.collection.objects.link(mesh2)