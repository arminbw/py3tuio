# py3tuio

py3tuio is a very basic, crude and compact implementation of a [TUIO](http://www.tuio.org/) 1.x client written in Python 3 using pyliblo. It is restricted to 2D surfaces and does not distinguish between different servers.

## Requirements
The TUIO protocol is based on the OSC (Open Sound Control) protocol. [liblo](https://github.com/radarsat1/liblo) is a popular and lightweight OSC implementation. [Pyliblo](https://github.com/dsacre/pyliblo) is a Python wrapper for liblo.
To use py3tuio in your project, install liblo first, then pyliblo.

You may want to use one or two package managers to do this:

    brew install liblo
    pip3 install pyliblo
	
## Basic use (demo)
Type ```python3 py3tuio.py``` in your terminal.
Get a [TUIO simulator](http://www.tuio.org/?software). Try [TuioPad](https://github.com/mkalten/TuioPad) if you want to capture data from iOS devices.

## Background
[Back in 2012 I couldn't find any TUIO client](http://igw.tuwien.ac.at/ceat/node/15) written in python 3.




