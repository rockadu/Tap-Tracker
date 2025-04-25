from collections import defaultdict
from pprint import pformat
from threading import Lock
import datetime

buffer_input = defaultdict(lambda: {"MouseClicks": 0, "KeyPresses": 0, "MouseScroll": 0})
lock = Lock()

def add_input_event(event_type, logged_user):
    with lock:
        current_minute = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        buffer_input[(current_minute, logged_user)][event_type] += 1
        txt = pformat(buffer_input)
        print("Estado do buffer:\n" + txt)

def flush_buffer():
    with lock:
        flushed_data = dict(buffer_input)
        print(f'dados atuais no buffer: {flushed_data}')
        buffer_input.clear()
        print (f'buffer limpo: {buffer_input}')
    return flushed_data