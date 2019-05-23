import threading
import sys
import time
import random
import queue as Queue
import copy
import locks
import globalvars



class chef_thread(threading.Thread):
    """        """
    def __init__(self, name = "chef", menu = None, cond = None, queues = None):
        """                """
        threading.Thread.__init__(self)
        self.name = name
        self._done = threading.Event()
        self._next = threading.Event()
        self._statlock = threading.Lock()
        self.state = "WAITING"
        self.menu = menu
        self.food_queue = queues
        self.food_count = 0


    def run(self):
        while True:
            # locks.next_round.wait()


            # locks.food_ready.clear()
            locks.bell.wait(timeout=0.5)

            if self._done.is_set():
                break

            self.make_food()

            locks.food_ready.set()
            with self._statlock:
                self.food_count += 2
            # print("{}".format(self.food_count))
            # self.food_queue.join()
            locks.bell.clear()
            locks.next_round.clear()





    def close_shop(self):
        self._done.set()


    def make_food(self):
        self.state = "COOKING"
        items = len(self.menu) - 1
        prepared = ()
        for _ in range(items):
            item = random.randint(0, items)
            while self.menu[item] in prepared:
                item = random.randint(0, items)

            prepared += self.menu[item],

            food = self.menu[item]
            if food == "HAMBURGER":
                send_out = hamburger()
            elif food == "FRIES":
                send_out = fries()
            elif food == "SODA":
                send_out = soda()

            self.food_queue.put(send_out, block=False)
            msg = "Sending out {}..".format(send_out)
            globalvars.message_q.put(msg)







class customer_thread(threading.Thread):
    """        """
    def __init__(self, name = "customer", orders = None, menu = None, line = \
                 None, lock = None, bell = None, next_item = None, queues = None):
        """                """
        threading.Thread.__init__(self)
        self.name = name
        self._done = False
        self._waiting = threading.Event()
        self.state = "HUNGRY"
        self.menu = menu
        self.orders = orders
        self.times_ate = 0
        self.line = line
        self.bell = bell
        self.next_item = next_item
        self.tries = 0
        self.food_queue = queues
        self.plate = []
        self.inlock = threading.Lock()



    def run(self):
        while True:
            # self.state = "HUNGRY"
            # globalvars.thread_state.put("SYN")
            # locks.next_round.wait()
            time.sleep(0.5)
            if self._done:
                msg = "Done"
                globalvars.message_q.put(msg)
                break

    # def run(self):
        # items = []
        # while True:
            # self.state = "HUNGRY"
            # globalvars.thread_state.put("SYN")
            # locks.next_round.wait()
            # if self._done:
                # msg = "Done"
                # globalvars.message_q.put(msg)
                # break

            # msg = "{} is waiting".format(self.name)
            # globalvars.message_q.put(msg)

            # locks.b.wait()

            # if self.eat():
                # del items[:]
                # items = []

            # locks.next_round.clear()
            # locks.threads_ready.clear()
            # locks.food_ready.wait()

            # with locks.lock:
                # msg = "{} has lock {}".format(self.name, locks.lock.locked())
                # globalvars.message_q.put(msg)
                # try:
                    # if self.food_queue.empty():
                        # msg = "{} sees no food".format(self.name)
                        # globalvars.message_q.put(msg)
                        # self.state = "DONE"
                    # while not self.food_queue.empty():
                        # next_item = self.food_queue.get()
                        # items.append(copy.deepcopy(next_item))
                # except Exception as e:
                    # print("{}".format(e))
                # else:
                    # if self.state == "HUNGRY":
                        # msg = "{} has new items {}".format(self.name, items)
                        # globalvars.message_q.put(msg)

                        # for item in items:
                            # if self.wants(item):
                                # msg = "{} took {}".format(self.name, item)
                                # globalvars.message_q.put(msg)

                                # self.take_item(item)

                                # msg = "{} is {}".format(self.name, self.state)
                                # globalvars.message_q.put(msg)

                                # try:
                                    # self.food_queue.task_done()
                                # except:
                                    # pass
                            # else:
                                # msg = "{} put back {} has {}".format(self.name, item,
                                                                     # self.plate)
                                # globalvars.message_q.put(msg)
                                # self.food_queue.put(copy.deepcopy(item))

                                # try:
                                    # self.food_queue.task_done()
                                # except:
                                    # pass


    def process_item(self, item):
        result = False
        if self.wants(item):
            self.take_item(item)
            result = True

        self.eat()
        return result


    def take_item(self, item):
        cpy = copy.deepcopy(item)
        self.plate.append(cpy)
        globalvars.message_q.put("{} took {}".format(self.name, self.plate))



    def wants(self, item):
        if item in self.orders and item not in self.plate:
            return True
        else:
            return False



    def eat(self):
        if len(self.plate) == 2:
            globalvars.message_q.put("{} eating {}".format(self.name, self.plate))
            del self.plate[:]
            self.plate = []
            self.times_ate += 1
            return True
        return False



    def pause(self):
        self.state = "WAITING"
        self.paused = True


    def set_done(self):
        # with self.inlock:
        self._done = True

    def go_home(self):
        self.set_done()



    def ring_bell(self, event):
        event.set()






class food:
    def __init__(self):
        self.consumed = False

    def consumed(self):
        return self.consumed





class hamburger(food):
    def __init__(self):
        self.name = "HAMBURGER"

    def __repr__(self):
        return "HAMBURGER"

    def __eq__(self, obj):
        return isinstance(obj, hamburger) and obj.name == self.name

    def __ne__(self, obj):
        return not self.__eq__(obj)





class soda(food):
    def __init__(self):
        self.name = "SODA"

    def __repr__(self):
        return "SODA"

    def __eq__(self, obj):
        return isinstance(obj, soda) and obj.name == self.name

    def __ne__(self, obj):
        return not self.__eq__(obj)





class fries(food):
    def __init__(self):
        self.name = "FRIES"

    def __repr__(self):
        return "FRIES"

    def __eq__(self, obj):
        return isinstance(obj, fries) and obj.name == self.name

    def __ne__(self, obj):
        return not self.__eq__(obj)





class messenger(threading.Thread):
    """        """
    def __init__(self, name = "messages"):
        """                """
        threading.Thread.__init__(self)
        self.name = name
        self._done = threading.Event()
        # self.daemon = True



    def run(self):
        with open("output.txt", mode='w') as f:
            try:
                while not self._done.is_set():
                    try:
                        recvd = globalvars.message_q.get(timeout=0.5)
                    except Queue.Empty:
                        pass
                    else:
                        f.write("MSG: {}\n".format(recvd))
                        # print("MSG: {}".format(recvd))
                        globalvars.message_q.task_done()
            except:
                pass
            else:
                self.empty_q(f)
            # finally:
                # return
                # f.flush()
                # f.close()


    def empty_q(self,f):
        while not globalvars.message_q.empty():
            recvd = globalvars.message_q.get(timeout=0.1)
            f.write("MSG: {}\n".format(recvd))
            # print("MSG: {}".format(recvd))
            globalvars.message_q.task_done()


    def stop(self):
        self._done.set()

