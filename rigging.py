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
    eb.show_axis = True
    eb.show_in_front = True
    bone.hide = False
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
            # arm.show_axis = True
            # arm.show_in_front = True
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


rigging_settings = {
    'symmetrize': {
        'clavicle', 'upper_arm', 'lower_arm', 'hand', 'palm', 'finger', 'pelvis', 'upper_leg', 'lower_leg', 'ankle', 'toe', 'breast'
    }
}

rig_bones = []

def fix_single_bone(arm, bone, parentTgt = None):
    # clean up name
    name = bone.name
    right = name.endswith('.R')
    left = name.endswith('.L')
    suffix = ''
    if right: 
        suffix = '.R'
    if left: 
        suffix = '.L'

    cleanName = bone.name.lstrip('DEF_').rstrip('.L').rstrip('.R')

    for sym in rigging_settings['symmetrize']:
        if sym in cleanName and not right and not left:
            left = True

    # rename bone
    name = 'DEF_' + cleanName + suffix
    bone.name = name
    rig_bones.append(cleanName + suffix)

    if cleanName == 'root':
        bone.use_deform = False
    else:
        bone.use_deform = True

    # create TGT bone
    ebs = arm.data.edit_bones
    eb = ebs.new('TGT_' + cleanName + suffix)
    eb.parent = parentTgt
    eb.tail = bone.tail
    eb.head = bone.head
    bone.hide = False

    if parentTgt:
        eb.matrix = bone.matrix.copy()
        if bone.use_connect:
            eb.use_connect = True

    if bone.use_deform:
        eb.use_deform = False

    # repeat
    for b in bone.children:
        fix_single_bone(arm, b, eb)


class FixSkeleton(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.fix_skeleton"
    bl_label = "Fix Skeleton"

    def execute(self, context):
        if context.object.type == 'ARMATURE':
            arm = context.object
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)

            # get root bone
            rootBone = None
            for b in arm.data.edit_bones:
                if not b.parent:
                    if b.name.startswith('TGT'):
                        raise NameError('Target bones not removed')

                    if rootBone:
                        raise NameError('Multiple root bones')

                    rootBone = b

            fix_single_bone(arm, rootBone)
        
        bpy.ops.object.mode_set(mode='POSE', toggle=False)
        for boneName in rig_bones:
            srcBone = arm.pose.bones['DEF_' + boneName]
            cstr = srcBone.constraints.new('COPY_TRANSFORMS')
            cstr.name = 'CSTR_TGTDEF_' + boneName
            cstr.target = arm
            cstr.subtarget = 'TGT_' + boneName
            pass

        return {'FINISHED'}


class CleanUp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.clean_skeleton"
    bl_label = "Clean Skeleton"

    def execute(self, context):
        if context.object.type == 'ARMATURE':
            arm = context.object
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)

            # deleteList = [b for b in arm.data.edit_bones if b.name.startswith('DEF')]
            # arm['selected_objects'] = deleteList
            # arm.select_set(deleteList)
            # bpy.ops.armature.delete()

            # override = context.copy()
            # override["selected_objects"] = list(context.scene.objects)
            # with context.temp_override(**override):
            #     bpy.ops.object.delete()

            for b in arm.data.edit_bones:
                if b.name.startswith('TGT'):
                    arm.data.edit_bones.remove(b)
                    continue
                b.name = b.name.lstrip('TGT_')
                b.name = b.name.rstrip('.L')
                b.name = b.name.rstrip('.R')


        return {'FINISHED'}
