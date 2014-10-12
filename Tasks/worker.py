#!/usr/bin/env python
import sys
from rq import Queue, Connection, Worker

# Preload libraries
import library_that_you_want_preloaded

# Starting up a queue
with Connection():
    qs = map(Queue, sys.argv[1:]) or [Queue()]

    w = Worker(qs)
    w.work()