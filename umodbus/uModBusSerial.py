# Based on: https://github.com/pycom/pycom-modbus/tree/master/uModbus
#This file has been modified and differ from its source version.

import umodbus.uModBusFunctions as functions
import umodbus.uModBusConst as Const
from machine import UART, Pin, idle
import struct
import time

class uModBusSerial:

    def __init__(self, uart_id, baudrate=9600, data_bits=8, stop_bits=1, parity=None, pins=None, ctrl_pin=None):
        pinsLen=len(pins)
        if pins==None or pinsLen < 2:
            raise ValueError('pins should contain pin names/numbers for: tx, rx')
        tx=pins[0]
        rx=pins[1]

        self._uart = UART(uart_id, baudrate=baudrate, bits=data_bits, parity=parity, stop=stop_bits, timeout_char=10, tx=tx, rx=rx)
        if ctrl_pin is not None:
            self._ctrlPin = Pin(ctrl_pin, mode=Pin.OUT)
        else:
            self._ctrlPin = None
        self.char_time_ms = (1000 * (data_bits + stop_bits + 2)) // baudrate

    def _calculate_crc16(self, data):
        crc = 0xFFFF

        for char in data:
            crc = (crc >> 8) ^ Const.CRC16_TABLE[((crc) ^ char) & 0xFF]

        return struct.pack('<H',crc)

    def _to_short(self, byte_array):
        return int.from_bytes(byte_array, 'big')

    def _to_string(self, byte_array):
        return str(byte_array, 'utf-8')
    
    def _exit_read(self, response):
        if response[1] >= Const.ERROR_BIAS:
            if len(response) < Const.ERROR_RESP_LEN:
                return False
        elif (Const.READ_COILS <= response[1] <= Const.READ_INPUT_REGISTER):
            expected_len = Const.RESPONSE_HDR_LENGTH + 1 + response[2] + Const.CRC_LENGTH
            if len(response) < expected_len:
                return False
        elif len(response) < Const.FIXED_RESP_LEN:
            return False

        return True

    def _uart_read(self):
        response = bytearray()

        for x in range(1, 40):
            if self._uart.any():
                response.extend(self._uart.read())
                if self._exit_read(response):
                    break
            time.sleep(0.05)
        return response

    def _send_receive(self, modbus_pdu, slave_addr, count):
        serial_pdu = bytearray()
        serial_pdu.append(slave_addr)
        serial_pdu.extend(modbus_pdu)

        crc = self._calculate_crc16(serial_pdu)
        serial_pdu.extend(crc)

        # flush the Rx FIFO
        self._uart.read()
        if self._ctrlPin:
            self._ctrlPin(1)
        self._uart.write(serial_pdu)
        if self._ctrlPin:
            while not self._uart.wait_tx_done(2):
                idle()
            time.sleep_ms(1 + self.char_time_ms)
            self._ctrlPin(0)

        return self._validate_resp_hdr(self._uart_read(), slave_addr, modbus_pdu[0], count)

    def _validate_resp_hdr(self, response, slave_addr, function_code, count):

        if len(response) == 0:
            raise OSError('no data received from slave')

        resp_crc = response[-Const.CRC_LENGTH:]
        expected_crc = self._calculate_crc16(response[0:len(response) - Const.CRC_LENGTH])
        if (resp_crc[0] != expected_crc[0]) or (resp_crc[1] != expected_crc[1]):
            raise OSError('invalid response CRC')

        if (response[0] != slave_addr):
            raise ValueError('wrong slave address')

        if (response[1] == (function_code + Const.ERROR_BIAS)):
            raise ValueError('slave returned exception code: {:d}'.format(response[2]))

        hdr_length = (Const.RESPONSE_HDR_LENGTH + 1) if count else Const.RESPONSE_HDR_LENGTH

        return response[hdr_length : len(response) - Const.CRC_LENGTH]

    def read_holding_registers(self, slave_addr, starting_addr, register_qty, signed=True):
        modbus_pdu = functions.read_holding_registers(starting_addr, register_qty)

        resp_data = self._send_receive(modbus_pdu, slave_addr, True)
        register_value = self._to_string(resp_data) if (register_qty > 2) else self._to_short(resp_data)

        return register_value

    def write_single_register(self, slave_addr, register_address, register_value, signed=True):
        modbus_pdu = functions.write_single_register(register_address, register_value, signed)

        resp_data = self._send_receive(modbus_pdu, slave_addr, False)
        operation_status = functions.validate_resp_data(resp_data, Const.WRITE_SINGLE_REGISTER,
                                                        register_address, value=register_value, signed=signed)

        return operation_status

    def close(self):
        if self._uart == None:
            return
        try:
            self._uart.deinit()
        except Exception:
            pass

