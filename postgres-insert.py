#!/usr/bin/python3

import time
import psycopg2

############
LOW_ROWS = 500
HIGH_ROWS = 1000
SAMPLES = 100
############


MICROSECONDS_PER_SECOND = 1000000

db = psycopg2.connect('host=35.235.77.254 user=postgres password=foobar dbname=benchmark')
c = db.cursor()

c.execute('DROP TABLE IF EXISTS pushrows')
c.execute('''
CREATE TABLE pushrows (
    id BIGSERIAL PRIMARY KEY
)
''')

c.execute('DROP FUNCTION IF EXISTS pushrows (numrows INTEGER)')
c.execute('''
CREATE FUNCTION pushrows (numrows INTEGER) RETURNS void AS $$
DECLARE
	rec RECORD;
	x INTEGER := 0;
BEGIN
	LOOP
		EXIT WHEN x = numrows;
		x := x + 1;
                INSERT INTO pushrows VALUES (DEFAULT);
	END LOOP;
END
$$ language plpgsql
''')

def MeanExecutionTime(rows, samples):
    start = time.perf_counter()
    for _ in range(samples):
        c.execute('SELECT pushrows(%d)' % rows)
    end = time.perf_counter()

    return (end - start) / samples

low = MeanExecutionTime(LOW_ROWS, SAMPLES)
high = MeanExecutionTime(HIGH_ROWS, SAMPLES)

per_row = (high - low) / (HIGH_ROWS - LOW_ROWS)
base = high - (HIGH_ROWS * per_row)

print('%dus/row' % (per_row * MICROSECONDS_PER_SECOND))
print('%dus commit' % (base * MICROSECONDS_PER_SECOND))
