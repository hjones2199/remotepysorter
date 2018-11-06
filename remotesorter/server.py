"""
Implementation of a multiprocess TCP server that sorts lists of strings
"""
import sys
import socketserver
import os
from multiprocessing import Process, Queue

def merge_sort(data):
    pass

def merge_sort_recurse(left, right):
    pass

class TCPForkHandler(socketserver.BaseRequestHandler):
    """Handles multiprocess logic for an a TCP server that accepts ASCII"""
    def handle(self):
        """
        Handler called in child process, once for each client connection.
        """
        client_req = self.request.recv(2048)


class ForkingServerTCP(socketserver.ForkingMixIn, socketserver.TCPServer):
    """Handles Unix fork logic automatically"""
    queueref = None

    def service_actions(self):
        """Runs periodically to check whether the server should shut down"""
        super().service_actions()
        pass

def run_cli():
    pass

def main():
    pass

if __name__ == '__main__':
    main()
