# SSH Connector

A flexible and user-friendly SSH connection manager for quickly accessing your servers through a simple terminal interface.

![SSH Connector Demo](https://github.com/yourusername/ssh-connector/raw/main/assets/demo.gif)

## Features

- **Organized Server Management**: Group servers logically (development, production, databases, etc.)
- **Easy Navigation**: Simple menu-driven interface for quick server access
- **Customizable**: Add, edit, or remove server groups and servers
- **Persistent Configuration**: Settings saved between sessions
- **Portable**: Works on Linux, macOS, WSL, and anywhere Python runs
- **Import/Export**: Share your server configurations between systems
- **Kerberos Support**: Built-in support for Kerberos authentication

## Installation

### Requirements

- Python 3.6+
- SSH client installed on your system

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/ssh-connector.git

# Navigate to the directory
cd ssh-connector

# Make the script executable
chmod +x ssh_connector.py

# Create a symbolic link (optional)
sudo ln -s $(pwd)/ssh_connector.py /usr/local/bin/sshc
```

### Windows (WSL) Installation

If you're using Windows Subsystem for Linux (WSL):

1. Clone the repository in your WSL environment
2. Make the script executable with `chmod +x ssh_connector.py`
3. You can add it to your PATH or create an alias in your `.bashrc` or `.zshrc`:
   ```bash
   echo 'alias sshc="~/path/to/ssh_connector.py"' >> ~/.bashrc
   source ~/.bashrc
   ```

## Usage

### Basic Usage

```bash
# Run directly
./ssh_connector.py

# Or, if you created the symbolic link:
sshc
```

### First Run

On first run, SSH Connector will:
1. Create a configuration directory at `~/.ssh_connector/`
2. Generate a default configuration file with example server groups
3. Guide you through setting up your first server group

### Configuration

SSH Connector stores its configuration in `~/.ssh_connector/config.json`. This file contains:

- Your default SSH username
- Server groups and their associated servers

You can edit this file manually or use the built-in management options.

### SSH Authentication

SSH Connector uses your system's SSH client and configuration:

- For passwordless login, set up SSH keys for your servers
- Configure server-specific settings in `~/.ssh/config`
- The tool supports Kerberos authentication for enterprise environments

## Customization

### Command-line Arguments

```bash
# Specify an alternate configuration file
./ssh_connector.py --config /path/to/config.json

# Start directly with a specific server group
./ssh_connector.py --group "Production"

# Use a different username
./ssh_connector.py --username "admin"
```

### Advanced Configuration

For advanced users, you can customize SSH parameters by editing the code or creating a configuration file with additional options.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for quick server access in multi-environment setups
- Thanks to all contributors and users for their feedback and suggestions

---

Built with ❤️ by Rethin Silvester (https://github.com/rethinsilvester/ssh-connector)
