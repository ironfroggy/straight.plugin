from multiprocessing import Process, Pipe


def _proxy_main(pipe):
    ppc = PluginProxyChild(pipe)
    ppc.run()


class PluginProxy(object):
    """Manages a plugin running in an external process."""

    def __init__(self):
        self.parent_conn, self.child_conn = Pipe()
        self.process = Process(target=_proxy_main, args=(self.child_conn,))
        self.process.start()
        self._inst_num = 0
        self._callbacks = {}

    def _send_instruction(self, inst, args, kwargs, callback=None):
        self._inst_num += 1
        n = self._inst_num
        if callback is not None:
            self._callbacks[n] = callback
        self.parent_conn.send((n, inst, args, kwargs))

    def _handle_one_response(self):
        if self.parent_conn.poll():
            n, resp = self.parent_conn.recv()
            try:
                callback = self._callbacks.pop(n)
            except KeyError:
                return
            callback(resp)

    def handle_responses(self):
        while self.parent_conn.poll():
            self._handle_one_response()


class PluginProxyChild(object):

    def __init__(self, pipe):
        self.pipe = pipe
        self.modules = []

    def run(self):
        while True:
            n, inst, args, kwargs = self.pipe.recv()
            handler = getattr(self, 'inst_' + inst)
            r = handler(*args, **kwargs)
            self.pipe.send((n, r))

    def inst_echo(self, x):
        return x

