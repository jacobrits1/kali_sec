# Kali Security Automation

A Python script that automates command execution in a Kali Linux Docker container and integrates with Supabase for action management.

## Features

- **Automated Command Execution**: Runs commands in Kali Docker container
- **Supabase Integration**: Fetches pending actions and stores results
- **Continuous Monitoring**: Optional continuous mode for real-time processing
- **Error Handling**: Comprehensive error handling and logging
- **Rate Limiting**: Built-in rate limiting to prevent overload

## Prerequisites

- Python 3.8+
- Docker with Kali Linux container running
- Supabase account and database
- Required Python packages (see requirements.txt)

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup**:
   ```bash
   python setup_kali_automation.py
   ```

4. **Configure environment**:
   - Edit `.env` file with your Supabase credentials
   - Ensure your Kali container is running

## Supabase Table Structure

Create a table named `kali_actions` with the following structure:

```sql
CREATE TABLE kali_actions (
    id SERIAL PRIMARY KEY,
    command TEXT NOT NULL,
    result TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Usage

### Single Run Mode
```bash
python kali_automation.py
```

### Continuous Monitoring Mode
Set `CONTINUOUS_MODE=true` in your `.env` file:
```bash
python kali_automation.py
```

### Environment Variables

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key
- `KALI_CONTAINER_NAME`: Name of your Kali Docker container (default: kali-container)
- `CONTINUOUS_MODE`: Enable continuous monitoring (true/false)
- `CHECK_INTERVAL`: Interval between checks in seconds (default: 60)

## Example Commands

The script can handle various Kali Linux commands:

- `nmap -sV bi.sawisonline.co.za`
- `dirb http://example.com`
- `nikto -h http://example.com`
- `sqlmap -u "http://example.com/vuln.php?id=1"`

## Security Considerations

- **Rate Limiting**: Built-in delays between command executions
- **Error Handling**: Comprehensive error logging and handling
- **Container Isolation**: Commands run in isolated Docker container
- **Environment Variables**: Sensitive data stored in environment variables

## Logging

Logs are written to both console and `kali_automation.log` file.

## Troubleshooting

1. **Container not found**: Ensure your Kali container is running and named correctly
2. **Supabase connection issues**: Verify your credentials in `.env` file
3. **Permission errors**: Ensure Docker daemon is accessible

## License

This project is for educational and authorized security testing purposes only.