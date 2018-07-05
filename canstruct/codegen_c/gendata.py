import math

class DataCodeGenerator(object):
    BYTE_ORDER_BIG_ENDIAN = 'big_endian'
    BYTE_ORDER_LITTLE_ENDIAN = 'little_endian'
    def __init__(
        self,
        name,
        type,
        start_byte,
        byte_order='big_endian',
        start_bit=0,
        bit_count=8,
        uom='',
        description='',
    ):
        self._name = name
        self._type = type
        self._start_byte = start_byte
        self._byte_order = byte_order
        self._start_bit = start_bit
        self._bit_count = bit_count
        self._uom = uom
        self._description = description

    def generate_decoder_code(self):
        raise NotImplemented

    def generate_encoder_code(self):
        raise NotImplemented
