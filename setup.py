from setuptools import setup

setup(
    name='wsgi-supervisor',
    url='https://github.com/zweifisch/wsgi-supervisor',
    version='0.0.1',
    description='reload wsgi app on file change',
    author='Feng Zhou',
    author_email='zf.pascal@gmail.com',
    packages=['wsgi_supervisor'],
    install_requires=['pyinotify', 'docopt'],
    entry_points={
        'console_scripts': ['wsgi-supervisor=wsgi_supervisor:main'],
    },
)
