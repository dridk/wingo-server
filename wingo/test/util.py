import json	
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
#from wingo.models import *



#DATA is a JSON STRING
def check_json(data):
	results = json.loads(data)
	if "success" not in data:
		raise Warning("Wingo json schema is wrong. success is mandatory")
	return results

def check_success(obj):
	if obj["success"] is False:
		raise Warning(obj["message"])



def create_user(count = 1):
	user = User()
	user.nickname = "test"
	user.email    = "test@test.fr"
	user.password = "test"
	user.save()
	return user

def print_json(data):
	print highlight(data, JsonLexer(), TerminalFormatter())
