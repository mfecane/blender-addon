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


mesh ops

        ['add_uvs', 'average_normals', 'beautify_fill', 'bevel', 'bisect', 'blend_from_shape', 'bridge_edge_loops', 'colors_reverse', 'colors_rotate', 'convex_hull', 'customdata_custom_splitnormals_add', 'customdata_custom_splitnormals_clear', 'customdata_mask_clear', 'customdata_skin_add', 'customdata_skin_clear', 'decimate', 'delete', 'delete_edgeloop', 'delete_loose', 'dissolve_degenerate', 'dissolve_edges', 'dissolve_faces', 'dissolve_limited', 'dissolve_mode', 'dissolve_verts', 'dupli_extrude_cursor', 'duplicate', 'duplicate_move', 'edge_collapse', 'edge_face_add', 'edge_rotate', 'edge_split', 'edgering_select', 'edges_select_sharp', 'extrude_context', 'extrude_context_move', 'extrude_edges_indiv', 'extrude_edges_move', 'extrude_faces_indiv', 'extrude_faces_move', 'extrude_manifold', 'extrude_region', 'extrude_region_move', 'extrude_region_shrink_fatten', 'extrude_repeat', 'extrude_vertices_move', 'extrude_verts_indiv', 'face_make_planar', 'face_set_extract', 'face_split_by_edges', 'faces_mirror_uv', 'faces_select_linked_flat', 'faces_shade_flat', 'faces_shade_smooth', 'fill', 'fill_grid', 'fill_holes', 'flip_normals', 'hide', 'inset', 'intersect', 'intersect_boolean', 'knife_project', 'knife_tool', 'loop_multi_select', 'loop_select', 'loop_to_region', 'loopcut', 'loopcut_slide', 'mark_freestyle_edge', 'mark_freestyle_face', 'mark_seam', 'mark_sharp', 'merge', 'merge_normals', 'mod_weighted_strength', 'normals_make_consistent', 'normals_tools', 'offset_edge_loops', 'offset_edge_loops_slide', 'paint_mask_extract', 'paint_mask_slice', 'point_normals', 'poke', 'polybuild_delete_at_cursor', 'polybuild_dissolve_at_cursor', 'polybuild_extrude_at_cursor_move', 'polybuild_face_at_cursor', 'polybuild_face_at_cursor_move', 'polybuild_split_at_cursor', 'polybuild_split_at_cursor_move', 'polybuild_transform_at_cursor', 'polybuild_transform_at_cursor_move', 'primitive_circle_add', 'primitive_cone_add', 'primitive_cube_add', 'primitive_cube_add_gizmo', 'primitive_cylinder_add', 'primitive_grid_add', 'primitive_ico_sphere_add', 'primitive_monkey_add', 'primitive_plane_add', 'primitive_torus_add', 'primitive_uv_sphere_add', 'quads_convert_to_tris', 'region_to_loop', 'remove_doubles', 'remove_inactive_uvs', 'remove_uvs', 'rename_uvs', 'reveal', 'rigify_encode_mesh_widget', 'rip', 'rip_edge', 'rip_edge_move', 'rip_move', 'screw', 'sculpt_vertex_color_add', 'sculpt_vertex_color_remove', 'select_all', 'select_axis', 'select_face_by_sides', 'select_interior_faces', 'select_less', 'select_linked', 'select_linked_pick', 'select_loose', 'select_mirror', 'select_mode', 'select_more', 'select_next_item', 'select_non_manifold', 'select_nth', 'select_prev_item', 'select_random', 'select_similar', 'select_similar_region', 'select_ungrouped', 'separate', 'set_normals_from_faces', 'shape_propagate_to_all', 'shortest_path_pick', 'shortest_path_select', 'show_uvs', 'smooth_normals', 'solidify', 'sort_elements', 'spin', 'split', 'split_normals', 'subdivide', 'subdivide_edgering', 'symmetrize', 'symmetry_snap', 'sync_uv_ids', 'tris_convert_to_quads', 'unsubdivide', 'uv_texture_add', 'uv_texture_remove', 'uvs_reverse', 'uvs_rotate', 'vert_connect', 'vert_connect_concave', 'vert_connect_nonplanar', 'vert_connect_path', 'vertex_color_add', 'vertex_color_remove', 'vertices_smooth', 'vertices_smooth_laplacian', 'wireframe', 'zenuv_mirror_seams', 'zenuv_select_seams', 'zenuv_select_sharp']