import sqlite3
import os


class SqlLiteHelper(object):
    def __init__(self, db_name='orc.db'):
        self.connect = None
        self.cursor = None
        self._is_connected = False
        self.db_name = db_name

    def _get_connect(self):
        if self._is_connected:
            pass
        else:
            try:
                self.connect = sqlite3.connect(self.db_name)
                self._is_connected = True
            except Exception as e:
                print(e)
                self.connect = None

    def _ensure_connected(self):
        if not self._is_connected:
            self._get_connect()
            self.cursor = self.connect.cursor()
            self._is_connected = True

    def init_db(self):
        if not os.path.exists(self.db_name):
            sql = f"""
            create table orc_recognize(
                obj_md5  varchar(50) primary key,
                content  text,
                rows int
            )
            """
            self._ensure_connected()
            self.cursor.execute(sql)
            self.connect.commit()
            self.safe_close()
        else:
            pass

    def fetch_data(self, key):
        self._ensure_connected()
        sql = f"""
                select content,rows  from orc_recognize
                where obj_md5 = '{key}'
                """
        print(f'query sql:{sql}')
        cursor = self.cursor.execute(sql)
        data = cursor.fetchone()
        data = [] if data is None else data
        return data

    def update_data(self, params):
        assert isinstance(params, (tuple, list)),f'only supported tuple or ' \
                                                 f'list,but get {type(params)}'
        sql = f"""
               insert into orc_recognize(obj_md5,content,rows)
               values("{params[0]}","{params[1]}",{params[2]})
            """
        print(f'update_sql:{sql}')
        self._ensure_connected()
        self.cursor.execute(sql)
        self.connect.commit()
        self.safe_close()

    def safe_close(self):
        if self.connect is not None:
            self.connect.close()
