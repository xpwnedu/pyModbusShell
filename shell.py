import cmd
from pymodbus.client import ModbusTcpClient

class modbusShell(cmd.Cmd):
    intro = "Welcome to the pyModbusShell, written by xpwnedu. \nType help or ? to list commands.\n"
    prompt = "(pyMbShell) > "
    client = None

    # ----- basic MbShell commands -----
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
            print('Not connected to a server.')
            return
        self.client.close()
        print("Succesfully disconnected.")

    def do_read_coil(self, arg):
        'Read a coil: read_coil <coil>'
        if not self.client:
            print('Not connected to a server.')
            return
        coil = int(arg)
        read = self.client.read_coils(coil, 1)
        print(read.bits[0])
    
    def do_read_coils(self, arg):
        'Read coils: read_coils <starting_coil> <count>'
        if not self.client:
            print('Not connected to a server.')
            return
        starting_coil, count = arg.split()
        read = self.client.read_coils(int(starting_coil), int(count))
        for i in range(int(count)):
            print(f"Coil {i}: {read.bits[i]}")

    def do_write_coil(self, arg):
        'Write to a coil: write_coil <coil> <Boolean>'
        if not self.client:
            print('Not connected to a server.')
            return
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
        read = self.client.read_coils(int(coil))
        print(read.bits[0])
    
    def do_read_register(self, arg):
        'Read a register: read_holding_register <register>'
        if not self.client:
            print('Not connected to a server.')
            return
        register = int(arg)
        read = self.client.read_holding_registers(register)
        print(read.registers[0])
    
    def do_read_registers(self, arg):
        'Read a register: read_holding_register <register> <count>'
        if not self.client:
            print('Not connected to a server.')
            return
        register, count = arg.split()
        for i in range(int(count)):
            read = self.client.read_holding_registers(int(register) + 1)
            print(read.registers[0])

if __name__ == '__main__':
    modbusShell().cmdloop()