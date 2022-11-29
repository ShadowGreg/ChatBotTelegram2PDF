import sqlite3
from datetime import datetime
import os
from utils import export_csv, create_tmp_dir

DEFAULT_ADMIN_ID = 538455552

GET_SUMMARY_REPORT = 0
GET_CONVERTS_REPORT = 1
GET_FILES_REPORT = 2
GET_ADMINS_REPORT = 3


SRC_DB = './db/'
DB_NAME = 'data_base.db'
DB_FILE = SRC_DB + DB_NAME

DB_CREATE_TABLE_USERS_QUERY = """
CREATE TABLE IF NOT EXISTS users(
    id integer PRIMARY KEY AUTOINCREMENT,
    user_id integer UNIQUE NOT NULL,
    username text,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

DB_CREATE_TABLE_FILES_QUERY = """
CREATE TABLE IF NOT EXISTS files(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   file_name TEXT NOT NULL,
   file_ext TEXT NOT NULL,
   file_size INTEGER NOT NULL,
   has_text BOOL DEFAULT FALSE
);
"""


DB_CREATE_TABLE_CONVERTS_QUERY = """
CREATE TABLE IF NOT EXISTS converts(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   user_id INTEGER NOT NULL,
   file_id INTEGER NOT NULL,
   convert_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   tg_version TEXT,
   is_success BOOL DEFAULT FALSE,
   FOREIGN KEY (file_id) 
      REFERENCES files (id) 
         ON DELETE CASCADE 
         ON UPDATE CASCADE,
   FOREIGN KEY (user_id) 
      REFERENCES users (id) 
         ON DELETE CASCADE 
         ON UPDATE CASCADE
);
"""

DB_CREATE_TABLE_ADMINS_QUERY = """
CREATE TABLE IF NOT EXISTS admins(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   user_id INTEGER NOT NULL,
   enabled BOOL DEFAULT FALSE,
   modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

DB_INSERT_DEFAULT_ADMIN_QUERY = f"""
INSERT INTO admins (user_id, enabled)
VALUES ({DEFAULT_ADMIN_ID}, true);
"""

DB_INSERT_USER_QUERY = """
INSERT INTO users (user_id, username, registration_date, last_used)
VALUES (?, ?, ?, ?);
"""

DB_UPDATE_USER_QUERY = """
UPDATE users SET username = ?, last_used = ? WHERE user_id = ?;
"""

DB_SEARCH_USER_BY_ID_QUERY = """
SELECT * FROM users WHERE user_id=?;
"""

DB_INSERT_ADMIN_QUERY = """
INSERT INTO admins (user_id, enabled, modified)
VALUES (?, ?, ?);
"""

DB_UPDATE_ADMIN_QUERY = """
UPDATE admins SET enabled = ?, modified = ? WHERE user_id = ?;
"""

DB_SEARCH_ADMIN_BY_ID_QUERY = """
SELECT * FROM admins WHERE user_id=?;
"""

DB_CHECK_ADMIN_QUERY = """
SELECT * FROM admins WHERE user_id=? AND enabled=true;
"""

DB_SELECT_ADMINS_QUERY = """
SELECT * FROM admins;
"""

DB_INSERT_FILES_QUERY = """
INSERT INTO files (file_name, file_ext, file_size, has_text)
VALUES (?, ?, ?, ?);
"""

DB_INSERT_CONVERTS_QUERY = """
INSERT INTO converts (user_id, file_id, tg_version, is_success)
VALUES (?, ?, ?, ?);
"""

DB_SELECT_CONVERTS_QUERY = """
SELECT * FROM converts;
"""

DB_SELECT_FILES_QUERY = """
SELECT * FROM files;
"""

DB_SELECT_SUMMARY = """
SELECT 
	ROW_NUMBER () OVER (ORDER BY user_id) AS number,
	user_id,
	count(files.id) AS count_all,
	COUNT(DISTINCT file_name || file_ext) AS count_unique FROM converts
JOIN files ON files.id = converts.file_id;
"""


def db_get_connection():
    try:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)  # Connect DB.
        print('successfully connected to existing db')
    except sqlite3.Error as e:
        print('Connection error to existing db', e)
    return conn


def db_add_user(conn, cur, user_id: int, username: str, registration_date: datetime, last_used: datetime):
    cur.execute(DB_INSERT_USER_QUERY, (user_id, username, registration_date, last_used))
    conn.commit()


def db_update_user(conn, cur, user_id: int, username: str, last_used: datetime):
    cur.execute(DB_UPDATE_USER_QUERY, (username, last_used, user_id))
    conn.commit()
    

def update_user(conn, cur, message):
    user_id = message.from_user.id
    username = message.from_user.username
    registration_date = datetime.today()
    last_used = datetime.today()

    check_for_user_id = cur.execute(DB_SEARCH_USER_BY_ID_QUERY, (user_id,))
    if check_for_user_id.fetchone() is None:  # Делаем когда нету человека в бд
        db_add_user(conn, cur, 
                    user_id=user_id,
                    username=username,
                    registration_date=registration_date,
                    last_used=last_used
        )
    else:  # Делаем когда есть человек в бд
        db_update_user(conn, cur,
                        user_id=user_id,
                        username=username,
                        last_used=last_used
            )


