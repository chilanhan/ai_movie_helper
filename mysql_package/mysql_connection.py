import pymysql
config={
        'host':'localhost',
        'port':3306,
        'user':'debian-sys-maint',
        'passwd':'swikoiR9sw8jcRUv',
        'db':'try',
        'charset':'utf8mb4',
        'local_infile':1

    }
conn=pymysql.connect(** config)
cur=conn.cursor()
print('success')
userid=123
sql_cmd="select * from user where uid='"+str(userid)+"'"
sql_cmd
query_data=db.engine.excute(sql_cmd)
if len(list(query_data))==0:
    sql_cmd="insert into user (uid) values('"+str(userid)+"');"
    db.engine.excute(sql_cmd)
