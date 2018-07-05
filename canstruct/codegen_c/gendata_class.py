from canstruct.codegen_c import gendata

class DataClassCodeGenerator(object):
    #BYTE_ORDER_BIG_ENDIAN = 'big_endian'
    #BYTE_ORDER_LITTLE_ENDIAN = 'little_endian'
    def __init__(
        self,
        name,
        data
    ):
        self._name = name
        self._data = data

    def generate_class(self):
        raise NotImplemented

class DataClassGeneratorPython(DataClassCodeGenerator):

    #def __init__(self, data):
    def generate_class(self):
        # class definition and constructor

        result = 'class {}(object):\n'.format(self._name)
        indent = '    '
        result += indent + 'def __init__(\n'
        result += indent + indent + 'self,\n'
        for item in self._data.keys():
            result += indent + indent + '{},\n'.format(item)
        result += indent + '):\n'
        for item in self._data.keys():
            result += indent + indent + 'self._{} = {}\n'.format(item, item)
        result += '\n'
        result += '\n'

        # encoder

        result += indent + 'def encode(self):\n'
        result += indent + indent + 'data = [0x00] * 8\n'
        for item, value in self._data.iteritems():
            result += indent + indent + '# serializing {}\n'.format(item)
            code_generator = gendata.DataCodeGeneratorPython(
                item,
                value['type'],
                value['start_byte'],
                start_bit=value['start_bit'],
                bit_count=value['bit_count']
            )
            result += code_generator.generate_encoder_code(
                variable_name='self._' + item,
                indent=indent + indent
            )
            result += indent + indent + '#\n'
        result += indent + indent + 'return data\n'
        result += '\n'
        # decoder

        result += indent + '@staticmethod\n'
        result += indent + 'def decode(data):\n'
        for item, value in self._data.iteritems():
            result += indent + indent + '# deserializing {}\n'.format(item)
            code_generator = gendata.DataCodeGeneratorPython(
                item,
                value['type'],
                value['start_byte'],
                start_bit=value['start_bit'],
                bit_count=value['bit_count']
            )
            result += code_generator.generate_decoder_code(
                variable_name=item,
                indent=indent + indent
            )
            result += indent + indent + '#\n'

        result += indent + indent + 'return {}(\n'.format(self._name)
        for item in self._data.keys():
            result += indent + indent + indent + item +',\n'
        #result += indent + indent + 'return result\n'
        result += indent + indent + ')\n'

        return result
