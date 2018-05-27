from Mud.ticker import make_tick


def do_dance(user, args):
    def dance(user):
        user.p.send_text('You are performing a mighty jig!')
        for u in user.tile.occupants:
            if u is user:
                continue
            u.p.send_text(f'{user.name} flails their legs around in what appears to be some kind of dance.')
    tick = make_tick(interval=5, func=dance, repeat=True, args=[user])
    user.ticks.append(tick)
    tick.start()


def do_stop(user, args):
    user.stop_ticks()
    user.p.send_text('You cease all dancing related activities.')