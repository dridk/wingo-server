from flask.ext.script import Manager

from wingo.application import app

manager = Manager(app)

@manager.command
def hello():
    print "hello"

@manager.command
def run():
	app.run(debug=True, host="0.0.0.0")



if __name__ == "__main__":
    manager.run()