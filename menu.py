import bpy

class OBJECT_PT_Mfecane_tools(bpy.types.Panel):
    bl_label = "Mfecane toolset"
    bl_idname = "OBJECT_PT_Mfecane_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Mfecane toolset'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("mfecane_tools.set_up")

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
        row.operator("mfecane_tools.fix_skeleton")
        row = layout.row()
        row.operator("mfecane_tools.tentacle_rig")
        row = layout.row()
        row.operator("mfecane_tools.clean_skeleton")
        row = layout.row()
        row.operator("mfecane_tools.test_pole")
        row = layout.row()
        row.operator("mfecane_tools.export_fbx")
        row = layout.row()

        row.label(text="3D printing", icon="NLA")
        row = layout.row()
        row.operator("mfecane_tools.split_mesh")