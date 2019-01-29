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

c.execute('DROP TABLE IF EXISTS pushrows')
c.execute('''
CREATE TABLE pushrows (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY
) ENGINE=InnoDB
''')

c.execute('DROP PROCEDURE IF EXISTS pushrows')
c.execute('''
CREATE PROCEDURE pushrows (IN num INT)
BEGIN
	DECLARE x INT;
	SET x = 0;
	WHILE x < num DO
                INSERT INTO pushrows VALUES ();
		SET X = x + 1;
	END WHILE;
END
''')

def MeanExecutionTime(rows, samples):
    start = time.perf_counter()
    for _ in range(samples):
        c.execute('CALL pushrows(%d)' % rows)
    end = time.perf_counter()

    return (end - start) / samples

low = MeanExecutionTime(LOW_ROWS, SAMPLES)
high = MeanExecutionTime(HIGH_ROWS, SAMPLES)

per_row = (high - low) / (HIGH_ROWS - LOW_ROWS)
base = high - (HIGH_ROWS * per_row)

print('%dus/row' % (per_row * MICROSECONDS_PER_SECOND))
print('%dus commit' % (base * MICROSECONDS_PER_SECOND))
