# Rewrite-helper tests

# Running unit tests
1. Run AdGuardHome vm 
2. Ensure if ip address of vm is correct (see [Notes about virtual machines](#Notesaboutvirtualmachines) )
3. Type following command
```bash
python3 -m unittest discover -t .
```
4. Goto [AdGuardHome vm](http://192.168.56.103/#dns_rewrites) webpage and check if there is no dns rewrite configured.

Some test needs virtual machines or special files, please read [Test environment](#Testenvironment) and 
[Notes about virtual machines](#Notesaboutvirtualmachines) section before 
running test.  


# Test environment
To perform some test, extra steeps, such as setting file permissions, creating vm  must be taken. 

## Requirements
- [VirtualBox](https://www.virtualbox.org/)
- unittest

## Create environment automagically
1. Ensure if you are in test directory (rewrite-helper/tests).
2. Ensure you have VirtualBox installed
3. Run following commands, this script will create directories and attach vms
```bash
chmod +x ./create_test_env.sh
./create_test_env.sh
```
4. Go to VirtualBox 
5. Open File->Host Network Manager
6. Change ip range of vboxnet0 to 192.168.56.1/24
7. Ensure if vm named AdGuardHome have network adapter 1 set to vboxnet0
8. In case when changing ip range of vboxnet0 is impossible, change ip settings in tests/unit/test_ApiConnection.py

## Create environment manually
### Preparing environment for test: TestAnyYaml.test_no_permission()
Before run, ensure if there is a file named *config.yml* in directory *tests/unit/fixtures/config_files/any_yaml/no_permissions*.
This file must have 000 permission. This file is ignored by git (due to in insufficient permissions).

### Preparing environment for test: TestReadConfigFile.test_no_permission()
Before run, ensure if there is a file named *config.yml* in directory *tests/unit/fixtures/config_files/read_config_file/no_permissions*.
This file must have 000 permission. This file is ignored by git (due to in insufficient permissions).

### Preparing environment for test: TestReadConfigFile.test_file_is_a_directory()
Before run, ensure if directory test/unit/fixtures/config_files/read_config_file/a_directory exist, this directory should be empty.

### Download and install AdGuardHome vm

# Notes about virtual machines
## AdGuardHome 
IP address 192.168.56.103  
Web interface port 80  
Username admin  
Password 12345678  
Vm username root  
Vm password 12345678iQ  