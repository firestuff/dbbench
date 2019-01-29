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

c.execute('DROP TABLE IF EXISTS pullrows')
c.execute('''
CREATE TABLE pullrows (
    id BIGSERIAL PRIMARY KEY
)
''')
c.execute('INSERT INTO pullrows VALUES (1)')

c.execute('DROP FUNCTION IF EXISTS pullrows (numrows INTEGER)')
c.execute('''
CREATE FUNCTION pullrows (numrows INTEGER) RETURNS SETOF RECORD AS $$
DECLARE
	rec RECORD;
	x INTEGER := 0;
BEGIN
	LOOP
		EXIT WHEN x = numrows;
		x := x + 1;
		SELECT * FROM pullrows WHERE id=1 INTO rec;
		RETURN NEXT rec;
	END LOOP;
END
$$ language plpgsql
''')

def MeanExecutionTime(rows, samples):
    start = time.perf_counter()
    for _ in range(samples):
        c.execute('SELECT * FROM pullrows(%d) AS (id BIGINT)' % rows)
    end = time.perf_counter()

    return (end - start) / samples

diff = MeanExecutionTime(HIGH_ROWS, SAMPLES) - MeanExecutionTime(LOW_ROWS, SAMPLES)
per_row = diff / (HIGH_ROWS - LOW_ROWS)

print('%dus/row' % (per_row * MICROSECONDS_PER_SECOND))
