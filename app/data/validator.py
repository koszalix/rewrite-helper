import re
from _socket import inet_pton
from socket import AF_INET, AF_INET6


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
            return False


def validate_ips(ips: list) -> bool:
    """
    Check if provided ip addresses are valid
    :param ips:
    :return: True if address are valid, False if not
    """
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
    if re.search(r"[^a-zA-Z\d.-]", domain) is not None:
        return False
    # start with dot or hyphen
    if re.search(r"^[.-]|[.-]$", domain) is not None:
        return False
    # length of domain extension
    if len(domain.split(".")[-1]) > 4:
        return False
    # dots occur next to each others, (only inside, if domain starts or end with dot previous if will cath catch)
    if ('..' in domain) is True:
        return False
    # length of domain
    if len(domain) > 63:
        return False

    return True


def validate_network_port(port: int) -> bool:
    """
    Validate if port is from correct range
    :param port:
    :return: True if port is in range, False if not
    """
    if 0 <= port <= 65535:
        return True
    else:
        return False


def validate_http_response_code(code: int) -> bool:
    """
    Check if http response code correspond to any code defined in RFC7231(https://datatracker.ietf.org/doc/html/rfc7231)
    :param code:
    :return: True if code is valid http response code range, False if not
    """
    if 100 <= code < 600:
        return True
    return False


def validate_dns_rewrite(domain: str, primary_answer: str, failover_answers: list) -> bool:
    """
    Check if dns rewrite entry is valid.
    :param domain:
    :param primary_answer:
    :param failover_answers:
    :return: True if all everything is valid, False if not
    """
    if validate_domain(domain=domain) is False:
        return False
    elif validate_ip(ip=primary_answer) is False:
        return False
    else:
        for host in failover_answers:
            if validate_ip(host) is False:
                return False
        return True
