"""
Miscellaneous method and classes used by other parts of program
"""


def check_protocol_slashed(proto=""):
    """
    Check if provided protocol have slashes at the end, if not stick it.
    For example:
        proto = http:// -> return http://
        proto = http -> return http://
    :param proto:
    :return: str: protocol with slashes
    """
    if proto[-3:] == "://":
        return proto
    else:
        return proto + "://"
