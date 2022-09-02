from cmath import pi
import bpy
from math import (
    pi as PI, atan2
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

def getBone(context, name):
    arm = context.object
    bone = None
    try:
        if arm.mode == 'EDIT':
            bone = arm.data.edit_bones[name]
        if arm.mode == 'POSE':
            bone = arm.pose.bones[name]
    except:
        raise RuntimeError('Failed to retrieve bone "{}"'.format(name))
    return bone


def getLayers(layers):
    return [n in layers for n in range(0, 32)]


def selectBone(context, name):
    bpy.ops.armature.select_all(action='DESELECT')
    bone = getBone(context, name)
    bone.select = True

# TODO: handle errors
def alignBone(context, srcBone, tgtBone):
    arm = context.object
    bpy.ops.armature.select_all(action='DESELECT')
    arm.data.edit_bones.active = srcBone
    tgtBone.select = True
    bpy.ops.armature.align()
    bpy.ops.armature.select_all(action='DESELECT')


def prepare_skeleton(context):

    # subdivide arm bones
    selectBone(context, 'lower_arm')
    bpy.ops.armature.subdivide()

    lower1 = getBone(context, 'lower_arm')
    lower2 = getBone(context, 'lower_arm.001')
    lower1.name = 'lower_arm_1'
    lower2.name = 'lower_arm_2'


def prepare_single_bone(arm, bone, parentTgt=None):
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
        prepare_single_bone(arm, b, eb)


def set_up_torso_rig(context):
    arm = context.object
    ebs = arm.data.edit_bones
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
    hips = getBone(context, 'TGT_hips')
    spine = getBone(context, 'TGT_spine')
    chest = getBone(context, 'TGT_chest')
    root = getBone(context, 'TGT_root')
    root.layers = getLayers([0, 1])

    breast = getBone(context, 'TGT_breast.L')
    breast.layers = getLayers([0, 1])

    clavicle = getBone(context, 'TGT_clavicle.L')
    clavicle.layers = getLayers([0, 1])

    neck = getBone(context, 'TGT_neck')
    neck.layers = getLayers([0, 1])

    head = getBone(context, 'TGT_head')
    head.layers = getLayers([0, 1])

    ctrlTorso = ebs.new('CTRL_torso')
    ctrlTorso.use_deform = False
    ctrlTorso.use_connect = False
    ctrlTorso.head = spine.head
    ctrlTorso.tail = spine.head + Vector((0.0, 1.5, 0.0))
    ctrlTorso.parent = root
    ctrlTorso.layers = getLayers([0, 1])

    ctrlHips = ebs.new('CTRL_hips')
    ctrlHips.use_deform = False
    ctrlHips.use_connect = False
    ctrlHips.head = spine.head
    ctrlHips.tail = hips.head
    ctrlHips.parent = ctrlTorso
    ctrlHips.layers = getLayers([0, 1])
    hips.parent = ctrlHips

    ctrlSpine = ebs.new('CTRL_spine')
    ctrlSpine.use_deform = False
    ctrlSpine.use_connect = False
    ctrlSpine.head = spine.head
    ctrlSpine.tail = chest.head
    ctrlSpine.parent = ctrlTorso
    ctrlSpine.layers = getLayers([0, 1])
    
    spine.use_connect = False
    spine.parent = ctrlSpine
    
    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    ctrlSpine = getBone(context, 'CTRL_spine')
    chest = getBone(context, 'TGT_chest')
    
    cpRotCstr1 = chest.constraints.new('COPY_ROTATION')
    cpRotCstr1.target = arm
    cpRotCstr1.subtarget = ctrlSpine.name
    cpRotCstr1.target_space = 'LOCAL'
    cpRotCstr1.owner_space = 'LOCAL'
    

def set_up_leg_rig(context):
    arm = context.object
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    ebs = arm.data.edit_bones

    root = getBone(context, 'TGT_root')
    ankle = getBone(context, 'TGT_ankle.L')
    upper_leg = getBone(context, 'TGT_upper_leg.L')
    lowerLeg = getBone(context, 'TGT_lower_leg.L')
    upperLeg = getBone(context, 'TGT_upper_leg.L')


    # create IK bone
    
    ikLeg = ebs.new('MCH_ik_leg.L')
    ikLeg.use_deform = False
    ikLeg.use_connect = False
    ikLeg.parent = root
    ikLeg.head = ankle.head
    vec = ankle.tail - ankle.head
    vec.normalize()
    ikLeg.head = ankle.head
    ikLeg.tail = ankle.head + vec * 0.4
    alignBone(context, ankle, ikLeg)
    ikLeg.layers = getLayers([0, 1])

    # create target

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
    ikLegTarget.layers = getLayers([0, 1])

    rollBone = ebs.new('MCH_foot_roll.L')
    rollBone.use_deform = False
    rollBone.use_connect = False
    rollBone.parent = root
    rollBone.head = ankle.tail
    vec = ankle.tail - ankle.head
    vec[2] = 0.0
    rollBone.tail = ankle.tail - vec * 1.3
    rollBone.tail[2] = 0.0
    angle = atan2(vec[0], -vec[1])
    print('roll angle', angle)

    rollBone2 = ebs.new('MCH_foot_roll_2.L')
    rollBone2.use_deform = False
    rollBone2.use_connect = False
    rollBone2.parent = root
    rollBone2.head = rollBone.tail
    rollBone2.tail = rollBone.tail + Vector((0.0, 0.0, 0.5))
    rollBone2.roll = angle 

    ctrlRoll = ebs.new('CTRL_foot_roll.L')
    ctrlRoll.use_deform = False
    ctrlRoll.use_connect = False
    ctrlRoll.parent = root
    ctrlRoll.head = rollBone.tail - vec * 1.0
    ctrlRoll.head[2] = 0.0
    ctrlRoll.tail = rollBone.tail - vec * 1.0
    ctrlRoll.tail[2] = 0.5
    ctrlRoll.layers = getLayers([0, 1])

    alignBone(context, rollBone2, ctrlRoll)

    ikLeg.parent = rollBone
    rollBone.parent = rollBone2

    # IK constraint
    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    root = getBone(context, 'TGT_root')
    ankle = getBone(context, 'TGT_ankle.L')
    toe = getBone(context, 'TGT_toe.L')
    upper_leg = getBone(context, 'TGT_upper_leg.L')
    lowerLeg = getBone(context, 'TGT_lower_leg.L')
    upperLeg = getBone(context, 'TGT_upper_leg.L')
    ikLeg = getBone(context, 'MCH_ik_leg.L')
    ikTarget = getBone(context, 'MCH_ik_leg_target.L')
    rollBone = getBone(context, 'MCH_foot_roll.L')
    rollBone2 = getBone(context, 'MCH_foot_roll_2.L')
    ctrlRoll = getBone(context, 'CTRL_foot_roll.L')

    ctrlRoll.rotation_mode = 'XYZ'
    ctrlRoll.lock_rotation[1] = True
    ctrlRoll.lock_rotation[2] = True

    ikCstr = lowerLeg.constraints.new('IK')
    ikCstr.target = arm
    ikCstr.subtarget = ikLeg.name
    ikCstr.chain_count = 2
    ikCstr.pole_target = arm
    ikCstr.pole_subtarget = ikTarget.name
    ikCstr.pole_angle = PI / 2.0

    # lock unwanted axii
    lowerLeg.lock_ik_y = True
    lowerLeg.lock_ik_z = True

    copyRotCstr = ankle.constraints.new('COPY_ROTATION')
    copyRotCstr.target = arm
    copyRotCstr.subtarget = ikLeg.name
    copyRotCstr.target_space = 'WORLD'
    copyRotCstr.owner_space = 'WORLD'

    copyRotCstr2 = rollBone.constraints.new('COPY_ROTATION')
    copyRotCstr2.target = arm
    copyRotCstr2.subtarget = ctrlRoll.name
    copyRotCstr2.target_space = 'LOCAL'
    copyRotCstr2.owner_space = 'LOCAL'

    limitRotCstr = rollBone.constraints.new('LIMIT_ROTATION')
    limitRotCstr.use_limit_x = True
    limitRotCstr.min_x = 0
    limitRotCstr.max_x = PI/2
    limitRotCstr.owner_space = 'LOCAL'

    copyRotCstr3 = rollBone2.constraints.new('COPY_ROTATION')
    copyRotCstr3.target = arm
    copyRotCstr3.subtarget = ctrlRoll.name
    copyRotCstr3.target_space = 'LOCAL'
    copyRotCstr3.owner_space = 'LOCAL'

    limitRotCstr2 = rollBone2.constraints.new('LIMIT_ROTATION')
    limitRotCstr2.use_limit_x = True
    limitRotCstr2.min_x = -PI/2
    limitRotCstr2.max_x = 0
    limitRotCstr2.owner_space = 'LOCAL'

    copyRotCstr4 = toe.constraints.new('COPY_ROTATION')
    copyRotCstr4.target = arm
    copyRotCstr4.subtarget = rollBone.name
    copyRotCstr4.target_space = 'LOCAL'
    copyRotCstr4.owner_space = 'LOCAL'

def set_up_arm_rig(context):
    # EDIT MODE

    arm = context.object
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    ebs = arm.data.edit_bones
    root = getBone(context, 'TGT_root')
    clavicle = getBone(context, 'TGT_clavicle.L')
    upper = getBone(context, 'TGT_upper_arm.L')
    lower1 = getBone(context, 'TGT_lower_arm_1.L')
    lower2 = getBone(context, 'TGT_lower_arm_2.L')
    hand = getBone(context, 'TGT_hand.L')

    # create IK bone
    # TODO important! align this bone
    ikArm = ebs.new('MCH_ik_arm.L')
    ikArm.use_connect = False
    ikArm.parent = root
    ikArm.use_deform = False
    vec = hand.tail - hand.head
    vec.normalize()
    ikArm.head = hand.head
    ikArm.tail = hand.head + vec * 0.4
    alignBone(context, hand, ikArm)

    # create target
    vec1 = lower1.tail - lower1.head
    vec1.normalize()
    vec2 = upper.head - upper.tail
    vec2.normalize()
    vec3 = vec1 + vec2
    vec3.normalize()

    ikArmTarget = ebs.new('MCH_ik_arm_target.L')
    ikArmTarget.use_deform = False
    ikArmTarget.use_connect = False
    ikArmTarget.head = upper.tail - vec3 * 1.5
    ikArmTarget.tail = upper.tail - vec3 * 2
    ikArmTarget.parent = root

    # create ik chain

    upperIK = ebs.new('MCH_ik_upper_arm.L')
    upperIK.use_deform = False
    upperIK.use_connect = False
    upperIK.parent = clavicle
    upperIK.head = upper.head
    upperIK.tail = upper.tail
    upperIK.matrix = upper.matrix.copy()

    lowerIK = ebs.new('MCH_ik_lower_arm.L')
    lowerIK.use_deform = False
    lowerIK.use_connect = True
    lowerIK.parent = upperIK
    lowerIK.head = upperIK.tail
    lowerIK.tail = lower2.tail
    lowerIK.matrix = lower1.matrix.copy()

    hand.parent = lowerIK
    hand.use_connect = True

    # POSE MODE

    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    upperIk = getBone(context, 'MCH_ik_upper_arm.L')
    lowerIk = getBone(context, 'MCH_ik_lower_arm.L')
    lowerIk = getBone(context, 'MCH_ik_lower_arm.L')
    ikArm = getBone(context, 'MCH_ik_arm.L')
    ikArmTarget = getBone(context, 'MCH_ik_arm_target.L')

    upper = getBone(context, 'TGT_upper_arm.L')
    lower1 = getBone(context, 'TGT_lower_arm_1.L')
    lower2 = getBone(context, 'TGT_lower_arm_2.L')
    hand = getBone(context, 'TGT_hand.L')

    ikArmTarget.bone.layers = getLayers([0, 1])
    
    # IK constraint

    ikCstr = lowerIk.constraints.new('IK')
    ikCstr.target = arm
    ikCstr.subtarget = ikArm.name
    ikCstr.chain_count = 2
    ikCstr.pole_target = arm
    ikCstr.pole_subtarget = 'MCH_ik_arm_target.L'
    ikCstr.pole_angle = -PI / 2.0

    ikArm.bone.layers = getLayers([0, 1])

    # lock unwanted axii

    lowerIk.lock_ik_y = True
    lowerIk.lock_ik_z = True

    copyTrCstr = upper.constraints.new('COPY_TRANSFORMS')
    copyTrCstr.target = arm
    copyTrCstr.subtarget = upperIk.name
    copyTrCstr.target_space = 'LOCAL'
    copyTrCstr.owner_space = 'LOCAL'

    # constraint lower arm

    dmpTrckCstr1 = lower1.constraints.new('DAMPED_TRACK')
    dmpTrckCstr1.target = arm
    dmpTrckCstr1.subtarget = lower2.name

    cpRotCstr1 = lower1.constraints.new('COPY_ROTATION')
    cpRotCstr1.target = arm
    cpRotCstr1.subtarget = lowerIk.name
    cpRotCstr1.target_space = 'LOCAL'
    cpRotCstr1.owner_space = 'LOCAL'

    cpRotCstr2 = lower2.constraints.new('COPY_ROTATION')
    cpRotCstr2.target = arm
    cpRotCstr2.subtarget = hand.name
    cpRotCstr2.target_space = 'WORLD'
    cpRotCstr2.owner_space = 'WORLD'

    dmpTrckCstr2 = lower2.constraints.new('DAMPED_TRACK')
    dmpTrckCstr2.target = arm
    dmpTrckCstr2.subtarget = hand.name

    cpRotCstr2 = hand.constraints.new('COPY_ROTATION')
    cpRotCstr2.target = arm
    cpRotCstr2.subtarget = ikArm.name
    cpRotCstr2.target_space = 'WORLD'
    cpRotCstr2.owner_space = 'WORLD'


def set_up_palm_rig(context):
    arm = context.object
    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    palma = getBone(context, 'TGT_palm_a.L')
    palmb = getBone(context, 'TGT_palm_b.L')
    palmc = getBone(context, 'TGT_palm_c.L')
    palmd = getBone(context, 'TGT_palm_d.L')

    palma.bone.layers = getLayers([0, 1])

    palma.rotation_mode = 'XYZ'
    palma.lock_rotation[1] = True

    palmb.rotation_mode = 'XYZ'
    palmb.lock_rotation[1] = True

    palmc.rotation_mode = 'XYZ'
    palmc.lock_rotation[1] = True

    palmd.rotation_mode = 'XYZ'
    palmd.lock_rotation[1] = True

    copyRot1 = palmb.constraints.new('COPY_ROTATION')
    copyRot1.target = arm
    copyRot1.subtarget = 'TGT_palm_a.L'
    copyRot1.target_space = 'LOCAL'
    copyRot1.owner_space = 'LOCAL'
    copyRot1.influence = 0.7

    copyRot2 = palmc.constraints.new('COPY_ROTATION')
    copyRot2.target = arm
    copyRot2.subtarget = 'TGT_palm_a.L'
    copyRot2.target_space = 'LOCAL'
    copyRot2.owner_space = 'LOCAL'
    copyRot2.influence = 0.3

    limRot = palma.constraints.new(type='LIMIT_ROTATION')
    limRot.use_limit_x = True
    limRot.use_limit_z = True
    limRot.owner_space = 'LOCAL'

    limRot.min_x = -0.523599
    limRot.max_x = 0.523599
    limRot.max_z = 0.523599
    limRot.min_z = 0


def set_up_finger_rig(context, fingerIndex):
    # print('fingerIndex', fingerIndex)

    arm = context.object
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    ebs = arm.data.edit_bones

    hand = getBone(context, 'TGT_hand.L')
    finger1 = getBone(context, 'TGT_finger_{}_1.L'.format(fingerIndex))
    finger2 = getBone(context, 'TGT_finger_{}_2.L'.format(fingerIndex))
    finger3 = getBone(context, 'TGT_finger_{}_3.L'.format(fingerIndex))

    ctrlFinger1 = ebs.new('CTRL_finger_{}_1.L'.format(fingerIndex))
    ctrlFinger1.use_deform = False
    ctrlFinger1.use_connect = False
    ctrlFinger1.head = finger1.head
    ctrlFinger1.tail = Vector((
        finger1.head[0] + (finger1.tail[0] - finger1.head[0]) * 1.5,
        finger1.head[1] + (finger1.tail[1] - finger1.head[1]) * 1.5,
        finger1.head[2] + (finger1.tail[2] - finger1.head[2]) * 1.5
    ))
    ctrlFinger1.parent = hand

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
        ctrlFinger1.tail[0] + (ctrlFinger1.tail[0] -
                               ctrlFinger1.head[0]) * 0.5,
        ctrlFinger1.tail[1] + (ctrlFinger1.tail[1] -
                               ctrlFinger1.head[1]) * 0.5,
        ctrlFinger1.tail[2] + (ctrlFinger1.tail[2] - ctrlFinger1.head[2]) * 0.5
    ))

    bpy.ops.armature.select_all(action='DESELECT')
    arm.data.edit_bones.active = ctrlFinger1
    ctrlFinger2.select = True
    bpy.ops.armature.align()

    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    finger1 = getBone(context, 'TGT_finger_{}_1.L'.format(fingerIndex))
    finger2 = getBone(context, 'TGT_finger_{}_2.L'.format(fingerIndex))
    finger3 = getBone(context, 'TGT_finger_{}_3.L'.format(fingerIndex))

    ctrlFinger1 = getBone(context, 'CTRL_finger_{}_1.L'.format(fingerIndex))
    ctrlFinger2 = getBone(context, 'CTRL_finger_{}_2.L'.format(fingerIndex))

    ctrlFinger1.rotation_mode = 'XYZ'
    ctrlFinger1.lock_rotation[1] = True
    ctrlFinger1.lock_rotation[2] = True

    ctrlFinger2.rotation_mode = 'XYZ'
    ctrlFinger2.lock_rotation[1] = True
    ctrlFinger2.lock_rotation[2] = True

    copyRot1 = finger1.constraints.new('COPY_ROTATION')
    copyRot1.target = arm
    copyRot1.subtarget = 'CTRL_finger_{}_1.L'.format(fingerIndex)
    copyRot1.target_space = 'LOCAL'
    copyRot1.owner_space = 'LOCAL'

    copyRot2 = finger2.constraints.new('COPY_ROTATION')
    copyRot2.target = arm
    copyRot2.subtarget = 'CTRL_finger_{}_2.L'.format(fingerIndex)
    copyRot2.target_space = 'LOCAL'
    copyRot2.owner_space = 'LOCAL'

    copyRot3 = finger3.constraints.new('COPY_ROTATION')
    copyRot3.target = arm
    copyRot3.subtarget = 'CTRL_finger_{}_2.L'.format(fingerIndex)
    copyRot3.target_space = 'LOCAL'
    copyRot3.owner_space = 'LOCAL'

    ctrlFinger1.bone.layers = getLayers([0, 1])
    ctrlFinger2.bone.layers = getLayers([0, 1])


