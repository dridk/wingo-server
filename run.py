import os
from flask import Flask
from wingo import create_app 
app = create_app("devel")


if __name__ == "__main__":
	app.run()

