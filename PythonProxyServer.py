from socket import *
from ResponseManager import *
from RequestParser import *
import requests as req

class PythonProxyServer:
    def __init__(self, port):
        self.ip = '0.0.0.0'
        self.port = port
        self.http_header = 'HTTP/1.1 200 OK\n\n'
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.responseManager = ResponseManager()
        self.isValid = True

    def listen(self, backlog):
        self.socket.listen(backlog)
        print("Proxy server started on port " + str(self.port))

    def accept(self):
        self.responseWriter, self.clientAddr = self.socket.accept()
        self.requestStr = self.responseWriter.recv(1024).decode()
        print(self.requestStr)
        reqParser = RequestParser(self.requestStr)
        self.url = reqParser.getReqUrl()
        self.host = reqParser.getReqHost()
        self.isBlockedHost(self.host)
        self.isBlockedKeyword(self.url)
        self.forwardRequest()

    def isBlockedHost(self, hostName):
        if hostName == "yahoo.com":
            msg = self.responseManager.getBlockedWebsitePage()
            self.isValid = False
            self.responseWriter.sendall(msg.encode("utf-8"))
            self.responseWriter.close()
        else:
            self.responseWriter.sendall(self.http_header.encode("utf-8"))

    def isBlockedKeyword(self, url):
        if "movies" in str(url):
            msg = self.responseManager.getBlockedKeywordPage()
            self.isValid = False
            self.responseWriter.sendall(msg.encode("utf-8"))
            self.responseWriter.close()

    def forwardRequest(self):
        if self.isValid:
            try:
                header = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh: Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
                }
                resp = req.get(url=self.url, headers=header)
                self.responseWriter.sendall(resp.content)
            except Exception as e:
                print(e)

if __name__ == '__main__':
    proxy = PythonProxyServer(2647)
    proxy.listen(5)
    while True:
        proxy.accept()
