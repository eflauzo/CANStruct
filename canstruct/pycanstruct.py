
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
            result |= (int(arbid_dict[field_name]) & mask) << field_def['start_bit']
        return result

    def decode_message(self, message_type, message):
        result = {}
        for field_name, field_def in self.config['messages'][message_type]['data'].iteritems():
            byte_i = field_def['start_byte'] - 1
            bits_to_read = field_def['bit_count']
            start_bit = field_def['start_bit']
            value = 0x0
            shift = 0
            while bits_to_read > 0:
                max_avail_bits = 8 - start_bit
                if bits_to_read > max_avail_bits:
                    bits_in_this_byte = max_avail_bits
                else:
                    bits_in_this_byte = bits_to_read
                mask = bit_mask(bits_in_this_byte)
                tmp_val = (message[byte_i] >> start_bit) & mask
                value |= tmp_val << shift
                start_bit = 0
                bits_to_read -= bits_in_this_byte
                byte_i+=1
                shift += bits_in_this_byte
            result[field_name] = value * field_def['scale'] + field_def['offset']
        return result

    def encode_message(self, message_type, message):
        msg_type = self.config['messages'][message_type]
        result = [0x00] * msg_type['frame_length']
        for field_name, field_def in msg_type['data'].iteritems():
            f_value = (message[field_name] - field_def['offset']) / field_def['scale']
            value = int(f_value)
            start_bit = field_def['start_bit']
            byte_i = field_def['start_byte'] - 1
            bits_to_write = field_def['bit_count']
            while bits_to_write > 0:
                bits_in_this_byte = start_bit + bits_to_write
                if bits_in_this_byte>8:
                    bits_in_this_byte -= 8
                bits_in_this_byte -= start_bit
                mask = bit_mask(bits_in_this_byte)
                bits_to_write -= bits_in_this_byte
                result[byte_i] |= (value & mask) << start_bit
                value = value >> bits_in_this_byte
                start_bit = 0
                byte_i += 1
        return result

    def identify_message_type(self, parsed_arb_id):
        for msg_type, msg_def in self.config['messages'].iteritems():

            all_match = True

            for field_name, field_value in msg_def['id'].iteritems():
                assert field_name in parsed_arb_id.keys()
                all_match = all_match and( parsed_arb_id[field_name] == field_value)

            if all_match:
                 return msg_type
        return None
