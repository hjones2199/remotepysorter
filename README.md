**Client Usage**
    The client program is found at client/remotesorter_client.py, and requires
no command line arguments. When run, the client will prompt the user for the
ip address and port number of the server. It will then attempt to establish
a connection and prompt the user for a file to send to the server for sorting.

**Server Usage**
    The server is found at server/remotesorter_server.py, and can either take no
arguments or exactly 2 arguments *IP_ADDR* *PORT*. If no command
line arguments are given it will bind to all IP addresses at port 43802. The server
can be shut down by inputting q.

**Dependencies**
    Both the server and the client require python3 to run correctly. The server relies
heavily on python3 specific features, namely the socketserver module and the object oriented
multiprocessing implementation. The server also relies on a Unix specific multiprocess
system based on the Posix *fork()* system call. I have tested it on multiple Linux
distributions and FreeBSD, but it should run on any POSIX compliant system.

**Notes**
    Lucky for me, most of the boilerplate of my multiprocess palindrome client/server program
was easily modified and integrated into this project, so some of the structure may seem familiar.
The test files are found in the datafiles folder, and each one has three lines with twenty words
per line.
