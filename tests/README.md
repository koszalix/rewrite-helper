# Rewrite-helper tests


# Running tests
To run test, go to main project catalog and run:
```commandline
python3 -m unittest discover -t .
```

# Test environment
To perform some test, extra steeps, such as setting file permissions, creating vm  must be taken. 

## Create environment automagically
1. Ensure if you are in test directory (rewrite-helper/tests).
2. Run following commands
```bash
chmod +x ./create_test_env.sh
./create_test_env.sh
```

## Create environment manually
### Preparing environment for test: TestAnyYaml.test_no_permission()
Before run, ensure if there is a file named *config.yml* in directory *tests/unit/fixtures/config_files/any_yaml/no_permissions*.
This file must have 000 permission. This file is ignored by git (due to in insufficient permissions).

## Preparing environment for test: TestReadConfigFile.test_no_permission()
Before run, ensure if there is a file named *config.yml* in directory *tests/unit/fixtures/config_files/read_config_file/no_permissions*.
This file must have 000 permission. This file is ignored by git (due to in insufficient permissions).

## Preparing environment for test: TestReadConfigFile.test_file_is_a_directory()
Before run, ensure if directory test/unit/fixtures/config_files/read_config_file/a_directory exist, this directory should be empty.