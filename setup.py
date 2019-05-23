from setuptools import setup

setup(
    name='dot2nn',
    version='0.0.1',
    author='cympfh',
    author_email='cympfh@gmail.com',
    url='https://github.com/cympfh/dot2nn',
    install_requires=[
        'click',
        'rply',
    ],
    packages=['dot2nn', 'dot2nn/compile/'],
    scripts=['bin/dot2nn'],
)
