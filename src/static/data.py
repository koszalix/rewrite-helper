"""
Stores default configuration values, if you change any of these values change test case too
"""
# api
class Api:
    proto = "http"
    port = 80

    class Startup:
        test = True
        timeout = 10
        exit_on_false = False
        retry_after = 10

# ping jobs
class PingJob:
    interval = 60
    count = 2
    timeout = 2

# http job
class HttpJob:
    timeout = 10
    interval = 60
    status = 200
    proto = "http"

