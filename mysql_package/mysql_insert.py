import pymysql
uid=123
uname='ortonrocks'
config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'debian-sys-maint',
        'passwd': 'swikoiR9sw8jcRUv',
        'db': 'try',
        'charset': 'utf8mb4',
        'local_infile': 1

    }

def insert_user_to_mysql(uid,uname):
    conn = pymysql.connect(**config)
    print('successfully connected')

    cur = conn.cursor()

    get_data_sql = "select * from user where uid = '"+str(uid)+"' ;"

    cur.execute(get_data_sql)
    data=cur.fetchall()
    if len(data)==0:
        insert_user_sql="insert into user (uid,uname) values ('{}','{}')".format(uid,uname)
        cur.execute(insert_user_sql)
        conn.commit()
        print('成功存入user資料')
    else:
        print('已經註冊過了！')
    cur.close()
    conn.close()



def insert_bookingdata_to_mysql(uname,mname,session):
    conn = pymysql.connect(**config)
    print('successfully connected')
    cur = conn.cursor()
    delete_previous_sql=f" delete from  movie_booking  where (uname='{uname}') and (mname='{mname}') and (session='{session}')"
    cur.execute(delete_previous_sql)
    conn.commit()
    insert_user_sql=f"insert into movie_booking (uname,mname,session ) values ('{uname}','{mname}','{session}' )"
    cur.execute(insert_user_sql)
    conn.commit()
    cur.close() 
    conn.close()



def insert_user_habit(uname,like_movie_type,like_mname1,like_mname2,like_mname3):
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    print('successfully connected')
    delete_previous_sql=f" delete from user_habits where (uname='{uname}') ;"
    cur.execute(delete_previous_sql)
    conn.commit()
    insert_user_sql=f"insert into user_habits (uname,like_movie_type,like_mname1,like_mname2,like_mname3 ) values ('{uname}','{like_movie_type}','{like_mname1}','{like_mname2}','{like_mname3}' )"
    cur.execute(insert_user_sql)
    conn.commit()
    cur.close() 
    conn.close()
    print('successfully input user_habit!')









def insert_ratingdata_to_mysql(uname,mname,rating):
    print(f'========={uname}{mname}{rating}')
    conn = pymysql.connect(**config)
    print('successfully connected')
    cur = conn.cursor()
    delete_previous_sql=f" delete from  movie_rating  where (uname='{uname}') and (mname='{mname}')"
    cur.execute(delete_previous_sql)
    conn.commit()
    insert_user_sql=f"insert into movie_rating (uname,mname,rating) values ('{uname}','{mname}','{rating}' )"
    cur.execute(insert_user_sql)
    conn.commit()
    cur.close() 
    conn.close()
    print('successfully input movie booking!')

#def insert_movie_rating(uname,mname,rating):




