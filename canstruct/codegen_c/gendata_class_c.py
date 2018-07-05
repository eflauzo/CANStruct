from canstruct.codegen_c import gendata_c
from canstruct.codegen_c.c_common import type_to_c_type, bin_to_hex

class DataClassCodeGenerator(object):
    #BYTE_ORDER_BIG_ENDIAN = 'big_endian'
    #BYTE_ORDER_LITTLE_ENDIAN = 'little_endian'
    def __init__(
        self,
        name,
        data,
        frame_length,
    ):
        self._name = name
        self._data = data
        self._frame_length = frame_length

    def generate_class(self):
        raise NotImplemented

class DataClassGeneratorC(DataClassCodeGenerator):

    #def __init__(self, data):
    def generate_def(self):
        # class definition and constructor

        result = 'struct {}_t{{\n'.format(self._name)
        for item_name, item_def in self._data.iteritems():
            result += '    {} {};\n'.format(type_to_c_type(item_def['type']), item_name)
        #result += indent + 'def __init__(\n'
        #result += indent + indent + 'self,\n'
        #for item in self._data.keys():
        #    result += indent + indent + '{},\n'.format(item)
        #result += indent + '):\n'
        #for item in self._data.keys():
        #    result += indent + indent + 'self._{} = {}\n'.format(item, item)
        result += '};\n'
        result += '\n'
        result += '/* Encode {}_t into CAN frame */\n'.format(self._name)
        result += 'void {}_encode(struct {}_t*, {} data[]);\n'.format(self._name, self._name, type_to_c_type('uint8'))
        result += '\n'
        result += '/* Decode {}_t from CAN frame */\n'.format(self._name)
        result += 'void {}_decode(struct {}_t*, {} data[]);\n'.format(self._name, self._name, type_to_c_type('uint8'))

        return result;

    def generate_impl(self):
        # encoder
        indent = '    '
        #result += indent + 'def encode(self):\n'
        result = 'void {}_encode(struct {}_t* handle, {} data[]) {{\n'.format(self._name, self._name, type_to_c_type('uint8'))
        for byte_i in range(self._frame_length):
            result += indent + 'data[{}] = 0x00;\n'.format(byte_i)
        #result += indent + indent + 'data = [0x00] * 8\n'
        for item, value in self._data.iteritems():
            result += indent + '// serializing {}\n'.format(item)
            code_generator = gendata_c.DataCodeGeneratorC(
                item,
                value['type'],
                value['start_byte'],
                start_bit=value['start_bit'],
                bit_count=value['bit_count'],
            )
            tp = type_to_c_type(value['type'])
            result += indent + '{} {}_tmp = ({})((handle->{} - ({})) / {});\n'.format(
                'unsigned long',
                item,
                'unsigned long',
                item,
                value['offset'],
                value['scale']
            )
            result += code_generator.generate_encoder_code(
                variable_name=item+'_tmp',
                indent=indent
            )
            #result += indent + '#\n'
        #result += indent + 'return data\n'
        result += '}\n'
        result += '\n'
        # decoder

        #result = 'void encode({}_t* handle, uint8_t []data);\n'.format(self._name)rresult = 'void encode({}_t* handle, uint8_t []data);\n'.format(self._name)esult += indent + '@staticmethod\n'
        #result += indent + 'def decode(data):\n'
        result += 'void {}_decode(struct {}_t* handle, {} data[]) {{\n'.format(self._name, self._name, type_to_c_type('uint8'))
        result += indent + '{} byte_i;\n'.format(type_to_c_type('uint8'))

        for item, value in self._data.iteritems():
            result += indent + '// deserializing {}\n'.format(item)
            code_generator = gendata_c.DataCodeGeneratorC(
                item + '_tmp',
                value['type'],
                value['start_byte'],
                start_bit=value['start_bit'],
                bit_count=value['bit_count'],
            )
            result += code_generator.generate_decoder_code(
                variable_name=item,
                indent=indent
            )
            result += indent + 'handle->{} = {}_tmp * ({}) + ({});\n'.format(
                item,
                item,
                value['scale'],
                value['offset'],
            )
            result += indent + '\n'

        #result += indent + indent + 'return {}(\n'.format(self._name)
        #for item in self._data.keys():
        #    result += indent + indent + indent + item +',\n'
        #result += indent + indent + 'return result\n'
        result += '}\n'
        result += '\n'

        return result
