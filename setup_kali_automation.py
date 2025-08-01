#!/usr/bin/env python3
"""
Setup script for Kali Automation
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    env_example = Path('env.example')
    env_file = Path('.env')
    
    if env_file.exists():
        print(".env file already exists. Skipping creation.")
        return
    
    if not env_example.exists():
        print("Error: env.example not found")
        return
    
    # Copy template
    with open(env_example, 'r') as f:
        content = f.read()
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("Created .env file. Please update it with your Supabase credentials.")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import docker
        import supabase
        import dotenv
        print("✓ All dependencies are available")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_docker():
    """Check if Docker is running"""
    try:
        import docker
        client = docker.from_env()
        client.ping()
        print("✓ Docker is running")
        return True
    except Exception as e:
        print(f"✗ Docker error: {e}")
        print("Please ensure Docker is running and accessible")
        return False

def main():
    """Main setup function"""
    print("Setting up Kali Automation...")
    
    # Create .env file
    create_env_file()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        sys.exit(1)
    
    print("\nSetup complete! Please:")
    print("1. Update .env file with your Supabase credentials")
    print("2. Ensure your Kali container is running")
    print("3. Run: python kali_automation.py")

if __name__ == "__main__":
    main()