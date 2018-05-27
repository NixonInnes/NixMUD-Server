from Actions.info import do_help, do_look
from Entities.tile import Tile
from Entities.npc import NPC
from Mud import mud


def do_goto(user, args):
    """
    Move the user to the specified room, using the room name
    """
    if args is None:
        do_help(user, ['goto'])
        return
    tile_name = ' '.join(args).strip()
    dbTile = Tile.search(name=tile_name)
    if dbTile is None:
        user.p.send_text("Goto where?!")
        return
    user.move(dbTile)
    do_look(user, None)


def do_spawn(user, args):
    """
    Spawn a new NPC from the given name, in the same room as the user
    """
    if args is None:
        do_help(user, ['spawn'])
        return
    npc_name = ' '.join(args).strip()
    dbNPC = NPC.search(name=npc_name)
    if not dbNPC:
        user.p.send_text('Spawn a what?')
        return
    npc = NPC.load(dbNPC)
    npc.move(user.tile.db)
    user.p.send_text(f'You wave your hands erratically and suddenly a {npc.name} appears!')


def do_uinfo(user, args):
    """
    Display a specified users information
    """
    if not args or len(args) > 1:
        do_help(user, ['uinfo'])
        return
    target = mud.get_user(args[0])
    if not target:
        user.p.send_text(f'Unable to find {args[0]}')
        return
    user.p.send_info(
        title='User Info',
        header=target.name,
        info=[f'Name: {target.name}',
              f'ID: {target.model_id}',
              f'Flags: {target.flags}',
              f'Aliases: {target.aliases}',
              f'Race: {target.race.name}',
              f'Class: {target.class_.name}',
              f'Listening: {target.listening}',
              f'Tile: {target.tile.name}'
        ]
    )