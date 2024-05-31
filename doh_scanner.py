import os
import sys
import operator
import requests
import random
import queue
import threading

import dns.resolver

n_thread = 5
timeout = 4


ok = "\033[1;32mok\033[0m"
filtered = "\033[1;35mfiltered\033[0m"
bad_ping = "\033[1;35mbad ping\033[0m"
all_doh = []
# ok_doh = []
shuffle = True
threads = []

q = queue.Queue()


def resolve_ip(doh_url):
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.nameservers = [doh_url]
    try:
        # Perform the DNS resolution
        answers = resolver.resolve("google.com", 'A')
        # Extract and print the IP addresses
        for rdata in answers:
            print(f"{doh_url}, Status: {ok}")
            # ok_doh.append(doh_url)
            with open("tested-doh.txt", 'a') as f:
                f.write(f"{doh_url}\n")
            break
    except Exception as e:
        print(f"{doh_url} {filtered} or {bad_ping}!")


def worker(q):
    while True:
        try:
            url = q.get(block=False)
        except queue.Empty:
            break
        resolve_ip(url)
        q.task_done()


with open("doh_list.txt", "r") as doh_file:
    for doh in doh_file.readlines():
        all_doh.append(doh.strip())


if shuffle:
    random.shuffle(all_doh)


for doh in all_doh:
    q.put(doh)

for i in range(n_thread):
    t = threading.Thread(target=worker, args=(q,))
    threads.append(t)

for t in threads:
    t.start()

q.join()
