#!/usr/bin/env python
#coding: UTF-8

import json
import logging
import os
import sys
import unittest
from operator import add, mul

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '..')
from pyrpcsyncwerk import (
    NamedPipeClient, NamedPipeServer, RpcsyncwerkClient, RpcsyncwerkError,
    RpcsyncwerkTransport, rpcsyncwerk_func, rpcsyncwerk_server
)

SVCNAME = 'test-service'


def init_server():
    rpcsyncwerk_server.create_service(SVCNAME)
    rpcsyncwerk_server.register_function(SVCNAME, add, 'add')
    rpcsyncwerk_server.register_function(SVCNAME, mul, 'multi')
    rpcsyncwerk_server.register_function(SVCNAME, json_func, 'json_func')

def json_func(a, b):
    return {'a': a, 'b': b}


class DummyTransport(RpcsyncwerkTransport):
    def connect(self):
        pass

    def send(self, service, fcall_str):
        return rpcsyncwerk_server.call_function(service, fcall_str)

class RpcMixin(object):
    @rpcsyncwerk_func("int", ["int", "int"])
    def add(self, x, y):
        pass

    @rpcsyncwerk_func("string", ["string", "int"])
    def multi(self, x, y):
        pass

    @rpcsyncwerk_func("json", ["string", "int"])
    def json_func(self, x, y):
        pass

class DummyRpcClient(RpcsyncwerkClient, RpcMixin):
    def __init__(self):
        self.transport = DummyTransport()

    def call_remote_func_sync(self, fcall_str):
        return self.transport.send(SVCNAME, fcall_str)

class NamedPipeClientForTest(NamedPipeClient, RpcMixin):
    pass


SOCKET_PATH = '/tmp/librpcsyncwerk-test.sock'


class RpcsyncwerkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_server()
        cls.client = DummyRpcClient()

        cls.named_pipe_server = NamedPipeServer(SOCKET_PATH)
        cls.named_pipe_server.start()
        cls.named_pipe_client = NamedPipeClientForTest(SOCKET_PATH, SVCNAME)

    @classmethod
    def tearDownClass(cls):
        cls.named_pipe_client.stop()
        cls.named_pipe_server.stop()

    def test_normal_transport(self):
        self.run_common(self.client)

    # @unittest.skip('not implemented yet')
    def test_pipe_transport(self):
        self.run_common(self.named_pipe_client)

    def run_common(self, client):
        v = client.add(1, 2)
        self.assertEqual(v, 3)

        v = client.multi(1, 2)
        self.assertEqual(v, 2)

        v = client.multi('abc', 2)
        self.assertEqual(v, 'abcabc')

        v = client.json_func(1, 2)
        self.assertEqual(v, json_func(1, 2))

def setup_logging(level=logging.INFO):
    kw = {
        # 'format': '[%(asctime)s][%(pathname)s]: %(message)s',
        'format': '[%(asctime)s][%(module)s]: %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': level,
        'stream': sys.stdout
    }

    logging.basicConfig(**kw)


if __name__ == '__main__':
    setup_logging()
    unittest.main()
