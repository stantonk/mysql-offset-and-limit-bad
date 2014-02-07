#!/usr/bin/env python

from multiprocessing import Pool

from random import choice
from random import randint

from db import db, LOCAL_DB


id_gen = lambda: '%s_%s' % (randint(1, 10000), randint(1, 10000))
randstr = lambda: choice(['hello', 'goodbye', 'buenos dias', 'good day!'])


def write_rows(DB, batch_size, batches):
    with db(DB) as conn:
        with closing(conn.cursor()) as cursor:
            for _ in xrange(batches):
                q = 'insert into lotsa_data (some_str, msg) values (%s, %s)'
                value_gen = ((id_gen(), randstr()) for _ in xrange(batch_size))
                cursor.executemany(q, list(value_gen))
                conn.commit()

if __name__ == '__main__':
    DB = {'host': '127.0.0.1', 'user': 'root', 'db': 'batch_test'}

    pool = Pool(processes=8)
    for i in range(8):
        result = pool.apply_async(write_rows, [LOCAL_DB, 100000, 200])

    print 'closing pool'
    pool.close()
    print 'waiting for completion...'
    pool.join()
    print 'done'
