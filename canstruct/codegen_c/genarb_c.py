import math
from canstruct.codegen_c.gendata import DataCodeGenerator
from canstruct.codegen_c.c_common import type_to_c_type, bin_to_hex

class ArbCodeGeneratorC(object):
    def __init__(self, name, definition):
        self._name = name
        self._definition = definition
        self._arbid_type = type_to_c_type('uint32')

    def generate_def(self):
        indent = '   '
        result = '\n'
        result += 'struct {} {{\n'.format(self._name)
        for component_name, component_def in self._definition['components'].iteritems():
            result += indent + '{} {};\n'.format(type_to_c_type(component_def['type']), component_name)
        result += '};\n\n'

        result += '{} {}_encode(struct {}*);\n'.format(self._arbid_type, self._name, self._name)
        result += 'void {}_decode(struct {}*, {});\n'.format(self._name, self._name, format(self._arbid_type))
        result += '\n'
        return result

    def generate_impl(self):
        # generating serializer
        indent = '    '
        result = ''
        result += '{} {}_encode(struct {}* handle){{\n'.format(self._arbid_type, self._name, self._name)
        result += indent + "{} result = 0x0;\n".format(self._arbid_type)
        for component_name, component_def in self._definition['components'].iteritems():
            #result += indent + '{} {};\n'.format(type_to_c_type(component_def['type']), component_name)
            bit_mask = '0b' + ('1' * component_def['bit_count'])
            hex_bit_max = bin_to_hex(bit_mask)
            result += indent + 'result |= (uint32_t)({} & handle->{}) << {};\n'.format(hex_bit_max, component_name,  component_def['start_bit'])
        result += indent + 'return result;\n'
        result += "}\n\n"

        result += 'void {}_decode(struct {}* handle, {} arbid){{\n'.format(self._name, self._name, self._arbid_type)
        #result += indent + "*arbid = 0x0;\n"
        for component_name, component_def in self._definition['components'].iteritems():
            #result += indent + '{} {};\n'.format(type_to_c_type(component_def['type']), component_name)
            bit_mask = '0b' + ('1' * component_def['bit_count'])
            hex_bit_max = bin_to_hex(bit_mask)
            result += indent + 'handle->{} = ((arbid >> {}) & {});\n'.format(component_name, component_def['start_bit'], hex_bit_max)
            #result += indent + '*arbid |= ({} & handle->{}) << {};\n'.format(hex_bit_max, component_name,  component_def['start_bit'])
        #result += indent + 'return result;\n'
        result += "}\n\n"

        return result
    '''
    def generate_decoder_code(self, variable_name, indent):
        pass


    def generate_encoder_code(self, variable_name, indent):
        pass
    '''
