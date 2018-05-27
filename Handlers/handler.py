from Actions import ACTIONS
from Actions.user import do_move
from Channels import send_to_channel
from Mud import mud

COMPASS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'u', 'd']


class Handler(object):
    """
    Handler to parse basic human language commands received from the TCPHandler
    """
    def __init__(self, user):
        self.user = user

    def __call__(self, input):
        args = input.split()

        if not args:
            return

        if self.user.aliases and args[0] in self.user.aliases:
            args[0] = self.user.aliases[args[0]]
        msg = ' '.join(args)

        if len(args) is 1 and args[0].lower() in COMPASS:
            self.to_action(do_move, args[0])
            return

        if msg[0] in mud.channels:
            self.to_channel(mud.channels[msg[0]], msg[1:])
            return

        if args[0] in ACTIONS:
            self.to_action(ACTIONS[args[0]], args[1:] if len(args) > 1 else None)
            return

        self.user.p.send_text('Huh?')

    def to_channel(self, channel, msg):
        do_emote = False
        if msg[0] == '@':
            do_emote = True
            msg = msg[1:]
        send_to_channel(self.user, channel, msg, do_emote)

    def to_action(self, action, args):
        action(self.user, args)




