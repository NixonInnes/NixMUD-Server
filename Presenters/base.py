class Presenter(object):
    """
    Base Presenter object, all other Presenters inherit from this
    Provides an object that transforms the data from the server/mud to a format the connected client wants
    i.e. text/json/http

    """
    def __init__(self, send_method):
        """
        Wraps the TCPHandler.send() method to Presenter.present()
        """
        self.present = send_method

    def send_text(self, msg):
        """
        Send a body of text to the client
        """
        raise NotImplementedError

    def send_tile(self, tile):
        """
        Send tile information to the client
        """
        raise NotImplementedError

    def send_info(self, title, header, info):
        """
        Send a block of information to the client
        """
        raise NotImplementedError

    def send_info_2col(self, title, header, info):
        """
        Send a block of information to the client, in the format of two columns
        """
        raise NotImplementedError

    def send_info_3col(self, title, header, info):
        """
        Send a block of information to the client, in the format of three columns
        """
        raise NotImplementedError

    def send_channel(self, channel, msg):
        """
        Send channel messages to the client
        """
        raise NotImplementedError

    def send_help(self, help_file):
        """
        Send help file information to the client
        """
        raise NotImplementedError