from contextlib import contextmanager

import MySQLdb


LOCAL_DB = {'host': '127.0.0.1', 'user': 'root', 'db': 'batch_test'}


@contextmanager
def db(conn_dict):
    try:
        conn = MySQLdb.connect(**conn_dict)
        yield conn
    finally:
        print 'closing connection'
        conn.close()
