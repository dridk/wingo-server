 
 from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# TOOLS				 													    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# color in shell
class bC:
	H = '\033[95m' # Header 	(purple)
	O = '\033[92m' # Ok 		(green)
	W = '\033[93m' # Warning 	(Yellow)
	F = '\033[91m' # Fail 		(Red)
	E = '\033[0m'  # -end


# Print messages
def msg(message):
	if args.verbose:
		print message

def error(message, exception=None):
	if args.verbose:
		print bC.F + "Error : " + bC.E + message
		if exception is not None:
			print bC.F + "Exception : " + bC.E + exception.message

def warn(message):
	if args.verbose:
		print bC.W + "Warning : " + bC.E + message


def head(message):
	if args.verbose:
		print bC.H + " - " + message + bC.E

def g(message):
	return bC.O + str(message) + bC.E
def y(message):
	return bC.W + str(message) + bC.E
def r(message):
	return bC.F + str(message) + bC.E

def lst2str(theList):
		return '{' + ', '.join(theList) + '}'

