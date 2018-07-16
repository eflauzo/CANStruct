import threading
import time
import random

import argparse
from collections import OrderedDict

import can
import urwid

import yaml

import pycanstruct

class MsgRecord(object):
    def __init__(self):
        self.arb_id = None
        self.data = None
        self.msg_count = 0
        self.last_message_timestamp = 0
        self.rate_buf = []
        self._rate = None

    def _update_rate(self):
        if len(self.rate_buf) < 2:
            return
        delta_t = (self.rate_buf[-1] - self.rate_buf[0])
        count = float(len(self.rate_buf))
        self._rate = count / delta_t

    @property
    def rate(self):
        return self._rate

    def is_stale(self):
        max_delay = (1.0 / self.rate * 4.0)
        if (time.time() - self.last_message_timestamp) > max_delay:
            return True
        return False


    def update(self, message):
        self.arb_id = message.arbitration_id
        self.data = message.data
        self.msg_count += 1
        self.last_message_timestamp = time.time()
        self.rate_buf.append(self.last_message_timestamp)
        if len(self.rate_buf) > 10:
            del self.rate_buf[0]
        self._update_rate()

class MessagesWalker(urwid.ListWalker):
    def __init__(self):
        self.msgs = OrderedDict()
        self.pos = 0
        pass

    def build(self, ix):
        if ix >= len(self.msgs):
            return None

        message_key = self.msgs.keys()[ix]
        message_rec = self.msgs[message_key]

        id_wgt = urwid.Pile([
                urwid.Button('{}'.format(ix))
            ]
        )

        arb_id = canstruct_object.decode_arbid(message_key)
        arb_id_hex = '0x{:08X}'.format(message_key)

        items = []
        items.append(urwid.Text('{}'.format(arb_id_hex)))
        for id, value in arb_id.iteritems():
            items.append(urwid.Text('{}: {}'.format(id, value)))

        arb_id_wgt = urwid.Pile(
                items
        )
        nominal=True

        data_hex = ' '.join('{:02x}'.format(m) for m in message_rec.data)

        msg_type = canstruct_object.identify_message_type(arb_id);
        if msg_type is None:
            msg_text = data_hex
            data_wgt = urwid.Text('{}'.format(msg_text))
            nominal=False
        else:
            decoded_msg = canstruct_object.decode_message(msg_type, message_rec.data)
            items = []

            items.append(urwid.Text('{}'.format(data_hex)))
            items.append(urwid.Text('{}'.format(msg_type)))

            for id, value in decoded_msg.iteritems():
                value_str = '{0:.2f}'.format(value)
                items.append(urwid.Text('  {}: {}'.format(id, value_str)))

            data_wgt = urwid.Pile(
                    items
            )

        count_wgt = urwid.Text('{}'.format(message_rec.msg_count))

        rate_str = "?"
        if message_rec.rate is not None:
            if message_rec.is_stale():
                rate_str = 'stale'
            else:
                rate_str = '{0:.2f}'.format(message_rec.rate)

        rate_wgt = urwid.Text('{}'.format(rate_str))

        received_tm = time.time() - message_rec.last_message_timestamp
        time_str = '{0:.2f}'.format(received_tm)
        time_wgt = urwid.Text('{}'.format(time_str))

        if nominal:
            return urwid.AttrMap(
                urwid.Columns([id_wgt,count_wgt, rate_wgt, arb_id_wgt, data_wgt, time_wgt] ),  'inactive_item', 'active_item'
            )
        else:
            return urwid.AttrMap(
                urwid.Columns([id_wgt,count_wgt, rate_wgt, arb_id_wgt, data_wgt, time_wgt] ),  'err_inactive_item', 'err_active_item'
            )

    def get_next(self, position):
        if position+1 >= len(self.msgs):
            return None, None
        new_pos = position+1
        return self.build(new_pos), new_pos

    def get_prev(self, position):
        if position == 0:
            return None, None
        new_pos = position-1
        return self.build(new_pos), new_pos

    def set_focus(self, position):
        self.pos = position
        #pass

    def get_focus(self):
        return self.build(self.pos), self.pos

walker  = MessagesWalker()

header = urwid.AttrMap(urwid.Columns([urwid.Text('#'),urwid.Text('Packet Count'), urwid.Text('Receive Rate (Hz)'), urwid.Text('Arbitration ID'), urwid.Text('Data'), urwid.Text('Timestamp')] ), 'banner')
listbox = urwid.ListBox(walker)
footer = urwid.Columns([urwid.Text('Search'), urwid.Text('Send Mesage')] )
stat = urwid.Columns([urwid.Text('CAN Status: Error-Active'), urwid.Text('Receive Error Counter: 0'), urwid.Text('Transmit Error Counter: 0')] )


footer_text = ('foot', [
    "CAN Monitor",
    ('key', "F8"), " quit",
    ])

def unhandled_keypress(k):
    if k == "f8":
        raise urwid.ExitMainLoop()

footer = urwid.AttrWrap(urwid.Text(footer_text), "foot")


palette = [
    ('banner', 'white', 'dark cyan'),
    ('active_item', 'white', 'dark blue'),
    ('inactive_item', 'white', 'black'),
    ('err_active_item', 'light red', 'dark blue'),
    ('err_inactive_item', 'light red', 'black'),
    ('bg', 'dark blue', 'black'),
    ('foot','dark cyan', 'dark blue', 'bold'),
]

main_window = urwid.Frame(listbox, header=header, footer=footer)

main_loop = urwid.MainLoop(main_window, palette,unhandled_input=unhandled_keypress)

parser = argparse.ArgumentParser(description='CANStruct CAN Packets Monitor')
parser.add_argument(
    'interface',
    help='SocketCAN interface to send and receive data'
)
parser.add_argument(
    'config',
    help='filename of CANStruct yaml configuration file with packet definition'
)

args = parser.parse_args()

cfg = yaml.load(open(args.config, 'r'))
canstruct_object = pycanstruct.CANStruct(cfg[cfg.keys()[0]]);

def updater():
    while 1:
        time.sleep(0.5)
        walker._modified()
        listbox._invalidate()
        main_loop.draw_screen()


def receiver():
    while 1:
        bus = can.interface.Bus(channel=args.interface , bustype='socketcan_ctypes')
        message = bus.recv()
        message_timestamp = time.time()
        msg_rec = None
        if message.arbitration_id in walker.msgs:
            msg_rec = walker.msgs[message.arbitration_id]
        else:
            msg_rec = MsgRecord()
            walker.msgs[message.arbitration_id] = msg_rec

        msg_rec.update(message)




receiver_thread = threading.Thread(target=receiver)
receiver_thread.daemon = True
receiver_thread.start()

updater_thread = threading.Thread(target=updater)
updater_thread.daemon = True
updater_thread.start()


main_loop.run()
