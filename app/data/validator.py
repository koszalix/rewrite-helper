import logging
import re
from _socket import inet_pton
from socket import AF_INET, AF_INET6
from typing import Union


def validate_ip(ip: str) -> bool:
    """
    Check if provided ip address is valid ipv4 or ipv6.
    :param ip:
    :return: True if address is valid, False if not
    """
    try:
        inet_pton(AF_INET, ip)
        return True
    except OSError:
        try:
            inet_pton(AF_INET6, ip)
            return True
        except OSError:
            logging.warning(msg="IP address is not valid (not ipv4 or ipv6)")
            return False


def validate_ips(ips: Union[list, str]) -> bool:
    """
    Check if provided ip addresses are valid
    :param ips:
    :return: True if address are valid, False if not
    """
    if type(ips) == str:
        return validate_ip(ip=ips)
    if len(ips) <= 0:
        return False
    for adr in ips:
        if validate_ip(ip=adr) is False:
            return False
    else:
        return True


def validate_domain(domain: str) -> bool:
    """
    Check if domain is valid:
        1. contain only numbers, letters, hyphens or dot
        2. length <= 63 characters
        3. length of domain extension <= 4 characters
        4. don't start or end with dot or hyphens
        5. dots don't occur next to each others
    :param domain: domain to check
    :return: True if domain is valid, False if not
    """
    # contain only numbers, letters, hyphens or dot
    if type(domain) is not str or re.search(r"[^a-zA-Z\d.-]", domain) is not None:
        logging.warning(msg="Domain is not valid (not allowed chars)")
        return False
    # start with dot or hyphen
    if re.search(r"^[.-]|[.-]$", domain) is not None:
        logging.warning(msg="Domain is not valid (start with dot or hyphen)")
        return False
    # length of domain extension
    if len(domain.split(".")[-1]) > 4:
        logging.warning(msg="Domain is not valid (length of domain extension)")
        return False
    # dots occur next to each others, (only inside, if domain starts or end with dot previous if will cath catch)
    if ('..' in domain) is True:
        logging.warning(msg="Domain is not valid (dots occur next to each others)")
        return False
    # length of domain
    if len(domain) > 63:
        logging.warning(msg="Domain is not valid (domain to long)")
        return False

    return True


def validate_network_port(port: int) -> bool:
    """
    Validate if port is from correct range
    :param port:
    :return: True if port is in range, False if not
    """
    if type(port) is not int or port < 0 or port > 65536:
        logging.warning(msg="Port is not valid (out of range)")
        return False

    return True


def validate_http_response_code(code: int) -> bool:
    """
    Check if http response code correspond to any code defined in RFC7231(https://datatracker.ietf.org/doc/html/rfc7231)
    :param code:
    :return: True if code is valid http response code range, False if not
    """
    if type(code) is not int or code < 100 or code >= 600:
        logging.warning(msg="Http response code is not valid (out of range)")
        return False
    return True


def validate_timeout(timeout: Union[int, float], gt=0.01) -> bool:
    """
    Check if request timeout is valid (>= 0)
    :param timeout: timeout to check
    :param gt: if timeout is lower than that value -> timeout is not valid
    :return: True if timeout is valid, False if not
    """
    if (type(timeout) is not int and type(timeout) is not float) or timeout < gt:
        logging.warning(msg="Timeout is not valid (value to low)")
        return False

    return True


def validate_ping_count(count: int) -> bool:
    """
    Check if number of request made by icmp ping is correct
    :param count: number of request send by icmp ping
    :return: True if correct, False if not
    """
    if type(count) is not int or count <= 0:
        logging.warning(msg="Ping count is not valid (value to low)")
        return False

    return True


def validate_interval(interval: int) -> bool:
    """
    Check if job interval have a correct value
    :param interval: job interval
    :return: True if interval is correct False if not
    """
    if type(interval) is not int or interval < 1:
        logging.warning(msg="Interval is not valid (interval must be greater or equal to one)")
        return False
    else:
        return True


def validate_proto(proto: str) -> bool:
    """
    Check if protocol is valid
    :param proto:
    :return:
    """
    if type(proto) is not str or re.search(r"[^a-zA-Z/:]", proto):
        logging.warning(msg="Proto is not valid (not allowed chars)")
        return False
    elif proto == "":
        logging.warning(msg="Proto is not valid (empty)")
        return False
    else:
        return True
