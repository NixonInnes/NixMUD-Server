from Mud import mud


class NPCChannel(object):
    """
    Dummy channel object so Presenters have the same interface, and we don't have to store NPC channels in the
    database
    """
    def __init__(self, name, token):
        self.name = name
        self.token = token


INFO = NPCChannel('INFO', '&u')


def broadcast(msg):
    for user in mud.get_users():
        user.p.send_channel(INFO, msg)
