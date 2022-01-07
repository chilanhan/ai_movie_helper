
import pymysql
config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'debian-sys-maint',
        'passwd': 'swikoiR9sw8jcRUv',
        'db': 'try',
        'charset': 'utf8mb4',
        'local_infile': 1

    }

def yahoo_csv_to_mysql():
    #connect to database

    #def load_csv(csv_file,table_name,database)
    csv_file= '../yahoo_movie1.csv'
    table_name='yahoo_movie'

    conn=pymysql.connect(** config)

    cur=conn.cursor()

    data_sql="LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES" %(csv_file,table_name)
    delete_previous_data='delete from yahoo_movie'
    cur.execute(delete_previous_data)
    cur.execute(data_sql)
    conn.commit()
    conn.close()
    cur.close()
    print('success')

def yahoo_mysql_to_carousel():
    conn = pymysql.connect(**config)
    print('successfully connected')

    cur = conn.cursor()

    get_data_sql = "select * from yahoo_movie;"
    cur.execute(get_data_sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


