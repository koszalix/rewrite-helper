# Rewrite-helper tests

# Running unit tests
0. Please read [#Test environment] section before.
1. Run `AdGuardVM`
2. Run `DummyHost_1` vm
3. Ensure if ip address of vm is correct (see [Notes about virtual machines](#Notes about virtual machines) )
4. Type following command
```bash
python3 -m unittest discover -t .
```
4. Goto [AdGuardHome vm](http://192.168.56.103/#dns_rewrites) webpage and check if there is no dns rewrite configured
   (excluding do-not.delete)

   
# Manual test
0. Please read [#Test environment] section before.
1. Run `AdGuardVM`, `DummyHost_1` and `DummyHost_2`
2. Check if dns-rewrite section is empty (excluding do-not.delete)
3. run program using (you must be in main program directory):
```bash
python3 ./main.py tests/manual/config.yml
```
4. Wait at least 2 minutes and check answers for domains dummy.ping, dummy.http, single.http, single.ping all domains
 should answer with 192.168.56.105.
5. Save `DummyHost_1`.
6. Wait a minute.
7. Check if answers of domain, for dummy.ping and dummy.http are 192.168.56.107 and answers for domains single.ping and 
   single.http is 192.168.56.107.
8. Run `DummyHost_1` again and wait at least 2 minutes
9. Check answers for domains dummy.ping, dummy.http, single.http, single.ping all domains should answer with 192.168.56.105.
10. Check if answer for domain static.lan is 192.168.56.1.
11. Delete entry static.lan and wait at least 2 minutes.
12. Check if entry mentioned in point 9 was added again.
13. Relaunch rewrite-helper and check if there aren't duplicated domains.
14. Shutdown rewrite-helper.
15. Delete all dns rewrites.
16. Save all machines.

# Test environment
To perform some test, extra steeps, such as setting file permissions or creating vm  must be taken. 

## Requirements
- [VirtualBox](https://www.virtualbox.org/)
- unittest

## Setting up test files
Almost all test files are downloaded from GitHub, but some files need to be set manually.
1. Ensure if you are in test directory (rewrite-helper/tests).
2. Run following commands, this script will create files and set permissions
```bash
    ./test_env/create_test_env.sh
```


## Creating virtual machines
1. Prepare 3 virtual machines with [Alpine Linux](https://alpinelinux.org/) or other distro if you like ;)
2. On two of them install a web server for ex: apache2 (see `install_web_server.sh` in test_env directory), from now
these VMs will be called `DummyHost_1` and `DummyHost_2`
3. On third machine install AdGuardHome, this machine is called `AdGuardVM` from now.
4. Make sure that `DummyHost_1` has ip address: 192.168.56.105, `DummyHost_1` has ip address: 192.168.56.107,
`AdGuardVm` has ip address 192.168.56.103.
5. Also check if you can ping those machines and access their web interfaces

