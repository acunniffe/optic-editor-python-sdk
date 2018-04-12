import websocket
import json

try:
    import thread
except ImportError:
    import _thread as thread
import time


class EditorConnection(object):

    def context(self, filepath, start, end, content):
        if self.ws.sock.connected:
            self.ws.send(
                json.dumps({'event': 'context', 'file': filepath, 'start': start, 'end': end, 'content': content}))

    def search(self, filepath, start, end, content, query):
        if self.ws.sock.connected:
            self.ws.send(json.dumps(
                {'event': 'search', 'file': filepath, 'start': start, 'end': end, 'content': content, 'query': query}))

    def onFilesUpdated(self, callback):
        print("ADDED CALLBACK")
        self.filesUpdatedCallbacks.append(callback)

    def _on_message(self, ws, message):
        payload = json.loads(message)
        if payload.event == 'files-updated':
            for c in self.filesUpdatedCallbacks:
                c(message)

        print(message)

    def _on_error(self, ws, error):
        print(error)

    def _on_close(self, ws):
        print(ws)
        print("### closed ###")

    def connect(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://localhost:30333/socket/editor/" + self.name, on_message=self._on_message,
                                         on_error=self._on_error, on_close=self._on_close)
        self.ws.run_forever()

    def __init__(self, name):
        self.name = name
        self.connect()
        self.filesUpdatedCallbacks = []




# connection = EditorConnection("pythonTest")
#
#
# def filesUpdates(value):
#     print("GOT IT")
#     print(value)
#
#
# connection.onFilesUpdated(filesUpdates)
# connection._on_message(0,  "{ 'event': 'files-updated' }")
#
