#!/usr/bin/env python

import time

from contextlib import closing

from db import db, LOCAL_DB

if __name__ == '__main__':
    with db(LOCAL_DB) as conn:
        with closing(conn.cursor()) as cursor:

            # SLOW METHOD
            q = 'select * from lotsa_data limit %(offset)s, %(row_count)s'

            # FAST METHOD
            #q = 'select * from lotsa_data where id > %(offset)s order by id asc limit %(row_count)s'

            params = {'offset': 0, 'row_count': 100}
            cursor.execute(q % params)
            rows = cursor.fetchall()
            print rows[0]
            while rows:
                params['offset'] += len(rows)
                s = time.time()
                cursor.execute(q % params)
                rows = cursor.fetchall()
                e = time.time()
                print rows[0], '%.3f ms' % ((e-s) * 1000)
