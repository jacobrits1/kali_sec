#!/usr/bin/env python3
"""
Kali Docker Automation Script
Handles command execution in Kali container and Supabase integration
"""

import os
import time
import logging
import subprocess
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import docker
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kali_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KaliAutomation:
    """
    Main class for Kali Docker automation with Supabase integration
    """
    
    def __init__(self):
        """Initialize the automation system"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.kali_container_name = os.getenv('KALI_CONTAINER_NAME', 'kali-container')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        # Initialize Supabase client
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        
        # Initialize Docker client
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            raise
    
    def get_pending_actions(self) -> List[Dict]:
        """
        Fetch actions from Supabase that have no results
        Returns: List of action records
        """
        try:
            response = self.supabase.table('kali_actions').select('*').is_('result', 'null').execute()
            logger.info(f"Found {len(response.data)} pending actions")
            return response.data
        except Exception as e:
            logger.error(f"Error fetching pending actions: {e}")
            return []
    
    def execute_command_in_kali(self, command: str) -> Dict[str, str]:
        """
        Execute command in Kali Docker container
        Args:
            command: Command to execute
        Returns:
            Dict with stdout, stderr, and exit_code
        """
        try:
            # Get the Kali container
            container = self.docker_client.containers.get(self.kali_container_name)
            
            # Execute command in container
            logger.info(f"Executing command: {command}")
            exec_result = container.exec_run(
                cmd=command,
                workdir='/root',
                environment={'TERM': 'xterm'}
            )
            
            result = {
                'stdout': exec_result.output.decode('utf-8', errors='ignore'),
                'stderr': '',  # Docker exec doesn't separate stderr
                'exit_code': exec_result.exit_code,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Command completed with exit code: {exec_result.exit_code}")
            return result
            
        except docker.errors.NotFound:
            logger.error(f"Container '{self.kali_container_name}' not found")
            return {
                'stdout': '',
                'stderr': f"Container '{self.kali_container_name}' not found",
                'exit_code': -1,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {
                'stdout': '',
                'stderr': str(e),
                'exit_code': -1,
                'timestamp': datetime.now().isoformat()
            }
    
    def update_action_result(self, action_id: int, result: Dict[str, str]) -> bool:
        """
        Update action result in Supabase
        Args:
            action_id: ID of the action to update
            result: Result dictionary
        Returns:
            Success status
        """
        try:
            # Format result for storage
            result_text = f"Exit Code: {result['exit_code']}\n"
            result_text += f"Timestamp: {result['timestamp']}\n"
            result_text += f"Output:\n{result['stdout']}"
            
            if result['stderr']:
                result_text += f"\nErrors:\n{result['stderr']}"
            
            # Update the record
            self.supabase.table('kali_actions').update({
                'result': result_text
            }).eq('id', action_id).execute()
            
            logger.info(f"Updated action {action_id} with result")
            return True
            
        except Exception as e:
            logger.error(f"Error updating action result: {e}")
            return False
    
    def process_pending_actions(self) -> int:
        """
        Process all pending actions
        Returns:
            Number of actions processed
        """
        actions = self.get_pending_actions()
        processed_count = 0
        
        for action in actions:
            try:
                action_id = action['id']
                command = action['command']
                
                logger.info(f"Processing action {action_id}: {command}")
                
                # Execute command
                result = self.execute_command_in_kali(command)
                
                # Update result in database
                if self.update_action_result(action_id, result):
                    processed_count += 1
                
                # Rate limiting - wait between commands
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error processing action {action.get('id', 'unknown')}: {e}")
                continue
        
        return processed_count
    
    def run_continuous_monitoring(self, interval_seconds: int = 60):
        """
        Run continuous monitoring of pending actions
        Args:
            interval_seconds: Interval between checks
        """
        logger.info(f"Starting continuous monitoring with {interval_seconds}s intervals")
        
        while True:
            try:
                processed = self.process_pending_actions()
                if processed > 0:
                    logger.info(f"Processed {processed} actions")
                else:
                    logger.debug("No pending actions found")
                
                time.sleep(interval_seconds)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval_seconds)

def main():
    """Main function"""
    try:
        # Initialize automation
        automation = KaliAutomation()
        
        # Check if running in continuous mode
        if os.getenv('CONTINUOUS_MODE', 'false').lower() == 'true':
            interval = int(os.getenv('CHECK_INTERVAL', '60'))
            automation.run_continuous_monitoring(interval)
        else:
            # Run once
            processed = automation.process_pending_actions()
            logger.info(f"Completed processing {processed} actions")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)

if __name__ == "__main__":
    main()