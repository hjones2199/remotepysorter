#!/usr/bin/env python3
"""
TCP client implementation that reads words from a file line by line
and asks the server to sort the words alphabetically on a per line basis.
"""
import socket

class defaults:
    """
    Common default values used throughout the program, possible candidate
    for refactoring into its own sharable module.
    """
    host_name = ""
    port_num = 43802
    tcp_buffsize = 4096

def file_len(file_name):
    """Returns number of lines in a file"""
    with open(file_name, "r") as file_ref:
        for i, l in enumerate(file_ref):
            pass
    return i + 1

def query_server(file_name, ip, port, tcp_buffsize):
    """
    Sends a string to the server over TCP and returns True
    or False as a string depending on whether the server
    detected that the string is a palindrome.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(str(file_len(file_name)).encode()) #sends number of incoming lines to server
    with open(file_name, "r") as file_ref:
        for msg in file_ref:
            if str(sock.recv(defaults.tcp_buffsize), 'ascii') != "OK":
                print("Error: protocol mismatch")
            sock.sendall(msg.encode())
            reply = sock.recv(defaults.tcp_buffsize)
            print(str(reply, 'ascii').strip())
    sock.close()

def term_interface():
    """
    TODO
    """
    tcp_buffsize = defaults.tcp_buffsize #not configurable in current server implementation without editing code
    host_name = input("Enter hostname or ip address of line sort server: ")
    port_input = input("Enter port number of line sort (" + str(defaults.port_num) + " by default): ")
    port_num = 0
    if port_input == '':
        port_num = defaults.port_num
    else:
        port_num = int(port_input)
    
    infile_name = ""
    while(True):
        infile_name = input("Enter a filename to sort or q to quit: ")
        if infile_name == 'q':
            return
        else:
            query_server(infile_name, host_name, port_num, tcp_buffsize)

def main():
    term_interface()

if __name__ == '__main__':
    main()
