#!/bin/bash
if [ ! -d "./unit/fixtures/config_files/any_yaml/no_permissions" ]
then
  mkdir "./unit/fixtures/config_files/any_yaml/no_permissions"
fi

if [ ! -d "./unit/fixtures/config_files/read_config_file/no_permissions" ]
then
  mkdir ./unit/fixtures/config_files/read_config_file/no_permissions
fi

if [ ! -d "./unit/fixtures/config_files/read_config_file/a_directory" ]
then
  mkdir ./unit/fixtures/config_files/read_config_file/a_directory
fi

chmod 000 unit/fixtures/config_files/any_yaml/no_permissions
chmod 000 unit/fixtures/config_files/read_config_file/no_permissions