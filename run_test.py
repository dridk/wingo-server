#!venv/bin/python 
import unittest 
from test import suite 
from colour_runner.runner import ColourTextTestRunner


ColourTextTestRunner(verbosity=2).run(suite)
