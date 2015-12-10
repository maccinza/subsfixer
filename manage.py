# -*- coding: utf-8 -*-
u"""

"""
__author__ = 'infante'

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask.ext.script import Manager, Server
from app import app

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '127.0.0.1')
)

if __name__ == "__main__":
    from views import *
    manager.run()
