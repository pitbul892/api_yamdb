import csv
import sqlite3


def main():
    connection = sqlite3.connect("api_yamdb/db.sqlite3")
    cursor = connection.cursor()

    with open(
        'api_yamdb/static/data/category.csv', "r", encoding='utf8'
    ) as fl:
        cursor.execute('DELETE FROM reviews_category;')
        contents = csv.DictReader(fl)
        to_db = [(i['id'], i['name'], i['slug']) for i in contents]

    connection.executemany(
        'INSERT INTO reviews_category (id, name, slug) VALUES (?, ?, ?);',
        to_db,
    )
    connection.commit()

    with open('api_yamdb/static/data/genre.csv', "r", encoding='utf8') as fl:
        cursor.execute('DELETE FROM reviews_genre;')
        contents = csv.DictReader(fl)
        to_db = [(i['id'], i['name'], i['slug']) for i in contents]

    connection.executemany(
        'INSERT INTO reviews_genre (id, name, slug) VALUES (?, ?, ?);',
        to_db,
    )
    connection.commit()

    with open('api_yamdb/static/data/titles.csv', "r", encoding='utf8') as fl:
        cursor.execute('DELETE FROM reviews_title;')
        contents = csv.DictReader(fl)
        to_db = [
            (i['id'], i['name'], i['year'], i['category']) for i in contents
        ]

    connection.executemany(
        '''INSERT INTO reviews_title (id, name, year, category_id)
        VALUES (?, ?, ?, ?);''',
        to_db,
    )
    connection.commit()

    with open(
        'api_yamdb/static/data/genre_title.csv', "r", encoding='utf8'
    ) as fl:
        cursor.execute('DELETE FROM reviews_titlegenre;')
        contents = csv.DictReader(fl)
        to_db = [(i['id'], i['genre_id'], i['title_id']) for i in contents]

    connection.executemany(
        '''INSERT INTO reviews_titlegenre (id, genre_id, title_id)
        VALUES (?, ?, ?);''',
        to_db,
    )
    connection.commit()

    with open('api_yamdb/static/data/review.csv', 'r', encoding='utf-8') as fl:
        cursor.execute('DELETE FROM reviews_review;')
        contents = csv.DictReader(fl)
        to_db = [
            (
                i['id'],
                i['text'],
                i['score'],
                i['pub_date'],
                i['author'],
                i['title_id'],
            )
            for i in contents
        ]

    connection.executemany(
        '''INSERT INTO reviews_review
        (id, text, score, pub_date, author, title_id)
        VALUES (?, ?, ?, ?, ?, ?);''',
        to_db,
    )
    connection.commit()

    with open(
        'api_yamdb/static/data/comments.csv', "r", encoding='utf8'
    ) as fl:
        cursor.execute('DELETE FROM reviews_comment;')
        contents = csv.DictReader(fl)
        to_db = [
            (i['id'], i['text'], i['pub_date'], i['author'], i['review_id'])
            for i in contents
        ]

    connection.executemany(
        '''INSERT INTO reviews_comment (id, text, pub_date, author, review_id)
        VALUES (?, ?, ?, ?, ?);''',
        to_db,
    )
    connection.commit()

    with open('api_yamdb/static/data/users.csv', "r", encoding='utf8') as fl:
        cursor.execute('DELETE FROM users_user;')
        contents = csv.DictReader(fl)
        to_db = [
            (
                i['id'],
                i['username'],
                i['email'],
                i['role'],
                i['bio'],
                i['first_name'],
                i['last_name'],
            )
            for i in contents
        ]

    connection.executemany(
        '''INSERT INTO users_user
        (id, username, email, role, bio, first_name, last_name)
        VALUES (?, ?, ?, ?, ?, ?, ?);''',
        to_db,
    )
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
