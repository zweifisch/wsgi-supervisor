# wsgi supervisor

reload wsgi application when code changed, should be used in development enviroment

depends on inotify, so only works on linux

```sh
Usage: wsgi-supervisor [options] <module:app>

Options:
    -e, --extensions=exts    only file with those extensions will be watched
                             [default: py]
    -w, --watch=folders      folders to watch
    -c, --cwd=dir            change dir before running app
    -p, --port=port          port to bind [default: 3000]
    --python=python          python excutable [default: python]

Examples:
    wsgi-supervisor wsgi:app
    wsgi-supervisor -e js,py -w public/js,controllers main:app
```

install via pip

```sh
pip install wsgi-supervisor
```
