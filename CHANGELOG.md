# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
## [0.6.0] - 2022-10-1
### Deprecated
- Installation using install script (only docker install will be available in future versions)

### Added
- Full data validation for jobs configurations 

### Changed 
- Configuration data are stored in class instead of dictionary  

### Removed
- `Startup` configuration for api
- Separate configuration parameters for primary and failover answers

## [0.5.0] - 2022-09-05
### Added
- Domain name and answer auto validation
- Http response status code validation

## [0.4.1] - 2022-09-04
### Fixed
- Log-file setting finally work

## [0.4.0] - 2022-09-04
### Added
- Configuration option 'entry_exist'

## [0.3.1] - 2022-08-30
### Fixed
- Setting negative timeout of ping/http job will crash application
- Setting negative interval will crash application

### Changed
- Default config values are stored in separate file  
- Logs from http job are more consistent now

## [0.3.0] - 2022-08-29
### Added
- Static entry

## [0.2.0] - 2022-08-28
### Added
- New config section (named config) with options: wait, log_level, log_file
- Auto port for http_job
### Fixed
- App crashing when config file is empty

## [0.1.0] - 2022-08-28
First working release, program seems to work fine, but it's still in early alpha stage.
