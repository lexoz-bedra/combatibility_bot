import psycopg2
from config import host, user, password, db_name


def connect(name_1, name_2, merge):
    try:
        # connect to the database
        con = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        # cursor for performing database operations
        with con.cursor() as cur:
            res = add_value(name_1, name_2, merge, cur)
            con.commit()
            return res

    except Exception as ex:
        print(f'[INFO] Error while working with PostgreSQL: {ex}')
    finally:
        if con:
            con.close()
            print('[INFO] PostgreSQL connection closed')


def add_value(name_1: str, name_2: str, merge: int, cur):
    if find_value(name_1, name_2, cur):
        res = find_value(name_1, name_2, cur)
    elif not find_value(name_1, name_2, cur):
        res = merge
        print('AAAAA')
        cur.execute("INSERT INTO pairs (name1, name2, value) VALUES (%(nm1)s, %(nm2)s, %(merge)s)",
                    {'nm1': name_1, 'nm2': name_2, 'merge': merge})
    return res


def find_value(name_1: str, name_2: str, cur):
    cur.execute(
        "SELECT value FROM pairs WHERE "
        "EXISTS(SELECT * FROM pairs WHERE name1 = %(nm1)s AND name2 = %(nm2)s OR name1 = %(nm2)s AND name2 = %(nm1)s"
        "OR name1 = %(nm2)s AND name2 = %(nm1)s) AND name1 = %(nm1)s "
        "AND name2 = %(nm2)s OR name1 = %(nm2)s AND name2 = %(nm1)s;",
        {'nm1': name_1, 'nm2': name_2})
    answers = cur.fetchall()
    if len(answers) > 0:
        return answers[0][0]
    return 0
