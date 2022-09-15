#Source: https://github.com/pycom/pycom-modbus/tree/master/uModbus

import umodbus.uModBusConst as Const
import struct


def read_holding_registers(starting_address, quantity):
    if not (1 <= quantity <= 125):
        raise ValueError('invalid number of holding registers')

    return struct.pack('>BHH', Const.READ_HOLDING_REGISTERS, starting_address, quantity)

def write_single_register(register_address, register_value, signed=True):
    fmt = 'h' if signed else 'H'

    return struct.pack('>BH' + fmt, Const.WRITE_SINGLE_REGISTER, register_address, register_value)

def validate_resp_data(data, function_code, address, value=None, quantity=None, signed = True):
    if function_code in [Const.WRITE_SINGLE_COIL, Const.WRITE_SINGLE_REGISTER]:
        fmt = '>H' + ('h' if signed else 'H')
        resp_addr, resp_value = struct.unpack(fmt, data)

        if (address == resp_addr) and (value == resp_value):
            return True

    elif function_code in [Const.WRITE_MULTIPLE_COILS, Const.WRITE_MULTIPLE_REGISTERS]:
        resp_addr, resp_qty = struct.unpack('>HH', data)

        if (address == resp_addr) and (quantity == resp_qty):
            return True

    return False
