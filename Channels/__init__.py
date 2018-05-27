import Database as db
from Mud import mud


def send_to_channel(user, channel, msg, do_emote=False):
    """
    Handles messages to channels
    Checks the channel.type to build a list of recipients
    If the message contains the emote token (@), the emote text is built from the database,
    Message is sent to all recipients presenters
    """
    args = msg.split()

    if channel.type is 0:
        user_list = [user]
    elif channel.type is 1:
        user_list = mud.get_users()
    elif channel.type is 2:
        user_list = user.tile.occupants
    elif channel.type is 3:
        user_list = []
    elif channel.type is 4:
        user_list = [mud.get_user(args[0])]
        args = args[1:]
        msg = ' '.join(args)
        if msg[0] is '@':
            do_emote = True
            msg = msg[1:]
            args = msg.split()
    else:
        user_list = []

    if do_emote:
        if len(args) > 1:
            if args[1] == "self":
                vict = user
            else:
                vict = mud.get_user(args[1])
            if vict is None:
                user.p.send_text(f'{args[1]} doesn\'t appear to be here...')
                return
        else:
            vict = None
        emote = get_emote(args[0], user, vict)
        if emote is None:
            user.p.send_text("Emote not found.")
            return

        if vict is not None and vict is not user:
            others = [u for u in user_list if u is not user and u is not vict and channel.key in u.listening]
            msg_vict = emote['vict']
        else:
            others = [u for u in user_list if u is not user and channel.key in u.listening] if emote['others'] else None
        msg_user = emote['user']
        msg_others = emote['others']
    else:
        others = [u for u in user_list if u is not user and channel.key in u.listening]
        msg_user = 'You: ' + msg
        msg_others = user.name + ': ' + msg

    user.p.send_channel(channel, msg_user)
    if do_emote and vict is not None and vict is not user:
       vict.presenter.show_channel(channel, msg_vict)
    if others is not None:
        for other in others:
            other.p.send_channel(channel, msg_others)


def get_emote(emote, user, vict=None):
    """
    Gets an emote from the database, and returns a dict of the strings to be used for the user, victim and others
    """
    emote = db.session.query(db.models.Emote).filter_by(name=emote).first()
    if emote is None:
        return None
    # TODO: Add some User code for proper pronouns
    if vict is None:
        return {
            'user': emote.user_no_vict.format(user=user.name, vict='my'),
            'others': emote.others_no_vict.format(user=user.name, vict='them') if emote.others_no_vict is not None else None
        }
    elif vict is user:
        return {
            'user': emote.user_vict_self.format(user=user.name, vict='my') if emote.user_vict_self is not None else emote.user_no_vict.format(user=user.name),
            'others': emote.others_vict_self.format(user=user.name, vict='them') if emote.others_vict_self is not None else emote.others_no_vict.format(user=user.name)
        }

    else:
        return {
            'user': emote.user_vict.format(user=user.name, vict=vict.name) if emote.user_vict is not None else emote.user_no_vict.format(user=user.name),
            'others': emote.others_vict.format(user=user.name, vict=vict.name) if emote.others_vict is not None else emote.others_no_vict.format(user=user.name),
            'vict': emote.vict_vict.format(user=user.name, vict=vict.name) if emote.vict_vict is not None else None
        }