def db_add_admin(conn, cur, user_id: int, enabled: bool, modified: datetime):
    cur.execute(DB_INSERT_ADMIN_QUERY, (user_id, enabled, modified))
    conn.commit()


def db_update_admin(conn, cur, user_id: int, enabled: bool, modified: datetime):
    cur.execute(DB_UPDATE_ADMIN_QUERY, (enabled, modified, user_id))
    conn.commit()


def update_admin(user_id, enabled):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        modified = datetime.today()
        check_for_user_id = cur.execute(DB_SEARCH_ADMIN_BY_ID_QUERY, (user_id,))
        if check_for_user_id.fetchone() is None:
            db_add_admin(conn, cur, 
                        user_id=user_id,
                        enabled=enabled,
                        modified=modified
            )
        else:
            db_update_admin(conn, cur, 
                        user_id=user_id,
                        enabled=enabled,
                        modified=modified
            )
    except sqlite3.Error as e:
        print('cannot create table inside db', e)
    finally:
        conn_cur_close(conn, cur)


def db_update_files(conn, cur, orig_file_info):
    cur.execute(DB_INSERT_FILES_QUERY, orig_file_info)
    inserted_id = cur.lastrowid    
    conn.commit()
    return inserted_id


def db_update_converts(conn, cur, convert_info):
    cur.execute(DB_INSERT_CONVERTS_QUERY, convert_info)
    inserted_id = cur.lastrowid    
    conn.commit()
    return inserted_id


def db_select_query(cur, query):
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def conn_cur_close(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.commit()            
        conn.close()    
    print("Соединение с SQLite закрыто")


def init_db():
    try:
        if not os.path.exists(SRC_DB):
            os.makedirs(SRC_DB)
    except OSError as e:
        print('cannot create db directory', e)
    
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        queries = (
            DB_CREATE_TABLE_USERS_QUERY, 
            DB_CREATE_TABLE_ADMINS_QUERY,
            DB_CREATE_TABLE_FILES_QUERY, 
            DB_CREATE_TABLE_CONVERTS_QUERY,
            DB_INSERT_DEFAULT_ADMIN_QUERY
        )
        for query in queries:
            cur.executescript(query)
        conn.commit()
        print('DB init is sucessful')
    except sqlite3.Error as e:
        print('cannot create table inside db', e)
    finally:
        conn_cur_close(conn, cur)


def save_to_db(message, orig_file_info, convert_status):
    try:
        conn = db_get_connection()
        cur = conn.cursor()  # Create cursor for work with tables.
        update_user(conn, cur, message)
        file_id = db_update_files(conn, cur, orig_file_info)
        user_id = message.from_user.id
        convert_id = db_update_converts(conn, cur, (user_id, file_id, 1, convert_status))
        print(convert_id)
    except sqlite3.Error as e:
        print("Ошибка при работе с SQLite", e)
    finally:  # закрыть соединение, когда все закончено.
        conn_cur_close(conn, cur)


def get_query_reportname_columns(report_type):
    cases = {
        GET_SUMMARY_REPORT: (
            DB_SELECT_SUMMARY, 
            'summary', 
            ('number', 'telegram_user_id', 'count_all', 'count_unique')
        ),
        GET_CONVERTS_REPORT: (
            DB_SELECT_CONVERTS_QUERY,
            'converts', 
            ('id', 'telegram_user_id', 'file_id', 'convert_datetime', 'tg_version', 'is_success')
        ),
        GET_FILES_REPORT: (
            DB_SELECT_FILES_QUERY,
            'files',
            ('id', 'file_name', 'file_ext', 'file_size', 'has_text')
        ),
        GET_ADMINS_REPORT: (
            DB_SELECT_ADMINS_QUERY,
            'admins',
            ('id', 'telegram_user_id', 'enabled', 'modified')
        ),
    }
    return cases.get(report_type, None)


def export_data_to_csv(message, report_type):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        query, report_name, columns = get_query_reportname_columns(report_type)
        rows = db_select_query(cur, query)
        dir_path = create_tmp_dir(message.chat.id)
        cur_datetime = datetime.today().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(dir_path, f"{cur_datetime}_{report_name}.csv")
        export_csv(file_path, columns, rows)
        print(f"CSV report is exported to {os.path.basename(file_path)}")
        return file_path
    except sqlite3.Error as e:
        print("Ошибка при работе с SQLite", e)
    finally:  # закрыть соединение, когда все закончено.
        conn_cur_close(conn, cur)


def check_is_admin(user_id):
    try:
        conn = db_get_connection()
        cur = conn.cursor()
        check_for_user_id = cur.execute(DB_CHECK_ADMIN_QUERY, (user_id,))
        if check_for_user_id.fetchone() is None:
            return False
        return True
    except sqlite3.Error as e:
        print('cannot create table inside db', e)
    finally:
        conn_cur_close(conn, cur)