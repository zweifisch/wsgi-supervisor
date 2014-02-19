# wsgi supervisor

reload wsgi application when code changed, should be used in development enviroment

it uses inotify, so only works on linux

```sh
Usage: wsgi-supervisor [options] <file>

Options:
    -e, --extensions=exts    only file with those extensions will be watched
                             [default: py]
    -w, --watch=folders      folders to watch
    -a, --app=appname        app name to import [default: app]
    -d, --pwd=path           path to app folder
    -p, --port=port          port to bind [default: 3000]
    --python=python          python excutable [default: python]

Examples:
    wsgi-supervisor app.py
    wsgi-supervisor -e js,py -w public/js,controllers app.py
```

install via pip

```sh
pip install wsgi-supervisor
```
