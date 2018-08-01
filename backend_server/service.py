"""Service backend"""

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import operations

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

def add(num1, num2):
    """Test method"""
    print("Add is called with %d and %d" % (num1, num2))
    return num1 + num2

def get_one_news():
    """Get one news"""
    print("get_one_news is called.")
    return operations.get_one_news()

def get_news_summaries_for_user(user_id, page_num):
    """Get news summaries"""
    print("get_news_summaries_for_user is called with %s and %s" % (user_id, page_num))
    return operations.get_news_summaries_for_user(user_id, page_num)

# Setup the server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(get_one_news, 'get_one_news')
RPC_SERVER.register_function(get_news_summaries_for_user, 'get_news_summaries_for_user')

print("Starting RPC server on %s:%d" % (SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()
