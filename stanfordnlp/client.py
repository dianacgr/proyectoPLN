import json
# from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
from pprint import pprint


class StanfordNLP:
    def __init__(self, port_number=3456):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

nlp = StanfordNLP()
result = nlp.parse("Hola mundo. Esto es hermoso.")
#~ pprint(result)

from nltk.tree import Tree
tree = Tree.parse(result['sentences'][1]['parsetree'])
#~ pprint(result['sentences'][1]['parsetree'])
