
def type_to_c_type(datatype):
    if datatype == 'uint8':
        return 'uint8_t'

    if datatype == 'uint16':
        return 'uint16_t'

    if datatype == 'uint32':
        return 'uint32_t'

    if datatype == 'int8':
        return 'int8_t'

    if datatype == 'int16':
        return 'int16_t'

    if datatype == 'int32':
        return 'int32_t'

    if datatype == 'float':
        return 'float'
    if datatype == 'double':
        return 'double'
    if datatype == 'double':
        return 'double'
    raise RuntimeError('Unknown datatype {}'.format(datatype))

def bin_to_hex(value):
    return hex(int(value,2))
