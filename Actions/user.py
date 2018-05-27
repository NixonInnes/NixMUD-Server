import re
from Actions.info import do_look
from Actions.admin import do_goto
from Channels.npc import broadcast
from Entities.user import User
from Utilities import defaults


def do_quit(user, args):
    """
    Disconnect from the server
    """
    user.p.send_text('You are wracked with an uncontrollable pain as you are extracted from the Matrix.')
    broadcast(f'{user.name} has left the realm.')
    user.disconnect()


def do_save(user, args):
    """
    Save user properties to the database
    """
    user.p.send_text('Saving...')
    user.save()


def do_move(user, args):
    """
    Move the user in a specified direction
    """
    direction = getattr(user.tile.db, args, None)
    if direction:
        user.move(direction)
        do_look(user, None)
        return
    user.p.send_text('There doesn\'t apppear to be an exit in that direction!')


def do_alias(user, args):
    """
    Create or delete aliases for the user.
    """
    if args is None:
        header = 'My Aliases'
        info = []
        for alias, text in user.aliases.items():
            info.append(f'{alias}: {text}')
        user.p.send_info('ALIASES', header, info)
        return

    if args[0] == 'delete' and len(args) > 1:
        if args[1] in user.user.aliases:
            user.aliases.pop(args[1])
            user.p.send_text(f'Alias "{args[1]}" has been deleted.')
            return
        user.p.send_text(f'You have no "{args[1]}" alias.')
        return

    alias = args[0]
    text = ' '.join(args[1:])
    if alias == 'alias':
        user.send('That\'s not a good idea...')
        return
    user.aliases[alias] = text
    user.p.send_text(f'Alias "{alias}" for "{text}" created.')