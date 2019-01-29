#!/usr/bin/python3

import time
import MySQLdb

############
SAMPLES = 10000
############


MICROSECONDS_PER_SECOND = 1000000

db = MySQLdb.connect(host='10.108.0.4', user='root', password='foobar')
c = db.cursor()

def MeanExecutionTime(samples):
    start = time.perf_counter()
    for _ in range(samples):
        c.execute('SELECT 1')
    end = time.perf_counter()

    return (end - start) / samples

print('%dus' % (MeanExecutionTime(SAMPLES) * MICROSECONDS_PER_SECOND))
