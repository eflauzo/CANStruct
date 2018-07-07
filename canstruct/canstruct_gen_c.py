import os
import argparse

import yaml

from canstruct.codegen_c import gendata_class_c
from canstruct.codegen_c import genarb_c
from canstruct.codegen_c import gendispatch_c
from canstruct.codegen_c import genbuild_msg_c

def generate(messages, outdir):
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    for proto_name, proto_def in messages.iteritems():
        header_name = proto_name.upper() + "_H"
        base_filename = proto_name.lower()

        output_code_h = '#ifndef {}\n'.format(header_name)
        output_code_h += '#define {}\n\n'.format(header_name)
        output_code_h += '#include <stdint.h>\n'

        output_code_c = '#include "{}.h"\n'.format(base_filename)
        output_code_c += '#include <stddef.h>\n'

        arb_id_type = proto_name + 'ArbId'
        generator = genarb_c.ArbCodeGeneratorC(arb_id_type, proto_def['arb_id'])
        output_code_h += generator.generate_def()
        output_code_c += generator.generate_impl()

        for message, message_def in proto_def['messages'].iteritems():
            parser_name = '{}{}'.format(proto_name, message)
            generator = gendata_class_c.DataClassGeneratorC(
                parser_name,
                message_def['data'],
                message_def['frame_length']
            )
            output_code_h += generator.generate_def()
            output_code_c += generator.generate_impl()

        generator = gendispatch_c.DispatchCodeGeneratorC(proto_name, proto_def)
        output_code_h += generator.generate_def()
        output_code_c += generator.generate_impl()

        generator = genbuild_msg_c.BuildMsgCodeGeneratorC(proto_name, proto_def);
        output_code_h += generator.generate_def()
        output_code_c += generator.generate_impl()

        output_code_h +='\n#endif'

        h_filename = os.path.join(outdir,base_filename+'.h')
        c_filename = os.path.join(outdir,base_filename+'.cpp')

        open(h_filename, 'w').write(output_code_h)
        open(c_filename, 'w').write(output_code_c)

def main():
    parser = argparse.ArgumentParser(description='CAN struct C code generator')
    parser.add_argument('canstruct_yaml', help='CANStruct Config File')
    parser.add_argument('--outdir', help='output directory')
    args = parser.parse_args()
    messages = yaml.load(open(args.canstruct_yaml,'r'))
    generate(messages, args.outdir)


if __name__ == "__main__":
    main()
