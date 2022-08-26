import bpy
from math import (
    pi as PI,
)
from mathutils import Vector

MCH_BONE_SIZE = 0.4

bones = []

rigging_settings = {
    'symmetrize': {
        'clavicle', 'upper_arm', 'lower_arm', 'hand', 'palm', 'finger', 'pelvis', 'upper_leg', 'lower_leg', 'ankle', 'toe', 'breast'
    }
}

rig_bones = []


def fix_single_bone(arm, bone, parentTgt=None):
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
            suffix = '.L'

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
    eb.use_deform = False

    # hide DEF bone

    if parentTgt:
        eb.matrix = bone.matrix.copy()
        if bone.use_connect:
            eb.use_connect = True

    # if bone.use_deform:
    #     eb.use_deform = False

    # repeat
    for b in bone.children:
        fix_single_bone(arm, b, eb)


leg_rig_data = {
    'bones': {}
}


def set_up_leg_rig(context):
    # TODO ensure bones
    arm = context.object
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    ebs = arm.data.edit_bones
    root = ebs['TGT_root']
    ankle = ebs['TGT_ankle.L']
    upper_leg = ebs['TGT_upper_leg.L']

    ankle.use_inherit_rotation = False

    # create IK bone
    ikLeg = ebs.new('MCH_ik_leg.L')
    ikLeg.use_deform = False
    ikLeg.use_connect = False
    ikLeg.head = ankle.head

    # TODO fix align
    ikLeg.tail = Vector(
        (ankle.head[0], ankle.head[1] + MCH_BONE_SIZE, ankle.head[2]))
    ikLeg.parent = root

    # create target
    lowerLeg = arm.data.edit_bones['TGT_lower_leg.L']
    upperLeg = arm.data.edit_bones['TGT_upper_leg.L']

    vec1 = lowerLeg.tail - lowerLeg.head
    vec1.normalize()
    vec2 = upperLeg.head - upperLeg.tail
    vec2.normalize()
    vec3 = vec1 + vec2
    vec3.normalize()

    ikLegTarget = ebs.new('MCH_ik_leg_target.L')
    ikLegTarget.use_deform = False
    ikLegTarget.use_connect = False
    ikLegTarget.head = upperLeg.tail - vec3 * 1.5
    ikLegTarget.tail = upperLeg.tail - vec3 * 2
    ikLegTarget.parent = root

    # IK constraint
    bpy.ops.object.mode_set(mode='POSE', toggle=False)
    lowerLeg = arm.pose.bones['TGT_lower_leg.L']

    ikLeg = arm.pose.bones['MCH_ik_leg.L']
    ikCstr = lowerLeg.constraints.new('IK')
    ikCstr.target = arm
    ikCstr.subtarget = 'MCH_ik_leg.L'
    ikCstr.chain_count = 2
    ikCstr.pole_target = arm
    ikCstr.pole_subtarget = 'MCH_ik_leg_target.L'
    ikCstr.pole_angle = PI / 2.0

    # lock unwanted axii
    lowerLeg.lock_ik_y = True
    lowerLeg.lock_ik_z = True

    ankle = arm.pose.bones['TGT_ankle.L']
    copyRotCstr = ankle.constraints.new('COPY_ROTATION')
    copyRotCstr.target = arm
    copyRotCstr.subtarget = 'MCH_ik_leg.L'
    copyRotCstr.invert_x = True
    copyRotCstr.target_space = 'LOCAL'
    copyRotCstr.owner_space = 'LOCAL'


def set_up_arm_rig(context):
    # TODO ensure bones
    arm = context.object
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    ebs = arm.data.edit_bones
    root = ebs['TGT_root']
    hand = ebs['TGT_hand.L']
    upper_arm = ebs['TGT_upper_arm.L']

    hand.use_inherit_rotation = False

    # create IK bone
    ikArm = ebs.new('MCH_ik_arm.L')
    ikArm.use_deform = False
    ikArm.use_connect = False
    ikArm.head = hand.head

    # TODO fix align
    ikArm.tail = Vector(
        (hand.head[0], hand.head[1] + MCH_BONE_SIZE, hand.head[2]))
    ikArm.parent = root

    # create target
    lowerArm = arm.data.edit_bones['TGT_lower_arm.L']
    upperArm = arm.data.edit_bones['TGT_upper_arm.L']

    vec1 = lowerArm.tail - lowerArm.head
    vec1.normalize()
    vec2 = upperArm.head - upperArm.tail
    vec2.normalize()
    vec3 = vec1 + vec2
    vec3.normalize()

    # TODO calculate transform
    ikArmTarget = ebs.new('MCH_ik_arm_target.L')
    ikArmTarget.use_deform = False
    ikArmTarget.use_connect = False
    ikArmTarget.head = upperArm.tail - vec3 * 1.5
    ikArmTarget.tail = upperArm.tail - vec3 * 2    
    ikArmTarget.parent = root

    # IK constraint
    bpy.ops.object.mode_set(mode='POSE', toggle=False)
    lowerArm = arm.pose.bones['TGT_lower_arm.L']
    ikArm = arm.pose.bones['MCH_ik_arm.L']
    ikCstr = lowerArm.constraints.new('IK')
    ikCstr.target = arm
    ikCstr.subtarget = 'MCH_ik_arm.L'
    ikCstr.chain_count = 2
    ikCstr.pole_target = arm
    ikCstr.pole_subtarget = 'MCH_ik_arm_target.L'
    ikCstr.pole_angle = -PI / 2.0

    # lock unwanted axii
    lowerArm.lock_ik_y = True
    lowerArm.lock_ik_z = True

    hand = arm.pose.bones['TGT_hand.L']
    copyRotCstr = hand.constraints.new('COPY_ROTATION')
    copyRotCstr.target = arm
    copyRotCstr.subtarget = 'MCH_ik_arm.L'
    copyRotCstr.invert_x = True
    copyRotCstr.target_space = 'LOCAL'
    copyRotCstr.owner_space = 'LOCAL'
    pass


