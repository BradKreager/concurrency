import threading
import queue as Queue
import globalvars


def dn():
    bell.set()
    msg = "Wait done, bell rung"
    globalvars.message_q.put(msg)

# b = threading.Barrier(3, timeout=5)
b = threading.Barrier(3, timeout=5, action=dn)
ready = threading.Barrier(2, timeout=5)
food_avail = threading.BoundedSemaphore(2)
lock = threading.Lock()
bell_lock = threading.Lock()
wait_for_food = threading.Condition()
chef_ready = threading.Condition()
bell = threading.Event()
next_round = threading.Event()
food_ready = threading.Event()
threads_ready = threading.Event()
