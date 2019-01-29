#!/usr/bin/python3

import time
import MySQLdb

############
LOW_ROWS = 500
HIGH_ROWS = 1000
SAMPLES = 100
############


MICROSECONDS_PER_SECOND = 1000000

db = MySQLdb.connect(host='35.235.123.231', user='root', password='foobar', db='benchmark')
c = db.cursor()

c.execute('DROP TABLE IF EXISTS pullrows')
c.execute('''
CREATE TABLE pullrows (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
) ENGINE=InnoDB
''')
c.execute('INSERT INTO pullrows VALUES (1)')

c.execute('DROP PROCEDURE IF EXISTS pullrows')
c.execute('''
CREATE PROCEDURE pullrows (IN num INT)
BEGIN
	DECLARE x INT;
	SET x = 0;
	WHILE x < num DO
                SELECT * FROM pullrows WHERE id=1;
		SET X = x + 1;
	END WHILE;
END
''')

def MeanExecutionTime(rows, samples):
    start = time.perf_counter()
    for _ in range(samples):
        c.execute('CALL pullrows(%d)' % rows)
    end = time.perf_counter()

    return (end - start) / samples

diff = MeanExecutionTime(HIGH_ROWS, SAMPLES) - MeanExecutionTime(LOW_ROWS, SAMPLES)
per_row = diff / (HIGH_ROWS - LOW_ROWS)

print('%dus/row' % (per_row * MICROSECONDS_PER_SECOND))
