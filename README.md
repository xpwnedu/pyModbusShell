# pyModbusShell

pyModbusShell is an interactive command-line tool designed to communicate with Modbus devices using Python. Built on the `pymodbus` library, it provides an intuitive shell interface for performing common Modbus operations, such as reading and writing coils and registers. The tool is developed by xpwnedu and is ideal for engineers, researchers, and developers working with industrial control systems.

## Features

- Interactive shell interface for Modbus communication.
- Supports Modbus TCP protocol.
- Handles both single and batch operations on coils and registers.
- Graceful handling of user interruptions (Ctrl+C).
- Extensible with custom commands for advanced use cases.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- `pip` package manager

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/xpwnedu/pyModbusShell.git
   cd pyModbusShell
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Launch the interactive shell:

   ```bash
   python shell.py
   ```

2. Use the built-in commands to interact with Modbus devices. Examples:

   - Connect to a server:
     ```
     connect <host> <port>
     ```
   - Read a single coil:
     ```
     read_coil <coil>
     ```
   - Write to a register:
     ```
     write_holding_register <register> <value>
     ```

### Example Session

```bash
$ python shell.py
Welcome to the pyModbusShell, written by xpwnedu. 
Type help or ? to list commands.

(pyMbShell) > connect 192.168.1.100 502
Connected to 192.168.1.100:502
(pyMbShell) > read_coil 0
True
(pyMbShell) > write_holding_register 100 12345
Register 100: 12345
(pyMbShell) > disconnect
Successfully disconnected.
(pyMbShell) > exit
Bye bye!
```

## Commands Overview

### Connection Commands

- `connect <host> <port>`: Connect to a Modbus server.
- `disconnect`: Disconnect from the Modbus server.

### Coil Commands

- `read_coil <coil>`: Read the state of a single coil.
- `read_coils <starting_coil> <count>`: Read the states of multiple coils.
- `write_coil <coil> <Boolean>`: Write a value (True/False) to a single coil.

### Register Commands

- `read_holding_registers <starting_register> <count>`: Read values from holding registers.
- `read_input_registers <starting_register> <count>`: Read values from input registers.
- `write_holding_register <register> <value>`: Write a value to a holding register.
- `read_registers_from_file <filename>`: Read holding registers from a file.
- `write_registers_from_file <filename>`: Write values to holding registers from a file.

### Utility Commands

- `exit`: Exit the shell.