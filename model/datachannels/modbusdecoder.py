from typing import Dict

"""
    This module contains all the decoding methods for breakdown binary modbus data.
    Most of the function code protocols follow a similar strategy where a starting register is specified
    followed by the amount of registers to read.

    Write methods will send a starting register followed by a set of values to write into concurrent registers.
"""


def read_entity(data) -> (bool, Dict):
    data = data[1:]
    is_error = False

    address = (data[0] << 8) | (data[1])
    count = (data[2] << 8) | (data[3])

    if address < 0:
        is_error = True
        return is_error, _invalid_register_addr(data)
        # return is_error,
    elif count < 0:
        is_error = True
        return is_error, _invalid_data_value(data)
    else:
        return is_error, {
            'address': address,
            'count': count
        }


def read_coils(data):
    return read_entity(data)


def read_discrete_inputs(data):
    return read_entity(data)


def read_holding_registers(data):
    return read_entity(data)


def read_input_registers(data):
    return read_entity(data)


def write_entity(data) -> (bool, Dict):
    data = data[1:]
    is_error = False

    address = (data[0] << 8) | (data[1])
    value = (data[2] << 8) | (data[3])

    if address < 0:
        is_error = True
        return is_error, _invalid_register_addr(data)

    if value < 0:
        is_error = True
        return is_error, _invalid_data_value(data)

    return is_error, {
        'address': address,
        'value': value
    }


def write_single_coil(data):
    return write_entity(data)


def write_single_holding_register(data):
    return write_entity(data)


def write_multiple_coils(data):
    data = data[1:]
    is_error = False

    first_coil = (data[0] << 8) | (data[1])
    num_coils_to_write = (data[2] << 8) | (data[3])
    num_bytes_of_coils = data[4]
    coil_bytes = data[5:5 + num_bytes_of_coils]
    coil_values = [0] * (num_bytes_of_coils * 8)
    # Unpack the coil value hex into an array of on/off (1/0)
    for b in range(0, num_bytes_of_coils * 8):
        mask = 0x01 << b % 8
        bit_set = coil_bytes[b // 8] & mask
        coil_values[b] = 0xFF00 if bit_set else 0x00

    coil_values = coil_values[:num_coils_to_write]

    if first_coil < 0:
        is_error = True
        return is_error, _invalid_register_addr(data)

    for val in coil_values:
        if val < 0:
            return is_error, _invalid_data_value(data)

    return is_error, {
        'address': first_coil,
        'values': coil_values,
        'count': num_coils_to_write
    }


def write_multiple_holding_registers(data):
    data = data[1:]
    is_error = False

    first_register = (data[0] << 8) | (data[1])
    num_regs_to_write = (data[2] << 8) | (data[3])
    num_bytes_of_registers = data[4]
    register_values = [0] * (num_bytes_of_registers // 2)
    # Each register value is 16 bits, decode every 2 bytes of data into one 16 bit value
    for i in range(0, num_bytes_of_registers // 2):
        idx = 5 + i * 2
        register_values[i] = (data[idx] << 8) | (data[idx + 1])

    if first_register < 0:
        is_error = True
        return is_error, _invalid_register_addr(data)

    for val in register_values:
        if val < 0:
            return is_error, _invalid_data_value(data)

    return is_error, {
        'address': first_register,
        'values': register_values,
        'count': num_regs_to_write
    }


def dissect_header(header_data):
    if len(header_data) < 7:
        return {'error': 'header is too short'}
    transaction_id = (header_data[0] << 8) | (header_data[1])
    protocol_id = (header_data[2] << 8) | (header_data[3])
    length = (header_data[4] << 8) | (header_data[5])
    unit_id = (header_data[6])
    return {
        'transaction_id': transaction_id,
        'protocol_id': protocol_id,
        'length': length,
        'unit_id': unit_id
    }


def invalid_function_code(data):
    code = data[0]
    is_error = True
    response_code = 0x80 | code
    error_code = 0x01
    response = (response_code << 8) | error_code
    return is_error, response.to_bytes(2, byteorder='big')


def _invalid_register_addr(data):
    function_code = data[0]
    error_code = 0x02
    return (((function_code | 0x80) << 8) | error_code).to_bytes(2, byteorder='big')


def _invalid_data_value(data):
    function_code = data[0]
    error_code = 0x03
    return (((function_code | 0x80) << 8) | error_code).to_bytes(2, byteorder='big')
