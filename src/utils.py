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
    elif proto[-2:] == ":/":
        return proto + "/"
    elif proto[-1:] == ":":
        return proto + "//"
    else:
        return proto + "://"


def safe_parse_value(content, key, default_value):
        """
        Try to find a value assigned to key in dictionary, if key wasn't found return default value
        :param content: dict: a content to search in
        :param key: str: key to find
        :param default_value: default value in key wasn't found
        :return: value assigned to key, or default value
        """

        if key in content:
            return content[key]
        else:
            return default_value
