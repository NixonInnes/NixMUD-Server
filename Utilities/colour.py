TOKENS = {
    '&b': '\033[30m',  # black
    '&B': '\033[1;30m',  # bright-black
    '&r': '\033[31m',  # red
    '&R': '\033[1;31m',  # bright-red
    '&g': '\033[32m',  # green
    '&G': '\033[1;32m',  # bright-green
    '&y': '\033[33m',  # yellow
    '&Y': '\033[1;33m',  # bright-yellow
    '&u': '\033[34m',  # blue
    '&U': '\033[1;34m',  # bright-blue
    '&m': '\033[35m',  # magenta
    '&M': '\033[1;35m',  # bright-magenta
    '&c': '\033[36m',  # cyan
    '&C': '\033[1;36m',  # bright-cyan
    '&w': '\033[37m',  # white
    '&W': '\033[1;37m',  # bright-white
    '&x': '\033[0m'  # reset
}


def colourify(buf):
    """
    Replace colour tokens, defined in colour.TOKENS, in a body of text with their respective ASCII colour codes
    """
    for token in TOKENS:
        buf = buf.replace(token, TOKENS[token])
    return buf


def strip_tokens(buf):
    """
    remove all colour tokens, defined in colour.TOKENS, from a body of text
    """
    for token in TOKENS:
        buf = buf.replace(token, '')
    return buf
