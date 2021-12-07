#

from setuptools import setup

setup(
   name='cereblus',
   version='0.1.0',
   author='Paweł Gadziński',
   webpage='https://github.com/pggPL/cereblus',
   author_email='pawelgadzinski@gmail.com',
   packages=['.cereblus', '.cereblus.neurons', '.cereblus.stimulation', '.cereblus.neural_networks'],
   scripts=['cereblus/__init__.py'],
   license='./LICENSE.txt',
   description='Package for simple neural network simulations.',
   long_description=open('./README.txt').read(),
   install_requires=[
      'tk == 0.1.0'
   ],
)