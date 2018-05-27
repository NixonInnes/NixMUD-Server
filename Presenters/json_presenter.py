from json import dumps

from Presenters.base import Presenter


class JSONPresenter(Presenter):
    def send_text(self, msg):
       self.present(dumps({'text': msg}))

    def send_tile(self, tile):
        self.present(dumps({
            'tile': {
                'name': tile.name,
                'coord': tile.coord,
                'description': tile.description,
                'plane': tile.plane.name,
                'properties': tile.properties
            }
        }))

    def send_info(self, title, header, info):
        self.present(dumps({
            'info': {
                'title': title,
                'header': header,
                'info': info
            }
        }))

    def send_info_2col(self, title, header, info):
        self.present(dumps({
            'info_2col': {
                'title': title,
                'header1': header[0],
                'info1': info[0],
                'header2': header[1],
                'info2': info[1]
            }
        }))

    def send_info_3col(self, title, header, info):
        self.present(dumps({
            'info_3col': {
                'title': title,
                'header1': header[0],
                'info1': info[0],
                'header2': header[1],
                'info2': info[1],
                'header3': header[2],
                'info3': info[2]
            }
        }))

    def send_channel(self, channel, msg):
        self.present(dumps({
            'channel': {
                'channel': channel.name,
                'msg': msg
            }
        }))

    def send_help(self, help_file):
        with open(help_file, 'r') as f:
            msg = f.read()
        self.present(dumps({'text': msg}))
