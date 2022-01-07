import json
import pymysql

def update_all_json():
    def make_json_bubble(movie, col):
        config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'debian-sys-maint',
            'passwd': 'swikoiR9sw8jcRUv',
            'db': 'try',
            'charset': 'utf8mb4',
            'local_infile': 1

        }

        conn = pymysql.connect(**config)
        cur = conn.cursor()
        get_data_sql = F"select * from {movie} order by abs(timediff(curdate(),movie_date)) ;"

        cur.execute(get_data_sql)
        movie_data = cur.fetchall()

        conn.close()
        cur.close()

        text = []
        print(movie_data)
        j = col - 1
        for i in range(0 + 10 * j, 10 + 10 * j):
            name = movie_data[i][0]
            date = movie_data[i][2]
            img_url = movie_data[i][4]
            movie_url = movie_data[i][5]
            content = movie_data[i][3][:250] + str('...')
            # content=name
            bubble = {
                'type': 'bubble',
                "size": "kilo",
                'hero': {'type': 'image',
                         'margin': 'none',
                         'size': 'full',
                         'url': img_url,
                         'aspectMode': 'cover'},

                'body': {'type': 'box',
                         'layout': 'vertical',
                         'contents': [{'type': 'text', 'text': name, 'weight': 'bold', 'size': 'xl'},
                                      {'type': 'text', 'text': '上映日期：' + str(date)},
                                      {'type': 'box',
                                       'layout': 'horizontal',
                                       'contents': [{'type': 'button',
                                                     'action': {'type': 'message',
                                                                'label': '電影簡介',
                                                                'text': content}},
                                                    {'type': 'button',
                                                     'action': {'type': 'uri',
                                                                'label': '預告片',
                                                                'uri': movie_url}

                                                     }]}]}}
            text.append(bubble)

        message = {'type': 'carousel', 'contents': text}
        print(message)
        with open(F"{movie}{col}.json", 'w', encoding='utf-8') as f:
            json.dump(message, f)
        f.close()


    make_json_bubble('on_movie', 1)
    make_json_bubble('on_movie', 2)
    make_json_bubble('on_movie', 3)
    make_json_bubble('coming_movie', 1)
    make_json_bubble('coming_movie', 2)
    make_json_bubble('coming_movie', 3)
    print("successfully updated all jsons!")
