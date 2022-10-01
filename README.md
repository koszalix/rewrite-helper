# Disclaimer
Program seems to work, but it's still in early alpha stage

# Rewrite helper
This is a program for managing DNS rewrites in [AdGuardHome](https://github.com/AdguardTeam/AdGuardHome). Main idea 
behind this software is to add failover functionality to dns rewrite.

## What is a dns rewrite failover
Basically [AdGuardHome](https://github.com/AdguardTeam/AdGuardHome) allows you to set custom dns answer for specific 
domain which is great, but sometimes we may want a little more redundancy. The easiest way to achieve that is to use  
for example server with two networks adapters or setup two exactly the same containers. Instead of having one dns 
rewrite entry, we set up two of them for example nas-1.lan, nas-2.lan. It seems to work ok, but in case of failure user 
need to manually change configuration. Sometimes it may be nearly impossible to change configuration manually on every
device, for example someone who have a ton of iot devices need to manually change configuration of every device which 
may be very time-consuming.  
To solve these problems dns rewrite failover come in. Basically this is a program which monitors hosts or service and if 
one of it is down dns answer will be changed to pointing on active host (or service). It highly recommended to have at 
least two AdGuardHome instances with two separate rewrite-helpers.

## How it works
Rewrite-helper monitors host (by pinging them or checking http status code) and interact with AdGuardHome api to ensure 
possibly the highest accessibility.


# Getting started

## Requirements:
 - python >= 3.10
 - pip
 - curl

## Automated install
Run the following command  in your terminal:
```sh
    curl -sSL https://raw.githubusercontent.com/koszalix/rewrite-helper/main/install.sh | sh
    systemctl daemon-reload
    systemctl enable rewrite-helper
    systemctl start rewrite-helper
```
Configuration is needed to run this software see [Configuration](#Configuration) section for more.

## Docker install
See [docker hub](https://hub.docker.com/repository/docker/koszalix/rewrite-helper#Quickstart) page for docker install quick start guide.

# Configuration
All configuration settings are stored in file: /etc/rewrite-helper/config.yml.    
If file 'config.yml' not exist or is not readable program will try to find
another '.yml' file, but it's highly recommended to keep settings in config.yml  

## Setting up api connection to [AdGuardHome](https://github.com/AdguardTeam/AdGuardHome).
Edit section named api:
```yaml
api:
  host: 
  port: 
  proto: 
  username: 
  passwd: 
  timeout: 
  startup:
```
`host` - ip or domain of adguardhome  
`proto` - communication protocol http or https  
`username` - admin username  
`passwd` - admin password  
`port` - connection port  
`timeout` - maximum time to response, if api request exceeded this time request wil be treated as fail   
`startup` - if set to `True` program don't start until connection can be established (connection will be tested every 10
            seconds)
## Configure miscellaneous software options
Add following section to config file
```yaml
config:
  wait:
  log_level:
  log_file:
  entry_exist:
```
`wait` - time in seconds to wait before programs start, setting this value may be helpful on system startup when 
         rewrite-helper starts faster than AdGuardHome  
`log_level` - set log level, available levels DEBUG, INFO, WARNING, ERROR, CRITICAL  
`log_file` - set log output file (full path)  
`entry_exist` - set what to do when domain is registered in AdGuardHome but answer don't match to any of answers 
                  from config file. Available options: 
                        KEEP - keep actual domain and add new, 
                        DROP - treat job as if it didn't exist
                        DELETE - delete existing domain, if for some reason domain wasn't deleted job will not be started
If log_level or log_file is no specified or value is incorrect program will read those parameters from cli.  
## Configuring jobs
Job is set of hosts IP addresses within one domain. When host to which IP address domain is pointing is down, then dns
answer will be changed to IP address of host with is up. 
### Configuring ping jobs
Ping job send ICMP pings to host, when host response is quicker than timeout host will be treated as live. Add following 
section to config file to set up ping job.
```yaml
ping_jobs:
  - job:
      domain:  
      interval: 
      count: 
      timeout: 
      privileged:
      answers:
        - <ip address>
        - <ip address>
```
`domain` - dns rewrite domain, for ex.: server.lan  
`interval` - seconds between tests.  
`count` - numer of packages send to host on each test.    
`timeout` - test timeout, if host is not responding after that time it will be treated as inaccessible.   
`priviledeg` - run ping request as superuser
`answers` - list of ip address with will be used as dns answers, first item from this list is prioritized see [Answers priority]

### Configuring http job
Http job gets status code of webpage, if received code is the same as configured host will be treated as live. 
Add following section to config file to set up http job. 
```yaml
http_jobs:
  - job:
      domain: 
      interval: 
      status: 
      proto: 
      port:
      timeout:
      answers:
          - <ip address>
          - <ip address>
```
`domain` - dns rewrite domain, for ex.: server.lan  
`interval` - seconds between tests.  
`status` - http response status code; if code received from host is the same as code provided in this settings host will be treated as live.  
`proto` - communication protocol (http or https)  
`port` - connection port  
`timeout` - test timeout, if host is not responding after that time it will be treated as inaccessible.  
`answers` - list of ip address with will be used as dns answers, first item from this list is prioritized see [Answers priority]


## Configuring static entry
In opposition to previous jobs, static entry do not test host accessibility instead static entry only check if dns 
rewrite exist in AdGuardHome, it not guaranties any kind of redundancy but may be usefully for devices like network 
printers, routers etc. To Configure static entry add following lines to configurations file.
```yaml
static_entry:
  - job:
      domain: 
      answer: 
      interval:
```
`domain` - dns rewrite domain  
`answer` - ip address assigned to domain  
`interval` - seconds between checks  

## Other information about configurations

### Answers priority 
All answers all prioritized, this mean if first host from list is accessible, dns answer will be set to this host 
(regardless of state of other hosts), if firs host is inaccessible but second host is accessible dns answer will be set 
to second hosts and so on.

#### Default ports
When there is no port configured but protocol is set to http default port will be 80, 
if protocol is set to https default will be 443

## Default values  
To make configuration easier some config option have assigned default values. To use default values of specific option
do not put this option to config file.

| Section     | Option       | Value | Section   | Option   | Value  |
|-------------|--------------|-------|-----------|----------|--------|
| api         | proto        | http  | http_jobs | interval | 60     |
| api         | port         | 80    | http_jobs | status   | 200    |
| api/startup | test         | True  | http_jobs | proto    | http   |
| api/startup | timeout      | 10    | http_jobs | port     | 80/443 |
| api/startup | exit_on_fail | False | ping_jobs | interval | 60     |
| api/startup | retry_after  | 10    | ping_jobs | timeout  | 2      |
| http_jobs   | timeout      | 10    | ping_jobs | count    | 2      |
 
## Auto correctness check
On start rewrite helper checks correctness of job parameters if correctness check fails job will not be added. 

## [See example config file](https://github.com/koszalix/rewrite-helper/blob/main/docs/templates/example_config.yml)




