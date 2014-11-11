import json	
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from models import User,Note

# http://universimmedia.pagesperso-orange.fr/geo/loc.htm
places = [{
	"name": "Home #maison",
	"location" : [49.17970,-0.37282]
},
{
	"name": "School",
	"location" : [49.18375,-0.36809]
},
{
	"name": "#test Library",
	"location" : [49.18014,-0.37074]
},
{
	"name": "University #study",
	"location" : [49.18895, 	-0.36386]
},

{
	"name": "#test Herouville",
	"location" : [49.20103, 	-0.33770]
},

{
	"name": "Ouestream #eau #maison",
	"location" : [49.27666, 	-0.25866]
},
{
	"name": "Rouen",
	"location" : [49.44323, 	1.09997]
	
}]






#DATA is a JSON STRING
def check_json(data):
	results = json.loads(data)
	if "success" not in data:
		raise Warning("Wingo json schema is wrong. success is mandatory")
	return results

def check_success(obj):
	if obj["success"] is False:
		raise Warning(obj["message"])



def generate_data():
	Note.drop_collection()
	User.drop_collection()

	user = User(nickname="test", email="test@test.fr", password="test")
	user.save()

	for place in places:
		Note(location=place["location"], message=place["name"], author=user).save()

	



def print_json(data):
	print (highlight(data, JsonLexer(), TerminalFormatter()))
