#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import pathlib
from typing import List, Dict, Any, Optional

class SSHConnector:
    """
    A flexible SSH connection manager that allows users to organize and connect to servers
    through a simple menu interface. Server configurations are stored in a JSON file.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the SSH Connector with optional configuration path.
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        self.home_dir = str(pathlib.Path.home())
        self.config_dir = os.path.join(self.home_dir, '.ssh_connector')
        self.config_path = config_path or os.path.join(self.config_dir, 'config.json')
        self.username = self.get_default_username()
        self.server_groups = {}
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load configuration or create default
        self.load_config()
    
    def get_default_username(self) -> str:
        """Get default username from system"""
        return os.environ.get('USER') or os.environ.get('USERNAME') or 'user'
    
    def load_config(self) -> None:
        """Load server configuration from JSON file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.username = config.get('username', self.username)
                    self.server_groups = config.get('server_groups', {})
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading configuration: {e}")
                self.create_default_config()
        else:
            self.create_default_config()
    
    def save_config(self) -> None:
        """Save current configuration to JSON file"""
        config = {
            'username': self.username,
            'server_groups': self.server_groups
        }
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"Configuration saved to {self.config_path}")
        except IOError as e:
            print(f"Error saving configuration: {e}")
    
    def create_default_config(self) -> None:
        """Create a default configuration if none exists"""
        self.server_groups = {
            "Development": [
                "dev-server-1.example.com",
                "dev-server-2.example.com"
            ],
            "Production": [
                "prod-server-1.example.com",
                "prod-server-2.example.com"
            ],
            "Database": [
                "db-server-1.example.com",
                "db-server-2.example.com"
            ]
        }
        self.save_config()
        print(f"Created default configuration at {self.config_path}")
        print("Please customize this file with your own server groups and servers")
    
    def connect_to_server(self, server: str) -> None:
        """
        Connect to the selected server using SSH
        
        Args:
            server: Hostname or IP address of the server
        """
        print(f"\nConnecting to {server} as {self.username}...")
        try:
            subprocess.call([
                "ssh", 
                "-o", "GSSAPIAuthentication=yes", 
                "-o", "GSSAPIDelegateCredentials=yes", 
                f"{self.username}@{server}"
            ])
        except Exception as e:
            print(f"Error connecting to server: {e}")
        
        input("\nSSH session ended. Press Enter to return to the menu.")
    
    def change_username(self) -> None:
        """Change the SSH username"""
        print(f"\nCurrent username: {self.username}")
        new_username = input("Enter new username (leave blank to keep current): ")
        if new_username:
            self.username = new_username
            self.save_config()
            print(f"Username changed to {self.username}")
        else:
            print("Username unchanged")
        input("\nPress Enter to continue...")
    
    def add_server_group(self) -> None:
        """Add a new server group"""
        group_name = input("\nEnter name for the new server group: ")
        if not group_name:
            print("Group name cannot be empty")
            input("\nPress Enter to continue...")
            return
        
        if group_name in self.server_groups:
            print(f"Group '{group_name}' already exists")
            input("\nPress Enter to continue...")
            return
        
        self.server_groups[group_name] = []
        self.save_config()
        print(f"Group '{group_name}' added successfully")
        input("\nPress Enter to continue...")
    
    def manage_server_group(self, group_name: str) -> None:
        """
        Manage servers in a group
        
        Args:
            group_name: Name of the server group to manage
        """
        while True:
            options = [
                f"Add server to {group_name}",
                f"Remove server from {group_name}",
                f"Rename {group_name}",
                f"Delete {group_name}",
                "Back to Server Groups"
            ]
            
            choice = self.display_menu(f"MANAGE {group_name.upper()}", options)
            
            if choice == 0:  # Add server
                self.add_server(group_name)
            elif choice == 1:  # Remove server
                self.remove_server(group_name)
            elif choice == 2:  # Rename group
                self.rename_server_group(group_name)
                return  # Exit after renaming
            elif choice == 3:  # Delete group
                if self.delete_server_group(group_name):
                    return  # Exit if group was deleted
            elif choice == 4:  # Back
                return
    
    def add_server(self, group_name: str) -> None:
        """
        Add a server to a group
        
        Args:
            group_name: Name of the group to add server to
        """
        server = input("\nEnter server hostname or IP: ")
        if not server:
            print("Server cannot be empty")
        elif server in self.server_groups[group_name]:
            print(f"Server '{server}' already exists in this group")
        else:
            self.server_groups[group_name].append(server)
            self.save_config()
            print(f"Server '{server}' added to {group_name}")
        
        input("\nPress Enter to continue...")
    
    def remove_server(self, group_name: str) -> None:
        """
        Remove a server from a group
        
        Args:
            group_name: Name of the group to remove server from
        """
        if not self.server_groups[group_name]:
            print(f"No servers in {group_name}")
            input("\nPress Enter to continue...")
            return
        
        options = self.server_groups[group_name] + ["Cancel"]
        choice = self.display_menu(f"SELECT SERVER TO REMOVE FROM {group_name.upper()}", options)
        
        if choice < len(self.server_groups[group_name]):
            server = self.server_groups[group_name][choice]
            self.server_groups[group_name].remove(server)
            self.save_config()
            print(f"Server '{server}' removed from {group_name}")
            input("\nPress Enter to continue...")
    
    def rename_server_group(self, group_name: str) -> bool:
        """
        Rename a server group
        
        Args:
            group_name: Current name of the group
            
        Returns:
            bool: True if group was renamed, False otherwise
        """
        new_name = input(f"\nEnter new name for {group_name} (leave blank to cancel): ")
        if not new_name:
            print("Rename cancelled")
            input("\nPress Enter to continue...")
            return False
        
        if new_name in self.server_groups:
            print(f"Group '{new_name}' already exists")
            input("\nPress Enter to continue...")
            return False
        
        self.server_groups[new_name] = self.server_groups.pop(group_name)
        self.save_config()
        print(f"Group renamed from '{group_name}' to '{new_name}'")
        input("\nPress Enter to continue...")
        return True
    
    def delete_server_group(self, group_name: str) -> bool:
        """
        Delete a server group
        
        Args:
            group_name: Name of the group to delete
            
        Returns:
            bool: True if group was deleted, False otherwise
        """
        confirm = input(f"\nAre you sure you want to delete '{group_name}'? (y/n): ")
        if confirm.lower() != 'y':
            print("Deletion cancelled")
            input("\nPress Enter to continue...")
            return False
        
        del self.server_groups[group_name]
        self.save_config()
        print(f"Group '{group_name}' deleted")
        input("\nPress Enter to continue...")
        return True
    
    def server_group_menu(self, group_name: str) -> None:
        """
        Display server menu for a specific group
        
        Args:
            group_name: Name of the server group
        """
        while True:
            servers = self.server_groups.get(group_name, [])
            options = servers + ["Manage Group", "Back to Server Groups"]
            
            choice = self.display_menu(f"{group_name.upper()} SERVERS", options)
            
            if choice < len(servers):
                self.connect_to_server(servers[choice])
            elif choice == len(servers):  # Manage Group
                self.manage_server_group(group_name)
            else:  # Back
                return
    
    def display_menu(self, title: str, options: List[str]) -> int:
        """
        Display a menu with options and return the selected index
        
        Args:
            title: Title of the menu
            options: List of menu options
            
        Returns:
            int: Index of the selected option
        """
        while True:
            self.clear_screen()
            print("=" * 60)
            print(f"{title:^60}")
            print("=" * 60)
            print(f"Current username: {self.username}\n")
            
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
                
            try:
                choice = int(input(f"\nEnter your choice [1-{len(options)}]: "))
                if 1 <= choice <= len(options):
                    return choice - 1
                else:
                    print("\nInvalid choice. Press Enter to continue...")
                    input()
            except ValueError:
                print("\nPlease enter a number. Press Enter to continue...")
                input()
    
    def clear_screen(self) -> None:
        """Clear the terminal screen based on the platform"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def server_groups_menu(self) -> None:
        """Display the server groups menu"""
        while True:
            groups = list(self.server_groups.keys())
            options = groups + ["Add New Group", "Back to Main Menu"]
            
            choice = self.display_menu("SERVER GROUPS", options)
            
            if choice < len(groups):
                self.server_group_menu(groups[choice])
            elif choice == len(groups):  # Add New Group
                self.add_server_group()
            else:  # Back
                return
    
    def export_config(self) -> None:
        """Export configuration to a file"""
        export_path = input("\nEnter file path for export (or press Enter for default): ")
        if not export_path:
            export_path = os.path.join(self.home_dir, 'ssh_connector_config.json')
        
        try:
            with open(export_path, 'w') as f:
                json.dump({
                    'username': self.username,
                    'server_groups': self.server_groups
                }, f, indent=2)
            print(f"Configuration exported to {export_path}")
        except IOError as e:
            print(f"Error exporting configuration: {e}")
        
        input("\nPress Enter to continue...")
    
    def import_config(self) -> None:
        """Import configuration from a file"""
        import_path = input("\nEnter file path to import: ")
        if not os.path.exists(import_path):
            print(f"File not found: {import_path}")
            input("\nPress Enter to continue...")
            return
        
        try:
            with open(import_path, 'r') as f:
                config = json.load(f)
                
            # Validate structure
            if not isinstance(config, dict) or 'server_groups' not in config:
                raise ValueError("Invalid configuration format")
                
            self.username = config.get('username', self.username)
            self.server_groups = config['server_groups']
            self.save_config()
            print("Configuration imported successfully")
        except (json.JSONDecodeError, IOError, ValueError) as e:
            print(f"Error importing configuration: {e}")
        
        input("\nPress Enter to continue...")
    
    def show_help(self) -> None:
        """Display help information"""
        self.clear_screen()
        print("=" * 60)
        print(f"{'SSH CONNECTOR HELP':^60}")
        print("=" * 60)
        print("\nSSH Connector allows you to organize and connect to SSH servers")
        print("through a simple menu interface. The configuration is stored in:")
        print(f"{self.config_path}\n")
        print("Basic Usage:")
        print("  - Server Groups: Organize servers into logical groups")
        print("  - Add/Remove: Manage server groups and individual servers")
        print("  - Connect: Select a server to establish an SSH connection")
        print("  - Import/Export: Share configurations between systems\n")
        print("SSH Authentication:")
        print("  - The tool uses your system's SSH config and keys")
        print("  - For passwordless login, set up SSH keys for your servers")
        print("  - Edit ~/.ssh/config for advanced SSH options per host\n")
        print("For more information, visit the GitHub repository at:")
        print("https://github.com/yourusername/ssh-connector")
        
        input("\nPress Enter to return to the main menu...")
    
    def main_menu(self) -> None:
        """Display the main menu"""
        while True:
            options = [
                "Server Groups",
                "Change Username",
                "Import Configuration",
                "Export Configuration",
                "Help",
                "Exit"
            ]
            
            choice = self.display_menu("SSH CONNECTOR", options)
            
            if choice == 0:  # Server Groups
                self.server_groups_menu()
            elif choice == 1:  # Change Username
                self.change_username()
            elif choice == 2:  # Import Configuration
                self.import_config()
            elif choice == 3:  # Export Configuration
                self.export_config()
            elif choice == 4:  # Help
                self.show_help()
            elif choice == 5:  # Exit
                print("\nGoodbye!")
                sys.exit(0)


def main():
    """Main entry point"""
    try:
        connector = SSHConnector()
        connector.main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()

