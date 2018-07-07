import math
from canstruct.codegen_c.gendata import DataCodeGenerator
from canstruct.codegen_c.c_common import type_to_c_type, bin_to_hex

class BuildMsgCodeGeneratorC(object):
    def __init__(self, proto_name, proto_node):
        self._proto_name = proto_name
        self._proto_node = proto_node

    def generate_def(self):
        result = '\n'
        for message in self._proto_node['messages']:
            result += '\n'
            result += '/* initialize {} message with message specific ID fields */\n'.format(
                message,
            )
            result += 'void {}{}_init(struct {}ArbId* arb_id, struct {}{}_t* data);\n'.format(
                self._proto_name, message,
                self._proto_name,
                self._proto_name, message
            )
        return result

    def generate_impl(self):
        result = '\n'

        for message_name, message_node in self._proto_node['messages'].iteritems():
            result += '\n'
            result += '/* initialize {} message with message specific ID fields */\n'.format(
                message_name,
            )
            indent = '    '
            result += 'void {}{}_init(struct {}ArbId* arb_id, struct {}{}_t* data){{\n'.format(
                self._proto_name, message_name,
                self._proto_name,
                self._proto_name, message_name
            )
            for arbid_field, arbid_field_node in self._proto_node['arb_id']['components'].iteritems():
                value = 0x0
                if 'default' in arbid_field_node:
                    value = arbid_field_node['default']

                for id_field, id_value in message_node['id'].iteritems():
                    if id_field in self._proto_node['arb_id']['components'].keys():
                        if id_field == arbid_field:
                            value = id_value
                    else:
                        raise RuntimeError('There is no {} in arbitration id'.format(id_field))

                result += indent + 'arb_id->{} = {};\n'.format(arbid_field, value)

            result += '}\n'

        return result
