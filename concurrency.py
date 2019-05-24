#!/usr/bin/python3
import sys
import random
import time
import collections
import threading
import queue as Queue
import locks
import globalvars
from threads import chef_thread as chef
from threads import customer_thread as customer
from threads import messenger, hamburger, fries, soda



if __name__ == "__main__":
    closeup = False
    menu=("HAMBURGER", "FRIES", "SODA")

    food_queue = Queue.Queue()
    customer_line = Queue.Queue()
    message_q = Queue.Queue()

    next_item = None

    chef = chef(name="Carl", menu=menu, cond=locks.wait_for_food,
                queues=food_queue)

    customers = [
    customer(name="cust1", menu=menu, lock=locks.lock, queues=food_queue,
             next_item=next_item, orders=(fries(), soda())),
    customer(name="cust2", menu=menu, lock=locks.lock, queues=food_queue,
             next_item=next_item, orders=(hamburger(), soda())),
    customer(name="cust3", menu=menu, lock=locks.lock, queues=food_queue,
             next_item=next_item, orders=(hamburger(), fries())),
    ]

    msgs = messenger()
    msgs.start()


    try:
        chef.start()
        print("Chef {} opened restaurant".format(chef.name))
        for customer in customers:
            customer.start()
            print("Customer {} arrived".format(customer.name))

        print("\n")

        while chef.food_count < 200:
            locks.bell.set()
            sys.stdout.write("{} meals served\r".format(chef.food_count))
            sys.stdout.flush()
            # if chef.food_count == 196:
                # break
            while not food_queue.empty():
                item = food_queue.get()
                for customer in customers:
                    with locks.lock:
                        if customer.process_item(item):
                            food_queue.task_done()
                            break

            locks.next_round.set()




    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error: {}".format(e))
        chef.close_shop()
    finally:
        print("\n")
        chef.close_shop()
        for customer in customers:
            customer.set_done()
        for customer in customers:
            customer.join()
            print("{} has left".format(customer.name))
        chef.join()
        print("{} went home".format(chef.name))
        print("\n")
        print("STATS")
        print("="*20)
        for customer in customers:
            print("{} ate {} times".format(customer.name, customer.times_ate))
            globalvars.message_q.put("{} ate {} times".format(customer.name, customer.times_ate))
        globalvars.message_q.put("Chef {} made {} dishes".format(chef.name, chef.food_count))
        print("\nChef {} made {} dishes".format(chef.name, chef.food_count))
        for item, count in chef.item_count.items():
            print("{}: {}".format(item, count))
            globalvars.message_q.put("{}: {}".format(item, count))
        msgs.stop()
        msgs.join()
        sys.exit(0)
