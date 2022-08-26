# Test documentation
All additional information about tests will be added here.

# Running tests
To run test, go to main project catalog and run:
```commandline
python3 -m unittest discover -t .
```

# Additional action needed to run test completely 
## running TestAnyYaml.test_no_permission()
Before run, ensure if there is a file in directory tests/unit/fixtures/config_files/any_yaml/no_permissions.
This file must have 000 permission, manual check is needed because git can't work without permission to open file and 
this file can't be pushed to GitHub.

## running TestReadConfigFile.test_no_permission()
Before run, ensure if there is a file in directory tests/unit/fixtures/config_files/read_config_file/no_permissions.
This file must have 000 permission, manual check is needed because git can't work without permission to open file and 
this file can't be pushed to GitHub.

## running TestReadConfigFile.test_file_is_a_directory()
Before run, ensure if there is a directory test/unit/fixtures/config_files/read_config_file/a_directory