def set_up_hand_rig(context):
    for fingerIndex in ['a', 'b', 'c', 'd', 'e']:
        set_up_finger_rig(context, fingerIndex)


def add_groups(context):
    arm = context.object
    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    leftArmGrp = arm.pose.bone_groups.new(name='left_arm')
    leftArmGrp.color_set = 'THEME01'
    
    rightArmGrp = arm.pose.bone_groups.new(name='right_arm')
    rightArmGrp.color_set = 'THEME04'

    for fingerIndex in ['a', 'b', 'c', 'd', 'e']:
        bone = getBone(context, 'CTRL_finger_{}_1.L'.format(fingerIndex))
        bone.bone_group = leftArmGrp
        bone = getBone(context, 'CTRL_finger_{}_2.L'.format(fingerIndex))
        bone.bone_group = leftArmGrp

    bone = getBone(context, 'TGT_palm_a.L')
    bone.bone_group = leftArmGrp
    bone = getBone(context, 'MCH_ik_arm.L')
    bone.bone_group = leftArmGrp
    bone = getBone(context, 'TGT_clavicle.L')
    bone.bone_group = leftArmGrp
    bone = getBone(context, 'MCH_ik_arm_target.L')
    bone.bone_group = leftArmGrp

    for fingerIndex in ['a', 'b', 'c', 'd', 'e']:
        bone = getBone(context, 'CTRL_finger_{}_1.R'.format(fingerIndex))
        bone.bone_group = rightArmGrp
        bone = getBone(context, 'CTRL_finger_{}_2.R'.format(fingerIndex))
        bone.bone_group = rightArmGrp

    bone = getBone(context, 'TGT_palm_a.R')
    bone.bone_group = rightArmGrp
    bone = getBone(context, 'MCH_ik_arm.R')
    bone.bone_group = rightArmGrp
    bone = getBone(context, 'TGT_clavicle.R')
    bone.bone_group = rightArmGrp
    bone = getBone(context, 'MCH_ik_arm_target.R')
    bone.bone_group = rightArmGrp

    leftLegGrp = arm.pose.bone_groups.new(name='left_leg')
    leftLegGrp.color_set = 'THEME01'

    bone = getBone(context, 'MCH_ik_leg.L')
    bone.bone_group = leftLegGrp
    bone = getBone(context, 'CTRL_foot_roll.L')
    bone.bone_group = leftLegGrp
    bone = getBone(context, 'MCH_ik_leg_target.L')
    bone.bone_group = leftLegGrp
    
    rightLegGrp = arm.pose.bone_groups.new(name='right_leg')
    rightLegGrp.color_set = 'THEME04'

    bone = getBone(context, 'MCH_ik_leg.R')
    bone.bone_group = rightLegGrp
    bone = getBone(context, 'CTRL_foot_roll.R')
    bone.bone_group = rightLegGrp
    bone = getBone(context, 'MCH_ik_leg_target.R')
    bone.bone_group = rightLegGrp
    
    torsoGroup = arm.pose.bone_groups.new(name='torso')
    torsoGroup.color_set = 'THEME03'

    bone = getBone(context, 'CTRL_hips')
    bone.bone_group = torsoGroup
    bone = getBone(context, 'CTRL_spine')
    bone.bone_group = torsoGroup
    bone = getBone(context, 'CTRL_torso')
    bone.bone_group = torsoGroup
    bone = getBone(context, 'TGT_neck')
    bone.bone_group = torsoGroup
    bone = getBone(context, 'TGT_head')
    bone.bone_group = torsoGroup
    bone = getBone(context, 'TGT_breast.L')
    bone.bone_group = torsoGroup
    bone = getBone(context, 'TGT_breast.R')
    bone.bone_group = torsoGroup



