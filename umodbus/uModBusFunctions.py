#Based on: https://github.com/pycom/pycom-modbus/tree/master/uModbus

import umodbus.uModBusConst as Const
import struct


def read_holding_registers(starting_address, quantity):
    if not (1 <= quantity <= 125):
        raise ValueError('invalid number of holding registers')

    return struct.pack('>BHH', Const.READ_HOLDING_REGISTERS, starting_address, quantity)

def write_single_register(register_address, register_value, signed=True):
    fmt = 'h' if signed else 'H'

    return struct.pack('>BH' + fmt, Const.WRITE_SINGLE_REGISTER, register_address, register_value)

def validate_resp_data(data, function_code, address, value=None, signed = True):
    if function_code in [Const.WRITE_SINGLE_COIL, Const.WRITE_SINGLE_REGISTER]:
        fmt = '>H' + ('h' if signed else 'H')
        resp_addr, resp_value = struct.unpack(fmt, data)

        if (address == resp_addr) and (value == resp_value):
            return True
    return False

# Reads data from a list of bytes, and converts to an int
def bytes_to_int(bs, offset = 0, length = 2):
    if len(bs) < (offset + length):
        return 0
    if length > 0:
        byteorder='big'
        start = offset
        end = offset + length
    else:
        byteorder='little'
        start = offset + length + 1
        end = offset + 1
    return int.from_bytes(bs[start:end], byteorder)

# Reads data from a list of bytes, and converts to string
def bytes_to_string(byte_array):
    return str(byte_array, 'utf-8')
