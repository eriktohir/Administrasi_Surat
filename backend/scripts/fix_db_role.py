import pymysql

conn = pymysql.connect(host='localhost', user='root', password='', database='tuud_surat')
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='tuud_surat' AND TABLE_NAME='users' AND COLUMN_NAME='role'")
exists = cur.fetchone()[0]
if exists:
    print('column_exists')
else:
    cur.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'staf' NOT NULL")
    conn.commit()
    print('column_added')
cur.close()
conn.close()
