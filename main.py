# Import modules
import socket
import time
import datetime, pytz
from getservice import getservbyport

from threading import Thread, Lock
from queue import Queue

# Initlialise variable to track program execution time
start_time = time.time()

# Define number of threads and initialise queue and lock
N_THREADS = 150
q = Queue()
append_lock = Lock()

# Define global array to store open ports
openPorts = []

# Function to scan a `port` on the `host`
def port_scan(port):
    try:
        s = socket.socket()
        s.connect((host, port))
    except:
        pass
    else:
        # add the port to the list of open ports
        with append_lock:
            openPorts.append(port)
    finally:
        s.close()

# Function to get the next port number and scan it
def scan_thread():
    global q
    while True:
        # get the next port number from the queue
        currentPort = q.get()
        # scan that port number
        port_scan(currentPort)
        # tell the queue that the scanning for that port is done
        q.task_done()

# Function to initialise threads and add ports to the queue to scan
def run_scan(host, ports):
    global q
    for t in range(N_THREADS):
        # for each thread, start it
        t = Thread(target=scan_thread)
        # set daemon to true so each thread will end when the main thread ends
        t.daemon = True
        # start the daemon thread
        t.start()

    for worker in ports:
        # for each port, put that port into the queue to start scanning
        q.put(worker)
    
    # wait for the threads (port scanners) to finish
    q.join()

# Function to output scan report
def output(host, ports):
  # Print open ports and services
  print(f"Scan report for {host} ({socket.gethostbyname(host)})")
  print("Showing open tcp ports")
  print(f"{'PORT':<11}{'STATE':<7}SERVICE")
  for port in openPorts:
    print(f"{str(port)+'/tcp':<11}{'open':<7}{getservbyport(port, 'tcp')}")
  
  # Print execution time
  print(f"\nPort Scan complete: scanned in {round((time.time() - start_time), 2)} seconds")

# Set host and port range and begin scan
if __name__ == "__main__":
    host = "scanme.nmap.org"
    start_port = 1
    end_port = 65535
    ports = [p for p in range(start_port, (end_port + 1))]
    print("Starting Port Scan at", (datetime.datetime.now((pytz.timezone("Europe/London")))).strftime("%Y-%m-%d %H:%M %Z"))
    run_scan(host, ports)
    output(host, ports)