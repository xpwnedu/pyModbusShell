import cmd
import signal
from pymodbus.client import ModbusTcpClient

class modbusShell(cmd.Cmd):
    intro = "Welcome to the pyModbusShell, written by xpwnedu. \nType help or ? to list commands.\n"
    prompt = "(pyMbShell) > "
    client = None

    def __init__(self):
        super().__init__()
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self.signal_handler)
        self.interrupted = False

    def signal_handler(self, sig, frame):
        self.interrupted = True
        print("\nCtrl+C caught. Please type 'exit' to exit the shell.")
    
    def ensure_connection(self):
        "Ensure the client is connected."
        if not self.client:
            print("Not connected to a server.")
            return False
        return True

    def handle_interruptible_loop(self, start, count, action):
        "Handles an interruptible loop for reading Modbus data."
        try:
            for i in range(count):
                if self.interrupted:
                    self.interrupted = False
                    break
                action(i + start)
        except KeyboardInterrupt:
            self.interrupted = False
            print("\nOperation aborted by user.")
        except Exception as e:
            print(f"Error: {e}")
    
    # ----- Basic MbShell Commands -----
    def do_exit(self, arg):
        "Exit the shell: exit"
        print("Bye bye!")
        return True
    
    # ----- Modbus Connection Commands -----
    def do_connect(self, arg):
        "Connect to a Modbus server: connect <host> <port>"
        try:
            host, port = arg.split()
            self.client = ModbusTcpClient(host, port=int(port))
            if self.client.connect():
                print(f"Connected to {host}:{port}")
            else:
                print("Connection failed.")
        except Exception as e:
            print(f"Error: {e}")
        
    def do_disconnect(self, arg):
        "Disconnect from a Modbus server: disconnect"
        if not self.client:
            print("Not connected to a server.")
            return
        self.client.close()
        print("Successfully disconnected.")
    
    def do_get_device_information(self, arg):
        "Query device information: get_device_information"

    
    # ----- Coil Commands -----

    def do_read_coil(self, arg):
        'Read a coil: read_coil <coil>'
        if not self.ensure_connection():
            return
        try:
            coil = int(arg)
            read = self.client.read_coils(coil, 1)
            print(read.bits[0])
        except Exception as e:
            print(f"Error: {e}")

    def do_read_coils(self, arg):
        "Read coils: read_coils <starting_coil> <count>"
        if not self.ensure_connection():
            return
        try:
            starting_coil, count = map(int, arg.split())
            read = self.client.read_coils(starting_coil, count)
            self.handle_interruptible_loop(
                starting_coil, count, lambda i: print(f"Coil {i}: {read.bits[i - starting_coil]}")
            )
        except Exception as e:
            print(f"Error: {e}")

    def do_write_coil(self, arg):
        'Write to a coil: write_coil <coil> <Boolean>'
        if not self.ensure_connection():
            return
        try:
            coil, value = arg.split()
            value = value.lower()
            if value == "true":
                value = True
            elif value == "false":
                value = False
            else:
                print("Not a valid Boolean.")
                return
            self.client.write_coil(int(coil), value)
            read = self.client.read_coils(int(coil), 1)
            print(read.bits[0])
        except Exception as e:
            print(f"Error: {e}")

    # ----- Register Commands -----
    def do_read_registers_from_file(self, arg):
        "Read holding registers from a file: read_registers_from_file <filename>"
        if not self.ensure_connection():
            return
        try:
            with open(arg, "r") as file:
                for line in file:
                    # Parse lines in the format "<register>"
                    try:
                        register = int(line.strip())
                        read = self.client.read_holding_registers(int(register))
                        print(f"Holding register {register}: {read.registers[0]}")
                        read = self.client.read_holding_registers(int(register))
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
        except FileNotFoundError:
            print(f"File not found: {arg}")
        except Exception as e:
            print(f"Error: {e}")

    def do_read_holding_registers(self, arg):
        "Read holding registers: read_holding_registers <starting_register> <count>"
        if not self.ensure_connection():
            return
        try:
            starting_register, count = map(int, arg.split())
            self.handle_interruptible_loop(
                starting_register, count, 
                lambda i: print(f"Holding register {i}: {self.client.read_holding_registers(i).registers[0]}")
            )
        except Exception as e:
            print(f"Error: {e}")

    def do_read_input_registers(self, arg):
        "Read input registers: read_input_registers <starting_register> <count>"
        if not self.ensure_connection():
            return
        try:
            starting_register, count = map(int, arg.split())
            self.handle_interruptible_loop(
                starting_register, count, 
                lambda i: print(f"Input register {i}: {self.client.read_input_registers(i).registers[0]}")
            )
        except Exception as e:
            print(f"Error: {e}")

    def do_write_registers_from_file(self, arg):
        "Write holding registers from a file: write_registers_from_file <filename>"
        if not self.ensure_connection():
            return
        try:
            with open(arg, "r") as file:
                for line in file:
                    # Parse lines in the format "<register>: <value>"
                    try:
                        register, value = map(int, line.split(":"))
                        self.client.write_register(register, value)
                        print(f"Wrote {value} to holding register {register}")
                        read = self.client.read_holding_registers(register)
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
        except FileNotFoundError:
            print(f"File not found: {arg}")
        except Exception as e:
            print(f"Error: {e}")
    
    def do_write_holding_register(self, arg):
        'Write an input register: write_input_regiser <register> <value>'
        if not self.ensure_connection():
            return
        try:
            register, value = arg.split()
            self.client.write_register(int(register), int(value))
            read = self.client.read_holding_registers(int(register))
            print(f"Register {register}: {read.registers[0]}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    modbusShell().cmdloop()