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



def parse_value_with_default(content, key, default_value):
    """
    Try to find a value assigned to key in dictionary, if key wasn't found return default value
    :param content: dict: a content to search in
    :param key: str: key to find
    :param default_value: default value in key wasn't found
    :return: value assigned to key, or default value, type of returned value is the same as type of default value
    """
    if content is None:
        return default_value
    if key in content:
        if content[key] is not None:
            return (type(default_value))(content[key])
        else:
            return default_value
    else:
        return default_value


def check_linux_permissions(permissions, target):
    """
    check linux permission are higher or equal to larger
    :param permissions: str: actual file or directory permissions
    :param target: str: targeted permissions
    :return: True if permission >= target, False in other cases
    """
    for char_permissions, char_target in zip(permissions, target):
        if char_permissions < char_target:
            return False
    return True
