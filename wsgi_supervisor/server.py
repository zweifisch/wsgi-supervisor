import sys
from importlib import import_module
from wsgiref.simple_server import make_server

_, application, port, cwd = sys.argv

module_path, app_name = application.split(':')

sys.path.append(cwd)

module = import_module(module_path)

if not hasattr(module, app_name):
    raise Exception("can't find %s in %s" % (app_name, module_path))

print('listen on %s' % port)

make_server('', int(port), getattr(module, app_name)).serve_forever()
