# Import modules
import socket
import time
import multiprocessing

# Initlialise variable to track program execution time
start_time = time.time()

# Function to determine whether the host has the `port` open
def is_port_open(port):
    # Creates a new socket
    s = socket.socket()
    try:
        # Tries to connect to host using that port
        s.connect(("scanme.nmap.org", port))
        # Set timeout for connection establishment
        s.settimeout(0.2)
    except:
        # Cannot connect, port is closed
        return False
    else:
        # The connection was established, port is open
        return True
        
# Create new multiprocessing pool object
pool = multiprocessing.Pool()

# Create list of ports to scan
inputs = [i for i in range(1,1024)]

# Map the function to the list and pass inputs
outputs = pool.map(is_port_open, inputs)

# Print open ports and services
print(f"{'PORT':<9}OPEN")
for i in range(len(outputs)):
  if outputs[i]:
    print(f"{inputs[i]:<9}{outputs[i]}")

# Print execution time
print(f"\nRan in {round((time.time() - start_time), 4)}s")