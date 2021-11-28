### SNIPPETS ###

tools = bpy.context.workspace.tools
active_tool = tools.from_space_view3d_mode(bpy.context.mode).idname
active_tool = bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname

area = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]
override_context = bpy.context.copy()
override_context['window'] = bpy.context.window
override_context['screen'] = bpy.context.screen
override_context['area'] = area
override_context['region'] = area.regions[-1]
override_context['scene'] = bpy.context.scene
override_context['space_data'] = area.spaces.active

area = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]
override_context = bpy.context.copy()
override_context['window'] = bpy.context.window
override_context['screen'] = bpy.context.screen
override_context['area'] = area
override_context['region'] = area.regions[-1]
override_context['scene'] = bpy.context.scene
override_context['space_data'] = area.spaces.active

bpy.ops.wm.tool_set_by_id(name='builtin.select')
list(override_context.workspace.tools)

bpy.ops.wm.tool_set_by_id(name = "builtin.select_circle")
# Get the tool
tool = ToolSelectPanelHelper.tool_active_from_context(context)
props = tool.operator_properties('view3d.select_circle')

# Print all properties
print (dir(props))
[...'mode', 'radius', 'rna_type', 'wait_for_input', 'x', 'y']

# Set the properties
props.mode = 'SUB'
props.radius = 50

list(bpy.context.workspace.tools)

tool = bpy.context.workspace.tools.get('builtin.select')

# info
# hotkey file C:\Users\Mfecane\AppData\Roaming\Blender Foundation\Blender\2.92\scripts\presets\keyconfig