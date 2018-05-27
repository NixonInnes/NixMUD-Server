import os
from Mud import mud


def do_look(user, args):
    """
    Display the users current tile information
    """
    user.p.send_tile(user.tile)


def do_who(user, args):
    """
    Display who is currently online
    """
    user.p.send_info_2col('ONLINE', ('User', ''), [(username, '') for username in mud.users])


def do_help(user, args):
    """
    Display a help file
    """
    default = 'Help/help.txt'
    if not args:
        help = default
    else:
        if isinstance(args, (list, tuple)):
            help = ' '.join(args)
        else:
            help = args
        help = 'Help/'+help+'.txt'
    if not os.path.isfile(help):
        user.p.send_text('Unable to find that help file, try just \'help\'')
        return
    with open(help) as f:
        help_text = f.read()
    user.p.send_help(help_text)