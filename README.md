# HBASE

- shell 실행

```bash
$ hbase shell
```

- create table

```bash
create 'students', 'info'
```

- table 조회

```bash
list
```

- create

```bash
put 'students', '1', 'info:name', 'hong'
put 'students', '1', 'info:age', '20'
put 'students', '2', 'info:name', 'kim'
put 'students', '2', 'info:address', 'seoul'
```

- Read

```bash
get 'students', '1'
```

- Read all

```bash
 scan 'students'
```

- update

```bash
put 'students', '1', 'info:age', '30'
```

- delete

```bash
# 해당 컬럼 삭제
delete 'students', '2', 'info:address'
# 전체 컬럼 삭제
deleteall 'students', '1'
```

- drop table

```bash
disable 'students'
drop 'students'
```

# FastAPI

- 서버 실행
```bash
uvicorn main:app --reload
```

- Hbase 서버 실행
```bash
/hbase-2.5.11/bin/hbase-daemon.sh start thrift
```

