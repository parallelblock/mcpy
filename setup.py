from setuptools import setup

setup(name='mcpy',
        version='0.1',
        description='Minecraft client/server library',
        url='http://github.com/Ichbinjoe/mcpy',
        author='Ichbinjoe',
        author_email='joe@ibj.io',
        license='MIT',
        packages=['mcpy'],
        keywords=['protocol', 'minecraft', 'bot'],
        scripts=['bin/mcping', 'bin/mclogin'],
        install_requires=['aiohttp', 'aiodns', 'pycrypto', 'nbt', 'rx'],
        classifiers=[])
