"""
Stores default configuration values, if you change any of these values change test case too
"""


class Api:
    proto = "http"
    port = 80
    timeout = 10

    class Startup:
        test = True
        timeout = 10
        exit_on_false = False
        retry_after = 10


class Config:
    wait = 0
    log_level = False
    log_file = "N/A"
    entry_exist = 'KEEP'

class PingJob:
    interval = 60
    count = 2
    timeout = 2


class HttpJob:
    timeout = 10
    interval = 60
    status = 200
    proto = "http"
    port = 80


class StaticEntry:
    interval = 60
