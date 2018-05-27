from textwrap import wrap

from Presenters.base import Presenter
from Utilities.colour import colourify


class TextPresenter(Presenter):
    def send(self, buf):
        self.present(colourify(buf))

    def send_text(self, buf):
        self.send(buf)

    def send_tile(self, tile):
        buff = "&y.-~~~~~~~~~~~~~~~~~~~~~~~~~~&Y{{&W {:^20} &Y}}&x&y~~~~~~~~~~~~~&Y[&w{:^3}&y,&w{:^3}&y,&w{:^3}&Y]&x&y-.&x\r\n".format(
            tile.name, tile.x, tile.y, tile.z)
        buff += "&y:                                                                              &y:&x\r\n"
        desc = wrap(tile.description, width=72)
        for line in desc:
            buff += "&y:&x   {:<72}   &y:&x\r\n".format(line)
        buff += "&y:                                                                              &y:&x\r\n"
        occs = ', '.join([user.name for user in tile.occupants])
        occs = wrap(occs, width=76)
        for line in occs:
            buff += "&Y#[&x {:<74} &Y]#&x\r\n".format(line)
        exits = ', '.join([ex.upper() for ex in tile.exits.keys()])
        buff += "&Y#============&y[&w Exits: {:<43} &y]&x&Y============#&x\r\n".format(exits)
        self.send(buff)

    def send_info(self, title, header, info):
        buf = "&c||##########################&C[&x &W{:^20}&x &C]&x&c##########################||&x\r\n".format(title)
        buf += BLANK_80
        buf += "&c||&x {:^74} &c||&x\r\n".format(header)
        buf += ROW_LINE_80
        buf += BLANK_80
        for row in info:
            buf += "&c||&x {:^74} &c||&x\r\n".format(row)
        buf += BLANK_80
        buf += FOOTER_80
        self.send(buf)

    def send_info_2col(self, title, header, info):
        buf = "&c||##########################&C[&x &W{:^20}&x &C]&x&c##########################||&x\r\n".format(title)
        buf += BLANK_80
        buf += "&c||&x {:^35} &c||&x {:^35} &c||&x\r\n".format(header[0], header[1])
        buf += ROW_LINE_80
        buf += BLANK_80
        for row in info:
            buf += "&c||&x {:^35} &c||&x {:^35} &c||&x\r\n".format(row[0], row[1])
        buf += BLANK_80
        buf += FOOTER_80
        self.send(buf)

    def send_info_3col(self, title, header, info):
        buf = "&c||##########################&C[&x &W{:^20}&x &C]&x&c##########################||&x\r\n".format(title)
        buf += BLANK_80
        buf += "&c||&x {:^22} &c||&x {:^22} &c||&x {:^22} &c||&x\r\n".format(header[0], header[1], header[2])
        buf += ROW_LINE_80
        buf += BLANK_80
        for row in info:
            buf += "&c||&x {:^22} &c||&x {:^22} &c||&x {:^22} &c||&x\r\n".format(row[0], row[1], row[2])
        buf += BLANK_80
        buf += FOOTER_80
        self.send(buf)

    def send_channel(self, channel, msg):
        self.send("&W[&x{}{}&x&W]&x {}{}&x".format(channel.token, channel.name, channel.token, msg))

    def send_help(self, msg):
        self.send(msg)

########################################################################################################################
# Additional functions

FOOTER_80 = "&c||############################################################################||&x\r\n"
BLANK_80 = "&c||                                                                            ||&x\r\n"
ROW_LINE_80 = "&c||============================================================================||&x\r\n"
BLANK_2COL_80 = "&c||                                     ||                                     ||&x\r\n"
ROW_LINE_2COL_80 = "&c||=====================================||=====================================||&x\r\n"
BLANK_3COL_80 = "&c||                        ||                        ||                        ||&x\r\n"
ROW_LINE_3COL_80 = "&c||========================||========================||========================||&x\r\n"

FOOTER_40 = "&c||####################################||&x\r\n"
BLANK_40 = "&c||                                    ||&x\r\n"
ROW_LINE_40 = "&c||====================================||&x\r\n"
BLANK_2COL_40 = "&c||                 ||                 ||&x\r\n"
ROW_LINE_2COL_40 = "&c||=================||=================||&x\r\n"


def header_40(title):
    buf = "&c||###########&C[&x &W{:^10}&x &C]&x&c###########||&x\r\n".format(title)
    buf += BLANK_40
    return buf


def body_40(string, align='center'):
    if align == 'left':
        buf = "&c||&x {:<34} &c||&x\r\n".format(string)
    elif align == 'right':
        buf = "&c||&x {:>34} &c||&x\r\n".format(string)
    else:  # center
        buf = "&c||&x {:^34} &c||&x\r\n".format(string)
    return buf


def body_2cols_40(stringA, stringB):
    buf = "&c||&x {:^14} &c||&x {:^14} &c||&x\r\n".format(stringA, stringB)
    return buf