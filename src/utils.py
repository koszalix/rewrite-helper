"""
Miscellaneous method and classes used by other parts of program
"""
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
import re


def parse_logging_level(logging_str):
    """
    Convert loging level as string to logging object
    :param logging_str: str: logging level
    :return: logging level object (if possible) or False if can't match level
    """
    if logging_str == "DEBUG":
        return DEBUG
    elif logging_str == "INFO":
        return INFO
    elif logging_str == "WARNING":
        return WARNING
    elif logging_str == "ERROR":
        return ERROR
    elif logging_str == "CRITICAL":
        return CRITICAL
    else:
        return False


def check_protocol_slashed(proto=""):
    """
    Check if provided protocol have slashes at the end, if not stick it.
    For example:
        proto = http:// -> return http://
        proto = http -> return http://
    :param proto:
    :return: str: protocol with slashes
    """
    if len(proto) == 0:
        return ""
    elif proto[-3:] == "://":
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


def check_linux_permissions(permissions: str, target: str):
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


def match_port_to_protocol(proto: str, default_port=80):
    """
    Match port for protocol
    :param proto: protocol to find port
    :param default_port: port returned when proto wasn't found
    :return: matched port or default port
    """
    protocols_and_ports = {
        'http': 80,
        'https': 443,
    }
    if proto in protocols_and_ports:
        return protocols_and_ports[proto]
    else:
        return default_port


def check_domain_correctness(domain: str) -> bool:
    """
    Check if domain is valid:
        1. contain only numbers, letters, hyphens or dot
        2. length <= 63 characters
        3. length of domain extension <= 4 characters
        4. don't start or end with dot or hyphens
        5. dot is surrounded by letters or numbers
    :param domain: domain to check
    :return: True if domain is valid, False if not
    """
    # start with dot or hyphen
    if re.search("^[.-]|[.-]$", domain) is not None:
        return False
    # length of domain extension
    if len(domain.split(".")[-1]) > 4:
        return False
    # length of domain
    if len(domain) > 63:
        return False

    return True


def check_ip_correctness(ip: str) -> bool:
    pass
