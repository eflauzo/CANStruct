import math
from canstruct.codegen_c.gendata import DataCodeGenerator
from canstruct.codegen_c.c_common import type_to_c_type, bin_to_hex

class DataCodeGeneratorC(DataCodeGenerator):
    def generate_decoder_code(self, variable_name, indent):
        #bytes_to_read = int(math.ceil(self._bit_count/8.0))


        result = indent + 'unsigned long {}_tmp = 0x0;\n'.format(variable_name)
        #h_result = ''
        #assert self._byte_order == 'big_endian',\
        #    'Only "big endian" byte order is supported so far.'

        bytes_to_read = int(math.ceil((self._bit_count+self._start_bit)/8.0))

        # TODO: this should use byte order
        current_byte = self._start_byte -1
        start_bit = self._start_bit
        bit_count = self._bit_count
        shift = 0
        for i in range(bytes_to_read):
            use_bits_from_this_byte = bit_count + start_bit
            if use_bits_from_this_byte > 8:
                use_bits_from_this_byte = 8
            bits_from_this_byte = use_bits_from_this_byte - start_bit
            result += indent + 'byte_i = data[{}];\n'.format(current_byte)
            #if start_bit != 0:
            result += indent + 'byte_i >>= {};\n'.format(start_bit)

            #if bit_count < 8:
            #literal =
            bin_mask = '1' * bits_from_this_byte
            hex_mask = bin_to_hex(bin_mask)
            result += indent + 'byte_i &= {}; /* Masking out bits 0b{} */\n'.format(hex_mask, bin_mask)
            result += indent + '{}_tmp |= ((unsigned long)byte_i << {});\n'.format(variable_name, shift)
            start_bit = 0
            bit_count -= bits_from_this_byte
            shift += bits_from_this_byte
            current_byte += 1
        type_str = type_to_c_type(self._type)
        #result += indent + '{} {} = ({})({}) * {} + {};\n'.format(
        #    type_str,
        #    variable_name,
        #    type_str,
        #    variable_name,
        #    self._scale,
        #    self._offset
        #)
        return result


    def generate_encoder_code(self, variable_name, indent):

        #assert self._byte_order == 'big_endian',\
        #    'Only "big endian" byte order is supported so far.'
        result = ''
        #bytes_to_write = int(math.ceil(self._bit_count/8.0))

        # TODO: this should use byte order
        #current_byte = self._start_byte
        start_bit = self._start_bit
        #bit_count_i = self._bit_count
        bit_count = self._bit_count
        total_bits_written = 0
        #for i in range(bytes_to_write):
        current_byte = self._start_byte -1
        while bit_count > 0:
            max_bits_to_write_in_this_byte = bit_count + start_bit
            if max_bits_to_write_in_this_byte > 8:
                max_bits_to_write_in_this_byte = 8

            bits_to_be_written_in_this_byte = max_bits_to_write_in_this_byte-start_bit

            mask = '0b' + ('1' * bits_to_be_written_in_this_byte) + ('0' * start_bit)
            var = '(({} << {}) & {})'.format(variable_name, start_bit, mask)
            result += indent + 'data[{}] = data[{}] | {};\n'.format(current_byte, current_byte, var)
            result += indent + '{} >>= {};\n'.format(variable_name, bits_to_be_written_in_this_byte)
            start_bit = 0
            bit_count -= bits_to_be_written_in_this_byte
            current_byte += 1

        return result
