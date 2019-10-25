from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime
from time import sleep

def get_time(counter):
    return 'Counter: ' + str(counter)

def sent_message(pipe, counter, i):
    counter[i] += 1
    pipe.send(('', counter))
    return counter

def recv_message(pipe, counter, it):
    _, n_counter = pipe.recv()
    for i in range(len(counter)):
        counter[i] = max(n_counter[i], counter[i])
    counter[it] += 1
    return counter

def event(counter, i):
    counter[i] += 1
    return counter

def process_a(pipe_ab):
    counter = [0,0,0]
    i = 0
    counter = sent_message(pipe_ab, counter, i)
    counter = sent_message(pipe_ab, counter, i)
    counter = event(counter, i)
    counter = recv_message(pipe_ab, counter, i)
    counter = event(counter, i)
    counter = event(counter, i)
    counter = recv_message(pipe_ab, counter, i)
    print("Process a: {}".format(counter))

def process_b(pipe_ba, pipe_bc):
    counter = [0,0,0]
    i = 1
    counter = recv_message(pipe_ba, counter, i)
    counter = recv_message(pipe_ba, counter, i)
    counter = sent_message(pipe_ba, counter, i)
    counter = recv_message(pipe_bc, counter, i)
    counter = event(counter, i)
    counter = sent_message(pipe_ba, counter, i)
    counter = sent_message(pipe_bc, counter, i)
    counter = sent_message(pipe_bc, counter, i)
    print("Process b: {}".format(counter))

def process_c(pipe_cb):
    counter = [0,0,0]
    i = 2
    counter = sent_message(pipe_cb, counter, i)
    counter = recv_message(pipe_cb, counter, i)
    counter = event(counter, i)
    counter = recv_message(pipe_cb, counter, i)
    print("Process c: {}".format(counter))


if __name__ == '__main__':
    a_b, b_a = Pipe()
    b_c, c_b = Pipe()

    processes = []

    processes.append(Process(target=process_a, args=(a_b, )))
    processes.append(Process(target=process_b, args=(b_a, b_c)))
    processes.append(Process(target=process_c, args=(c_b, )))

    for pr in processes:
        pr.start()

    for pr in processes:
        pr.join()

    

    