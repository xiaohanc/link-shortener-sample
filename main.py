from flask import Flask, request, render_template, redirect
from sqlite3 import OperationalError
import sqlite3
from urllib.parse import urlparse
from core.id_convert import id_to_base62, url_to_base10
import base64

str_encode = str.encode

app = Flask(__name__)
host = 'http://localhost:5000/'


def table_check():
    create_table = """
        CREATE TABLE WEB_URL(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        URL TEXT NOT NULL
        );
        """
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(create_table)
        except OperationalError:
            pass


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = str_encode(request.form.get('url'))
        # add http if url does not contain http header
        if urlparse(original_url).scheme == '':
            url = 'http://' + original_url
        # when url does not contain http or https, the schema could be b''
        elif urlparse(original_url).scheme == b'':
            url = b'http://' + original_url
        else:
            url = original_url
        with sqlite3.connect('urls.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute(
                'INSERT INTO WEB_URL (URL) VALUES (?)',
                [base64.urlsafe_b64encode(url)]
            )
            # encode database id to base62 decimal
            encoded_string = id_to_base62(res.lastrowid)
        return render_template('index.html', short_url=host + encoded_string)
    return render_template('index.html')


@app.route('/<short_url>')
def redirect_short_url(short_url):
    # homepage http://localhost:5000/ will run redirect_short_url("favicon.ico")
    # url_to_base10('favicon.ico') would overflows the sqlite max and throws error
    # I will add a filter to avoid this issue
    if short_url == 'favicon.ico':
        return render_template('index.html')

    # decode short url from base62 to base10 id
    decoded = url_to_base10(short_url)

    url = host  # fallback if no URL is found
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        res = cursor.execute('SELECT URL FROM WEB_URL WHERE ID=?', [decoded])
        try:
            short = res.fetchone()
            if short is not None:
                url = base64.urlsafe_b64decode(short[0])
        except Exception as e:
            print(e)
    return redirect(url)


if __name__ == '__main__':
    # Check if the table is created or not, if not create table WEB_URL
    table_check()
    app.run(debug=True)
