"""
Implementation of a multiprocess TCP server that sorts lists of strings
"""

import sys
import socketserver
import os
from multiprocessing import Process, Queue

class defaults:
    """
    Common default values used throughout the program, possible candidate
    for refactoring into its own sharable module.
    """
    host_name = ""
    port_num = 43802
    tcp_buffsize = 4096

def merge_sort(data):
    """Recursively sorts the specified list via mergesort algorithm"""
    if len(data) < 2: #list is singleton
        return data
    sorted_list = []
    mid_point = int(len(data) / 2) #conversion to int will round for odd lengths
    left_sub = merge_sort(data[:mid_point]) #recursive call on left sublist
    right_sub = merge_sort(data[mid_point:]) #recursive call on right sublist
    left_index = 0
    right_index = 0
    while (left_index < len(left_sub)) and (right_index < len(right_sub)):
        if left_sub[left_index] > right_sub[right_index]: #right element is smaller
            sorted_list.append(right_sub[right_index])
            right_index += 1
        else: #left element is smaller
            sorted_list.append(left_sub[left_index])
            left_index += 1
    sorted_list += left_sub[left_index:]
    sorted_list += right_sub[right_index:]
    return sorted_list

class ForkedClientHandler(socketserver.BaseRequestHandler):
    """Handles multiprocess logic for an a TCP server that accepts ASCII"""
    linesleft = 0
    def handle(self):
        """
        Handler called in child process, once for each client connection.
        """
        client_req = self.request.recv(defaults.tcp_buffsize)
        self.linesleft = int(client_req.strip())
        while self.linesleft > 0:
            client_req = self.request.recv(defaults.tcp_buffsize)
            #converts data to a list of strings, delimited by whitespace
            sorted_list = merge_sort(str(client_req, 'ascii').strip().split())
            str_builder = ""
            for i in sorted_list:
                str_builder = str_builder + i + ' '
            self.request.sendall(str_builder.encode())
            self.linesleft -= 1

class ForkingServerTCP(socketserver.ForkingMixIn, socketserver.TCPServer):
    """Handles Unix fork logic automatically"""
    queueref = None

    def service_actions(self):
        """Runs periodically to check whether the server should shut down"""
        super().service_actions()
        if self.queueref.empty() != True:
            if self.queueref.get() == 'q':
                self.server_close() #Unbinds from socket
                exit(0)
    
    def queued_serve_forever(self, q1):
        """
        Helper method run once per server instance and allows communcation
        between the server processes and the server command line interface.
        """
        self.queueref = q1
        self.serve_forever()

class SortingServer:
    """
    Controller class that initiates and communicates with the background tcp server process.
    """
    host_name = None
    port_number = None
    server_process = None
    comm_queue = None
    is_running = False

    def __init__(self, host_name=defaults.host_name, port_number=defaults.port_num):
        self.host_name = host_name
        if port_number > 1024: #Program should never have permissions to use reserved ports
            self.port_number = port_number
        else:
            print("Invalid port number")
            exit(127) #Maybe change error code
    
    def run(self):
        """Attempts to start up the server on the instances hostname and port number"""
        if self.is_running:
            return #Maybe add error checking
        self.comm_queue = Queue()
        server = ForkingServerTCP((self.host_name, self.port_number), ForkedClientHandler)
        self.server_process = Process(target=server.queued_serve_forever, args=(self.comm_queue,))
        self.server_process.start()
        self.running = True
        print("Server process started on: " + self.host_name  + ":" + str(self.port_number))
        sys.stdout.flush()
    
    def stop(self):
        """Signals the server process to stop gracefully"""
        if self.running != True:
            exit(127) #maybe error check
        self.comm_queue.put('q')
        self.server_process.join()
        print("Server successfully shutdown")

def run_cli():
    """Starts server command line interface"""
    main_server = None
    if len(sys.argv) == 1:
        main_server = SortingServer()
    elif len(sys.argv) == 2:
        main_server = SortingServer(host_name=sys.argv[1])
    elif len(sys.argv) == 3:
        main_server = SortingServer(host_name=sys.argv[1], port_number=int(sys.argv[2]))
    else:
        print("Error: invalid syntax\nUsage:" + sys.argv[0] + " [ip addr] [port number]")
        exit(1)
    main_server.run()
    user_input = input("Enter q to shutdown: ")
    while user_input != 'q':
        user_input = input("Enter q to shutdown: ")
    main_server.stop()

if __name__ == '__main__':
    run_cli()
