
def bit_mask(bit_count):
    return int('0b'+('1' * bit_count), 2)

class CANStruct(object):

    def __init__(self, config):
        self.config = config

    def decode_arbid(self, arbid):
        result = {}
        for field_name, field_def in self.config['arb_id']['components'].iteritems():
            mask = bit_mask(field_def['bit_count'])
            result[field_name] = (arbid >> field_def['start_bit']) & mask
        return result

    def encode_arbid(self, arbid_dict):
        result = 0x0
        for field_name, field_def in self.config['arb_id']['components'].iteritems():
            mask = bit_mask(field_def['bit_count'])
            result |= int(arbid_dict[field_name]) & mask << start_bit
        return result

    def decode_message(self, message_type, message):
        #for message in self.config['messages']:
        result = {}
        for field_name, field_def in self.config['messages'][message_type]['data'].iteritems():
            byte_i = field_def['start_byte'] - 1
            bits_to_read = field_def['bit_count']
            start_bit = field_def['start_bit']
            value = 0x0
            while bits_to_read > 0:
                if bits_to_read + start_bit <= 8:
                    bits_in_this_byte = bits_to_read - start_bit
                else:
                    # will will roll over
                    bits_in_this_byte = 8 - start_bit
                shift = field_def['bit_count'] - bits_to_read
                mask = bit_mask(bits_in_this_byte)
                tmp_val = (message[byte_i] >> start_bit) & mask
                value |= tmp_val << shift
                start_bit = 0
                bits_to_read -= bits_in_this_byte
                byte_i+=1
            result[field_name] = value * field_def['scale'] + field_def['offset']
        return result

    def encode_message(self, message_type, message):
        msg_type = self.config['messages'][message_type]
        result = [0x00] * msg_type['frame_length']
        for field_name, field_def in msg_type['data'].iteritems():
            f_value = (message[field_name] - field_def['offset']) / field_def['scale']
            value = int(f_value)
            #bits_to_wite =
            #bits_in_this_byte =
            start_bit = field_def['start_bit']
            byte_i = field_def['start_byte'] - 1
            bits_to_write = field_def['bit_count']
            while bits_to_write > 0:
                bits_in_this_byte = bits_to_write
                if bits_in_this_byte > 8:
                    bits_in_this_byte -= 8
                bits_in_this_byte -= start_bit
                mask = bit_mask(bits_in_this_byte)
                bits_to_write -= bits_in_this_byte
                result_byte = (value & mask) << start_bit
                result[byte_i] = result_byte
                value = value >> bits_in_this_byte
                start_bit = 0
                byte_i += 1
        return result

    #    result = {}
    #    result_type = None
    #    for message in self.config['messages']:
    #        for id_field in =