class FixSkeleton(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.fix_skeleton"
    bl_label = "Fix Skeleton"

    def execute(self, context):

        # TODO: revert file

        if context.object.type == 'ARMATURE':
            arm = context.object
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            arm.data.show_axes = True

            prepare_skeleton(context)

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
            prepare_single_bone(arm, rootBone)

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
            
            set_up_torso_rig(context)
            set_up_leg_rig(context)
            set_up_arm_rig(context)
            set_up_palm_rig(context)
            set_up_hand_rig(context)

            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.symmetrize()

            add_groups(context)

            # TODO fix deform in one function

            # test

            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            bpy.ops.object.select_all(action='DESELECT') 
            mesh = bpy.data.objects['basemesh.002']
            mesh.select_set(True)
            arm.select_set(True)
            bpy.context.view_layer.objects.active = arm 
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')

            bpy.ops.object.select_all(action='DESELECT') 
            arm.select_set(True)
            bpy.context.view_layer.objects.active = arm 
            bpy.ops.object.mode_set(mode='POSE', toggle=False)

            # turn on all layers
            # arm.data.layers = [n == 0 or n == 1 for n in range(0, 32)]
            
            # turn on only ctrl layer
            arm.data.layers = [n == 1 for n in range(0, 32)]

        return {'FINISHED'}


class CleanUp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.clean_skeleton"
    bl_label = "Clean Skeleton"

    def execute(self, context):
        if context.object.type == 'ARMATURE':
            arm = context.object
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)

            for b in arm.data.edit_bones:
                if b.name.startswith('TGT') or b.name.startswith('CTRL') or b.name.startswith('MCH'):
                    arm.data.edit_bones.remove(b)
                    continue

                if b.name.startswith('DEF') and b.name.endswith('.R'):
                    arm.data.edit_bones.remove(b)
                    continue

                b.name = b.name.lstrip('DEF_')
                b.name = b.name.lstrip('TGT_')
                b.name = b.name.rstrip('.L')
                b.name = b.name.rstrip('.R')

        bpy.ops.object.mode_set(mode='POSE', toggle=False)
        arm.data.layers = [n == 0 or n == 1 for n in range(0, 32)]

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        
        # TODO: remove groups
        # TODO: join arm?

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
