try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='linptech',
    version='0.1.3',
    description='Linptech serial protocol',
    author='yangzhan',
    author_email='728074993@qq.com',
    url='https://github.com/yangguozhanzhao/linptech',
    packages=[
        'linptech',
    ],
    scripts=[
        'example.py',
    ],
    install_requires=[
        'pyserial>=3.0',
    ])
