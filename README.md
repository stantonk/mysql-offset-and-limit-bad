Iterating through a MySQL table using OFFSET and LIMIT is not
performant, as the OFFSET basically causes a row scan from the start of
the table up to the OFFSET row. This means that for each consecutive
batch, the query execution time grows.

If you have to cycle through all the rows in a table, you can avoid this
by instead batching on the primary keys, which is fast because they are
indexed. You need to use an ORDER BY to ensure you don't skip rows or
read the same row twice.

load.py:  script to quickly load lots of rows to test with
db.py: db helper code
batch_read.py: script that demonstrates both good and bad queries


When you run batch_read.py on your test table, the bad query will print
out progressively increasing query times, e.g.

```
(101L, '3890_1528', 'goodbye') 1.040 ms
...
(25601L, '7653_9863', 'good day!') 13.365 ms
...
(90501L, '9677_6312', 'goodbye') 47.163 ms
```

The good query, however, maintains a constant query execution time:

```
(101L, '3890_1528', 'goodbye') 0.486 ms
...
(25601L, '7653_9863', 'good day!') 0.391 ms
...
(90501L, '9677_6312', 'goodbye') 0.374 ms
```