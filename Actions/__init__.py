from Actions import admin, combat, info, tiles, user


ACTIONS = {
    'alias': user.do_alias,
    'dance': combat.do_dance,
    'dig': tiles.do_dig,
    'goto': admin.do_goto,
    'help': info.do_help,
    'look': info.do_look,
    'save': user.do_save,
    'spawn': admin.do_spawn,
    'stop': combat.do_stop,
    'quit': user.do_quit,
    'who': info.do_who,
}