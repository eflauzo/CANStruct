import math
from canstruct.codegen_c.gendata import DataCodeGenerator
from canstruct.codegen_c.c_common import type_to_c_type, bin_to_hex

class DispatchCodeGeneratorC(object):
    def __init__(self, proto, messages):
        self._proto = proto
        self._messages = messages
        self._arb_id_type = type_to_c_type('uint32')
        #self._arb_id_type = type_to_c_type('uint32')

        #self._definition = definition
        #self._arbid_type = type_to_c_type('uint32')

    def generate_def(self):
        indent = '   '
        result = '\n'
        result += 'struct {}Dispatcher_t{{\n'.format(
            self._proto
        )
        result += indent + 'void *user_data;\n'
        for message in self._messages['messages']:
            result += indent + 'void (*on_{}_ptr)(struct {}Dispatcher_t*, {} arb_id, struct {}{}_t *msg);\n'.format(
                message,
                self._proto,
                self._arb_id_type,
                self._proto,
                message,
            )
        result += '};\n'
        result += '\n'
        result += 'void {}_init(struct {}Dispatcher_t*);\n'.format(
            self._proto,
            self._proto,
        )
        result += 'void {}_dispatch(struct {}Dispatcher_t*, {} arb_id, {} data[]);\n'.format(
            self._proto,
            self._proto,
            self._arb_id_type,
            type_to_c_type('uint8')
        )
        return result;

    def generate_impl(self):
        indent = '    '
        result = '\n'
        result += 'void {}_init(struct {}Dispatcher_t *handle){{\n'.format(
            self._proto,
            self._proto,
        )
        result += indent + 'handle->user_data = NULL;\n'
        for message in self._messages['messages']:
            result += indent + 'handle->on_{}_ptr = NULL;\n'.format(message)
        result += "}\n"
        result += "\n"
        result += 'void {}_dispatch(struct {}Dispatcher_t *handle, {} arb_id, {} data[]){{\n'.format(
            self._proto,
            self._proto,
            self._arb_id_type,
            type_to_c_type('uint8')
        )
        #result += indent +
        result += indent + 'struct {}ArbId arb_id_struct;\n'.format(self._proto);
        result += indent + '{}ArbId_decode(&arb_id_struct, arb_id);\n'.format(self._proto);
        for message, message_def in self._messages['messages'].iteritems():
            result += indent + 'if (\n'
            #result += indent + 'if (\n'
            conditions = []
            for field, value in message_def['id'].iteritems():
                conditions.append('(arb_id_struct.{}=={})'.format(field, value))
            conditions_str = '&&'.join(conditions)
            result += indent + indent + conditions_str + '\n'
            result += indent + '){\n'
            result += indent + indent + 'if (handle->on_{}_ptr != NULL){{\n'.format(message);
            result += indent + indent + indent + 'struct {}{}_t msg;\n'.format(self._proto, message);
            result += indent + indent + indent + '{}{}_decode(&msg, data);\n'.format(self._proto, message);
            result += indent + indent + indent + '(*handle->on_{}_ptr)(handle, arb_id, &msg);\n'.format(message)
            result += indent + indent + '}\n'
            result += indent + '}\n'
        result += "}\n"
        result += "\n"
        return result
