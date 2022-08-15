import bpy


bones = []


def copy_bone(arm, bone, parent=None):
    if not bone.name.startswith('DEF'):
        bone.name = 'DEF_' + bone.name
    name = bone.name.lstrip('DEF_')
    bones.append(name)
    ebs = arm.data.edit_bones
    eb = ebs.new('TGT_' + name)
    eb.parent = parent
    eb.tail = bone.tail
    eb.head = bone.head
    bone.hide = True
    if parent:
        eb.matrix = bone.matrix.copy()
        eb.use_connect = True
    eb.use_deform = False
    for b in bone.children:
        copy_bone(arm, b, eb)


def add_constraints(arm):
    bpy.ops.object.mode_set(mode='POSE', toggle=False)
    for boneName in bones:
        srcBone = arm.pose.bones['DEF_' + boneName]
        cstr = srcBone.constraints.new('COPY_TRANSFORMS')
        cstr.name = 'CSTR_TGTDEF_' + boneName
        cstr.target = arm
        cstr.subtarget = 'TGT_' + boneName
        pass


class CopyArmature(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.copy_armature"
    bl_label = "Copy Armature"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        if context.object.type == 'ARMATURE':
            arm = context.object
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)

            rootBone = None
            for b in context.object.data.edit_bones:
                if not b.parent:
                    if rootBone:
                        raise NameError('Multiple root bones')
                    rootBone = b

            copy_bone(arm, rootBone, None)

            add_constraints(arm)

        return {'FINISHED'}
