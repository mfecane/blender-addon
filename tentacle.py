import bpy
from . import rigging_lib

getBone = rigging_lib.getBone
getLayers = rigging_lib.getLayers


config = {
    'steps': 4
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


def copyArmature(armature):
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    rootBone = None
    for b in armature.data.edit_bones:
        if not b.parent:
            if b.name.startswith('TGT'):
                raise NameError('Target bones not removed')

            if rootBone:
                raise NameError('Multiple root bones')

            rootBone = b
    copy = bpy.data.armatures.new('tree')
    copyObject = bpy.data.objects.new('treeArm', copy)
    bpy.context.scene.collection.objects.link(copyObject)
    bpy.context.view_layer.objects.active = copyObject
    copyObject.show_axis = True
    copyObject.show_in_front = True
    readBone(armature, copyObject, rootBone, None)
    return copyObject


def readBone(armature, copy, bone, parent):
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    copyBone = copy.data.edit_bones.new('DEF_' + bone.name)
    if parent != None:
        copyBone.parent = parent
    copyBone.tail = bone.tail
    copyBone.head = bone.head

    bone.hide = False
    if parent:
        copyBone.matrix = bone.matrix.copy()
        copyBone.use_connect = True
    for b in bone.children:
        readBone(armature, copy, b, copyBone)


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
    ctrlBoneName = ''

    parentName = ''
    parentBone = None
    if editBone.parent:
        parentName = editBone.parent.name
        parentBone = getBone(arm, parentName)

    if index % config['steps'] == 0:
        ctrlBoneName = 'CTRL' + str(index)
        ctrlBone = arm.data.edit_bones.new(ctrlBoneName)
        ctrlBone.tail = editBone.tail
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

    if not ctrlBone and parentName:
        poseParent = getBone(arm, parentName)
        copyRot = poseBone.constraints.new('COPY_ROTATION')
        copyRot.target = arm
        copyRot.subtarget = poseParent.name
        copyRot.target_space = 'LOCAL'
        copyRot.owner_space = 'LOCAL'
        copyRot.mix_mode = 'BEFORE'

    if ctrlBone:
        ctrlBone = getBone(arm, ctrlBoneName)
        ctrlBone.rotation_mode = 'XYZ'

        copyRot2 = poseBone.constraints.new('COPY_ROTATION')
        copyRot2.target = arm
        copyRot2.subtarget = ctrlBoneName
        copyRot2.target_space = 'LOCAL'
        copyRot2.owner_space = 'LOCAL'
        copyRot2.mix_mode = 'BEFORE'

        if parentName:
            poseParent = getBone(arm, parentName)
            copyRot = ctrlBone.constraints.new('COPY_ROTATION')
            copyRot.target = arm
            copyRot.subtarget = poseParent.name
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
    rootBone = None
    for b in arm.data.edit_bones:
        if not b.parent:
            if rootBone:
                raise NameError('Multiple root bones')
            rootBone = b

    set_up_tentacle_bone(arm, rootBone.name, 0)
    set_up_groups(arm)


class TentacleRig(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mfecane_tools.tentacle_rig"
    bl_label = "Tentacle rig"

    def execute(self, context):

        if context.object.type == 'ARMATURE':
            arm = copyArmature(context.object)
            # bpy.context.view_layer.layer_collection.children.get(context.object.name).hide_viewport = True
            # bpy.context.view_layer.layer_collection.children.get(context.object.name).hide_viewport = True
            set_up_tentacle(arm)

        return {'FINISHED'}
