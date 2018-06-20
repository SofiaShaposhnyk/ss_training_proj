import psycopg2
from app.config import db


def insert_users_data():
    with psycopg2.connect('host={db_host} dbname={db_name} user={db_user}'.format(**db)) as conn:
        with conn.cursor() as cur:
            with open('fixtures_users.csv', 'r') as f:
                cur.copy_from(f, 'users', sep=',')
            conn.commit()


def insert_projects_data():
    with psycopg2.connect('host={db_host} dbname={db_name} user={db_user}'.format(**db)) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO projects VALUES (1, 1, '2010-10-10', '{"1": "DELETE", "2": "UPDATE", "3": "VIEW"}')""")
            cur.execute(
                """INSERT INTO projects VALUES (2, 1, '2017-12-01', '{"1": "DELETE", "2": "VIEW"}')""")
            cur.execute(
                """INSERT INTO projects VALUES (3, 2, '2016-05-30', '{"2": "DELETE", "3": "VIEW"}')""")
            cur.execute(
                """INSERT INTO projects VALUES (4, 2, '2017-07-17', '{"2": "DELETE", "1": "UPDATE"}')""")
            cur.execute(
                """INSERT INTO projects VALUES (5, 2, '2016-10-11', '{"2": "DELETE"}')""")
            cur.execute(
                """INSERT INTO projects VALUES (6, 3, '2018-04-30', '{"3": "DELETE", "2": "VIEW"}')""")
            conn.commit()


def insert_invoices_data():
    with psycopg2.connect('host={db_host} dbname={db_name} user={db_user}'.format(**db)) as conn:
        with conn.cursor() as cur:
            with open('fixtures_invoices.csv', 'r') as f:
                cur.copy_from(f, 'invoices', sep=',')
            conn.commit()


def delete_all_from_db():
    with psycopg2.connect('host={db_host} dbname={db_name} user={db_user}'.format(**db)) as conn:
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM invoices""")
            cur.execute("""DELETE FROM projects""")
            cur.execute("""DELETE FROM users""")
