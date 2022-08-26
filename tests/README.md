# Test documentation
All additional information about tests will be added here.

# Running tests
To run test, go to main project catalog and run:
```commandline
python3 -m unittest discover -t .
```

# Test environment
To perform some test, extra steeps, such as setting file permissions, creating vm  must be taken. 

## Creating environment manually
### Preparing environment for TestAnyYaml.test_no_permission()
Before run, ensure if there is a file named *config.yml* in directory *tests/unit/fixtures/config_files/any_yaml/no_permissions*.
This file must have 000 permission. This file is ignored by git (due to in insufficient permissions).

## running TestReadConfigFile.test_no_permission()
Before run, ensure if there is a file named *config.yml* in directory *tests/unit/fixtures/config_files/read_config_file/no_permissions*.
This file must have 000 permission. This file is ignored by git (due to in insufficient permissions).

## running TestReadConfigFile.test_file_is_a_directory()
Before run, ensure if there is a directory test/unit/fixtures/config_files/read_config_file/a_directory