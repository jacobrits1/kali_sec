# Changelog

## [1.0.0] - 2024-01-XX

### Added
- Initial release of Kali Docker Automation script
- Supabase integration for action management
- Docker container command execution
- Continuous monitoring mode
- Comprehensive error handling and logging
- Rate limiting between command executions
- Environment-based configuration
- Setup script for easy installation

### Features
- Fetch pending actions from Supabase table
- Execute commands in Kali Docker container
- Store results back to database
- Support for both single-run and continuous modes
- Detailed logging with file and console output

### Security
- Environment variable configuration
- Container isolation for command execution
- Rate limiting to prevent overload
- Error handling to prevent crashes