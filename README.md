# REST-Based Locking Service

[![Build Status](https://travis-ci.org/mark-burnett/gsc-lock.png?branch=master)](https://travis-ci.org/mark-burnett/gsc-lock)

The purpose of this project is to provide a replacement for the network disk
based locking system currently in place in the
[Genome Modeling System](https://github.com/genome/gms-core).

## Testing
To run tests, start a local Redis server with default configuration and run:

    pip install tox
    tox