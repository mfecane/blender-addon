import bpy
from mathutils import Vector
from math import floor
from . import rigging_lib

getBone = rigging_lib.getBone
getLayers = rigging_lib.getLayers


config = {
    'boneCount': 7,
    'steps': 6
}


def getBone(arm, name):
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


def getBoneLengths():
    boneCount = config['boneCount']
    boneLengths = []
    totalzig = 0
    for idx in range(boneCount):
        revIndex = boneCount - idx
        resSize = revIndex * revIndex
        boneLengths.append((resSize, floor((4 + revIndex / 1.5))))
        totalzig += resSize

    for idx in range(boneCount):
        boneLengths[idx] = (boneLengths[idx][0] / totalzig, boneLengths[idx][1])

    return boneLengths


def createArmature(armature):
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

    baseBone = None
    head = Vector()
    tail = Vector()
    for b in armature.data.edit_bones:
        baseBone = b
        head = baseBone.head
        tail = baseBone.tail

    copy = bpy.data.armatures.new('tree')
    copyObject = bpy.data.objects.new('treeArm', copy)
    bpy.context.scene.collection.objects.link(copyObject)
    bpy.context.view_layer.objects.active = copyObject
    copyObject.show_in_front = True
    copyObject.data.display_type = 'BBONE'
    copyObject.data.show_axes = True
    copyObject.data.axes_position = 1


    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

    rootBone = copyObject.data.edit_bones.new('Root')
    rootBone.head = Vector((0.0, 0.0, 0.0))
    rootBone.tail = Vector((0.0, 1.0, 0.0))
    rootBone.use_deform = False

    prevBone = rootBone
    boneCount = config['boneCount']

    # stupid length generation
    boneLengths = getBoneLengths()

    for idx in range(boneCount):
        copyBone = copyObject.data.edit_bones.new('DEF_Bone' + str(idx))
        copyBone.parent = prevBone
        if prevBone.name != 'Root':
            copyBone.head = prevBone.tail
            copyBone.use_connect = True
        else:
            copyBone.head = head
        copyBone.tail = copyBone.head + (tail - head) * boneLengths[idx][0]
        prevBone = copyBone
        copyBone.bbone_segments = boneLengths[idx][1]


    copyObject
    return copyObject


def set_up_groups(arm):
    bpy.ops.object.mode_set(mode='POSE', toggle=False)

    g1 = arm.pose.bone_groups.new(name='def')
    g1.color_set = 'THEME01'

    g2 = arm.pose.bone_groups.new(name='ctrl')
    g2.color_set = 'THEME04'

    for b in arm.pose.bones:
        if b.name.startswith('DEF'):
            b.bone_group = g1
        else:
            b.bone_group = g2


def set_up_tentacle_bone(arm, boneName, index):
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    editBone = getBone(arm, boneName)
    ctrlBone = None
    ctrlBoneName = 'CTRL' + str(index)
    parentName = ''
    parentBone = None

    if editBone.parent:
        parentName = editBone.parent.name
        parentBone = getBone(arm, parentName)

    ctrlBone = arm.data.edit_bones.new(ctrlBoneName)
    vec = editBone.head - editBone.tail
    vec.normalize()
    ctrlBone.tail = editBone.head + vec
    ctrlBone.head = editBone.head
    if parentBone:
        ctrlBone.parent = parentBone
    ctrlBone.use_deform = False
    ctrlBone.use_connect = False
    ctrlBone.matrix = editBone.matrix.copy()
    ctrlBone.layers = getLayers([0, 1])

    bpy.ops.object.mode_set(mode='POSE', toggle=False)
    poseBone = getBone(arm, boneName)
    poseBone.rotation_mode = 'XYZ'

    ctrlBone = getBone(arm, ctrlBoneName)
    ctrlBone.rotation_mode = 'XYZ'

    copyRot2 = poseBone.constraints.new('COPY_ROTATION')
    copyRot2.target = arm
    copyRot2.subtarget = ctrlBoneName
    copyRot2.target_space = 'LOCAL'
    copyRot2.owner_space = 'LOCAL'
    copyRot2.mix_mode = 'BEFORE'

    if parentName and parentName != 'Root':
        poseParent = getBone(arm, parentName)
        copyRot = ctrlBone.constraints.new('COPY_ROTATION')
        copyRot.target = arm
        copyRot.subtarget = parentName
        copyRot.target_space = 'LOCAL'
        copyRot.owner_space = 'LOCAL'
        copyRot.mix_mode = 'BEFORE'

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    child = None
    for b in arm.data.edit_bones:
        if b.parent and b.parent.name == boneName and b.name.startswith('DEF'):
            child = b

    if child:
        index = index + 1
        set_up_tentacle_bone(arm, child.name, index)


def set_up_tentacle(arm):
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    rootBone = None
    for b in arm.data.edit_bones:
        if not b.parent:
            if rootBone:
                raise NameError('Multiple root bones')
            rootBone = b
    set_up_tentacle_bone(arm, rootBone.name, 0)

    # set up last bone
    lastBoneName = 'DEF_Bone' + str(config['boneCount'] - 1)
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    lastBone = getBone(arm, lastBoneName)
    ctrlBone = arm.data.edit_bones.new('CTRL_Tip')
    ctrlBone.matrix = lastBone.matrix.copy()
    ctrlBone.head = lastBone.tail
    vec = lastBone.tail - lastBone.head
    vec.normalize()
    ctrlBone.tail = lastBone.tail + vec
    ctrlBone.parent = lastBone
    ctrlBone.use_deform = False
    ctrlBone.use_connect = True

    bpy.ops.object.mode_set(mode='POSE', toggle=False)
    ctrlBone = getBone(arm, 'CTRL_Tip')
    lastBone = getBone(arm, lastBoneName)

    copyRot = ctrlBone.constraints.new('COPY_ROTATION')
    copyRot.target = arm
    copyRot.subtarget = lastBone.name
    copyRot.target_space = 'LOCAL'
    copyRot.owner_space = 'LOCAL'
    copyRot.mix_mode = 'BEFORE'

    set_up_groups(arm)
    
    # set transforms to local
    bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'

class TentacleRig(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.tentacle_rig"
    bl_label = "Tentacle rig"

    def execute(self, context):

        if context.object.type == 'ARMATURE':
            arm = context.object
            # arm = copyArmature(context.object)
            copy = createArmature(arm)
            # TODO ::: figure this this out
            # bpy.context.view_layer.layer_collection.children.get(context.object.name).hide_viewport = True
            # bpy.context.view_layer.layer_collection.children.get(context.object.name).hide_viewport = True
            set_up_tentacle(copy)

        return {'FINISHED'}
