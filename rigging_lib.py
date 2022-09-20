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
