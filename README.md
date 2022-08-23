# install

    With extension Blender Development

        Blender: Start
        Blender: Reload Addons

# How to develop


# Snippets

    if obj.type == 'MESH':

    # deleteList = [b for b in arm.data.edit_bones if b.name.startswith('DEF')]
    # arm['selected_objects'] = deleteList
    # arm.select_set(deleteList)
    # bpy.ops.armature.delete()

    # override = context.copy()
    # override["selected_objects"] = list(context.scene.objects)
    # with context.temp_override(**override):
    #     bpy.ops.object.delete()


# Hotkeys

## Armature

    Shift+N Recalculate roll


bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(7.45058e-09, 1.26578, 0), "orient_axis_ortho":'X', "orient_type":'NORMAL', "orient_matrix":((-0.996347, -0.000874098, -0.0853886), (0.0850589, 0.0782194, -0.993301), (0.00754729, -0.996936, -0.0778594)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1.77156, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":True, "use_accurate":False, "use_automerge_and_split":False})