def set_up_finger_rig(context, fingerIndex):
    print('fingerIndex', fingerIndex)

    arm = context.object
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    ebs = arm.data.edit_bones

    finger1 = ebs['TGT_finger_{}_1.L'.format(fingerIndex)]

    ctrlFinger1 = ebs.new('CTRL_finger_{}_1.L'.format(fingerIndex))
    ctrlFinger1.use_deform = False
    ctrlFinger1.use_connect = False
    ctrlFinger1.head = finger1.head
    ctrlFinger1.tail = Vector((
        finger1.head[0] + (finger1.tail[0] - finger1.head[0]) * 1.5,
        finger1.head[1] + (finger1.tail[1] - finger1.head[1]) * 1.5,
        finger1.head[2] + (finger1.tail[2] - finger1.head[2]) * 1.5
    ))

    # align selected bones to active bone
    bpy.ops.armature.select_all(action='DESELECT')
    arm.data.edit_bones.active = finger1
    ctrlFinger1.select = True
    bpy.ops.armature.align()

    ctrlFinger2 = ebs.new('CTRL_finger_{}_2.L'.format(fingerIndex))
    ctrlFinger2.use_deform = False
    ctrlFinger2.use_connect = False
    ctrlFinger2.head = ctrlFinger1.tail
    ctrlFinger2.parent = ctrlFinger1
    ctrlFinger2.tail = Vector((
        ctrlFinger1.tail[0] + (ctrlFinger1.tail[0] - ctrlFinger1.head[0]) * 0.5,
        ctrlFinger1.tail[1] + (ctrlFinger1.tail[1] - ctrlFinger1.head[1]) * 0.5,
        ctrlFinger1.tail[2] + (ctrlFinger1.tail[2] - ctrlFinger1.head[2]) * 0.5
    ))

    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    finger1 = arm.pose.bones['TGT_finger_{}_1.L'.format(fingerIndex)]
    finger2 = arm.pose.bones['TGT_finger_{}_2.L'.format(fingerIndex)]
    # finger3 = arm.pose.bones['TGT_finger_{}_3.L'.format(fingerIndex)]

    copyRot1 = finger1.constraints.new('COPY_ROTATION')
    copyRot1.target = arm
    copyRot1.subtarget = 'CTRL_finger_{}_1.L'.format(fingerIndex)
    copyRot1.target_space = 'LOCAL'
    copyRot1.owner_space = 'LOCAL'

    pass


def set_up_hand_rig(context):
    
    for fingerIndex in ['a', 'b', 'c', 'd', 'e']:
        set_up_finger_rig(context, fingerIndex)


class FixSkeleton(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.fix_skeleton"
    bl_label = "Fix Skeleton"

    def execute(self, context):

        # revert file




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

            arm.display_type = 'WIRE'
            fix_single_bone(arm, rootBone)

            bpy.ops.object.mode_set(mode='POSE', toggle=False)
            for boneName in rig_bones:
                srcBone = arm.pose.bones['DEF_' + boneName]
                # wtf
                # srcBone.bone.hide = True
                cstr = srcBone.constraints.new('COPY_TRANSFORMS')
                cstr.name = 'CSTR_TGTDEF_' + boneName
                cstr.target = arm
                cstr.subtarget = 'TGT_' + boneName
                pass

            set_up_leg_rig(context)
            set_up_arm_rig(context)
            set_up_hand_rig(context)

            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.symmetrize()

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


class TestPole(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.test_pole"
    bl_label = "TestPole"

    def execute(self, context):

        if context.object.type == 'ARMATURE':
            arm = context.object
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            ebs = arm.data.edit_bones
            sel = [v for v in ebs if v.select]
            
            if len(sel) != 2:
                raise NameError('Fuck you')

            bone1 = sel[0]
            bone2 = sel[1]

            vec1 = bone1.tail - bone1.head
            vec1.normalize()
            vec2 = bone2.head - bone2.tail
            vec2.normalize()
            vec3 = vec1 + vec2
            vec3.normalize()

            test3 = ebs.new('delete_me')
            test3.head = bone1.tail
            test3.tail = bone1.tail + vec3

        return {'FINISHED'}
