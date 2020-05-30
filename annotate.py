from multiprocessing import Pool, Queue, TimeoutError
from mysql.connector.errors import ProgrammingError
import csv
import mysql.connector
import re
import tqdm


MAX_CONN = 990

REGEX = re.compile('cost=.* rows=(\d+).* rows=(\d+)')

DB_CONFIG = {
    "database": "tpch_sf1_zfrnd",
    "user": "root",
    "unix_socket": "/tmp/mysql.sock",
}

PROGRESS = tqdm.tqdm(total=10000)

CSV_FILE = open('annotated_queries.csv', 'w')

LOGGER = csv.writer(CSV_FILE, delimiter=',')


# Label the query statistics (estimated row, actual row)
def annotate(row):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    result = []
    try:
        cursor.execute('EXPLAIN ANALYZE ' + row[0])
        stats = cursor.fetchall()[0][0]
    except mysql.connector.errors.ProgrammingError as e:
        print("Failed query: " + row[0] + " error: " + str(e))
    else:
        match = REGEX.search(stats)
        # encoded query, estimated_rows, actual_rows
        result.extend(row[1:] + [match.group(1)] + [match.group(2)])
    finally:
        cursor.close()
        conn.close()
        return result


def annotate_done(result):
    PROGRESS.update(1)
    if result:
        LOGGER.writerow(result)
        CSV_FILE.flush()


# Main
if __name__ == '__main__':
    # Start N worker processes
    with Pool(processes=MAX_CONN) as pool:
        results = []
        try:
            with open('queries.csv') as csvfile:
                query_reader = csv.reader(csvfile, delimiter=',')
                for row in query_reader:
                    results.append(pool.apply_async(annotate, args=(row,), callback=annotate_done))
        except KeyboardInterrupt:
            pool.terminate()
        for res in results:
            res.get()

    CSV_FILE.close()
