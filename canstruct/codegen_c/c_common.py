
def type_to_c_type(datatype):
    if datatype == 'uint8':
        return 'unsigned char'

    if datatype == 'uint16':
        return 'unsigned short'

    if datatype == 'uint32':
        return 'unsigned int'

    if datatype == 'int8':
        return 'char'

    if datatype == 'int16':
        return 'short'

    if datatype == 'int32':
        return 'int'

    if datatype == 'float':
        return 'float'
    if datatype == 'double':
        return 'double'
    if datatype == 'double':
        return 'double'
    raise RuntimeError('Unknown datatype {}'.format(datatype))

def bin_to_hex(value):
    return hex(int(value,2))
