##
#
# Copyright (c) 2014 Matt Molyneaux
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
##
"""yesd - the yes daemon"""

import asyncore
import socket

class YesHandle(asyncore.dispatcher):
    yes = "y\r\n"
    def handle_write(self):
        self.send(self.yes)

class Yes(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print "Connection from %s" % addr
            handle = YesHandle(sock)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        host = "localhost"
        port = 7272
    elif len(sys.argv) == 2:
        host = sys.argv[1]
        if ":" in host:
            host, port = host.split(":")
            port = int(port)
        else:
            port = 7272
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])

    yes = Yes(host, port)
    print "Listening for connections on %s:%s" % (host, port)

    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print "\rExiting..."
