# CANStruct
CAN Bus message definition using YAML

# Usage Example

```
canstruct_gen_c.py examples/j1939.yaml --outdir ./outdir
```

This will generate C code for serializing and deserializing
CAN j1939 messages (this is minimal example - dont expect too much)

in ./outdir should be two files

```
 j1939.c
 j1939.h

```

For linux there is handy utility to parse CANStruct Messages

```
python canmonitor.py can0 ~/project/persephone/messages/Siren.yaml
```

![CANStruct CAN Monitor Screenshot](https://github.com/eflauzo/CANStruct/blob/master/screenshots/canmonitor_siren.png "CAN Monitor")
