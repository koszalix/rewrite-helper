# Disclaimer
This software is still in development


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
```commandline
    curl -sSL https://raw.githubusercontent.com/koszalix/rewrite-helper/main/install.sh | sh
    systemctl daemon-reload
    systemctl enable rewrite-helper
    systemctl start rewrite-helper
```
Configuration is needed to run this software see [Configuration](#Configuration) section for more.

## Docker install
See [docker hub](https://hub.docker.com/repository/docker/koszalix/rewrite-helper#Quickstart) page for docker install quick start guide.

# Configuration
Edit file /etc/rewrite-helper/config.yml.

## Setting up credentials to [AdGuardHome](https://github.com/AdguardTeam/AdGuardHome).
Edit section named api:
```yaml
  api:
    host: adguard.example.com
    port: 80
    proto: http
    username: admin
    passwd: admin
```
host - ip of adguardhome  
proto - communication protocol http or https  
username - admin username  
passwd - admin password  
port - connection port

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
      answers:
        primary: 
        failover:
          - <failover ip>
          - <failover ip>
```
domain - dns rewrite domain, for ex.: server.lan  
interval - seconds between tests.  
count - numer of packages send to host on each test.  
timeout - test timeout, if host is not responding after that time it will be treated as dead.  
primary - primary dns answer, this answer has the highest priority, 
failover - list of IP addresses to switch dns answer when primary host is down  

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
      answers:
        primary: 
        failover:
          - <failover ip>
          - <failover ip>
```
domain - dns rewrite domain, for ex.: server.lan  
interval - seconds between tests.  
status - if response code received from host is the same as this setting host will be treated as live.  
proto - communication protocol (http or https)  
primary - primary dns answer, this answer has the highest priority, 
failover - list of IP addresses to switch dns answer when primary host is down  

## [See example config file](https://github.com/koszalix/rewrite-helper/blob/main/templates/example_config.yml)



