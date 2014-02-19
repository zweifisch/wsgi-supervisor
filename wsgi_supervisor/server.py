import os
import sys
from importlib import import_module
from wsgiref.simple_server import make_server

_, module_path, app_name, port, pwd = sys.argv

if module_path.endswith('.py'):
    module_path = module_path[:-3]
module_path = module_path.replace(os.path.sep, '.')

sys.path.append(pwd)

module = import_module(module_path)

if not hasattr(module, app_name):
    raise Exception("can't find %s in %s" % (app_name, module_path))

print('listen on %s' % port)

make_server('', int(port), getattr(module, app_name)).serve_forever()
