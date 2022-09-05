import re
from _socket import inet_pton
from socket import AF_INET, AF_INET6


def check_ip_correctness(ip: str) -> bool:
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
            return False


def check_domain_correctness(domain: str) -> bool:
    """
    Check if domain is valid:
        1. contain only numbers, letters, hyphens or dot
        2. length <= 63 characters
        3. length of domain extension <= 4 characters
        4. don't start or end with dot or hyphens
        5. dot don't occur next to each others
    :param domain: domain to check
    :return: True if domain is valid, False if not
    """
    # contain only numbers, letters, hyphens or dot
    if re.search("[^\da-zA-Z.-]", domain) is not None:
        return False
    # start with dot or hyphen
    if re.search("^[.-]|[.-]$", domain) is not None:
        return False
    # length of domain extension
    if len(domain.split(".")[-1]) > 4:
        return False
    # dot don't occur next to each others, (only inside, if domain starts or end with dot previous if will cath catch)
    if re.search("[..]\B", domain) is not None:
        return False
    # length of domain
    if len(domain) > 63:
        return False

    return True
