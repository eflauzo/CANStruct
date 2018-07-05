
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='canstruct',
    version='0.1.0',
    description='YAML based CAN message definition and code generation',
    author='Denys Metelskyy',
    scripts=['canstruct/canstruct_gen_c.py'],
    author_email='denys.y.metelskyy@gmail.com',
    url='https://github.com/eflauzo/CANstruct',
    license='MIT',
    packages=['canstruct']
)
