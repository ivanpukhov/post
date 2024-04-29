import sqlite3

import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)


# Функция для проверки наличия трек-номера в базе данных
def check_tracking_number(tracking_number):
    conn = sqlite3.connect('packages.db')
    cursor = conn.cursor()

    cursor.execute("SELECT tracking_number FROM packages WHERE tracking_number=?", (tracking_number,))
    result = cursor.fetchone()

    conn.close()

    return result is not None


# Функция для добавления трек-номера в базу данных
def add_tracking_number(tracking_number):
    conn = sqlite3.connect('packages.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO packages (tracking_number) VALUES (?)", (tracking_number,))
    conn.commit()

    conn.close()


# Функция для отправки запроса на внешний API и обработки ответа
def get_package_status(tracking_number):
    url = f'https://post.kz/external-api/tracking/api/v2/{tracking_number}/events'
    response = requests.get(url)

    if response.status_code == 404:
        return 404
    else:
        data = response.json()
        if 'error' in data:
            return 201
        else:
            return data


def get_package_name(tracking_number):
    url = f'https://post.kz/external-api/tracking/api/v2/{tracking_number}'
    response = requests.get(url)

    if response.status_code == 404:
        return 404
    else:
        data = response.json()
        if 'error' in data:
            return 201
        else:
            return data


@app.route('/')
def index():
    return render_template('index.html')


# Обработчик запроса для получения статуса посылки по трек-номеру
@app.route('/<tracking_number>', methods=['GET'])
def get_package(tracking_number):
    if check_tracking_number(tracking_number):
        package_status = get_package_status(tracking_number)
        package_name = get_package_name(tracking_number)
        if package_status == 404:
            return render_template('none.html', status="Ваша посылка не найдена", track=tracking_number)
        elif package_status == 201:
            return render_template('greenman.html', greenman="Посылка отправлена со склада Greenman",
                                   track=tracking_number)
        else:
            return render_template('trackinfo.html', status=package_status, package_name=package_name,
                                   track=tracking_number)
            # return jsonify(package_status), 200
    else:
        return render_template('none.html', status="Ваша посылка не найдена", track=tracking_number)

@app.route('/addd/', methods=['GET'])
def dd():
    return render_template('add.html')


# Обработчик запроса для добавления трек-номера в базу данных
@app.route('/add/<tracking_number>', methods=['GET'])
def add_package(tracking_number):
    if not check_tracking_number(tracking_number):
        add_tracking_number(tracking_number)
        return jsonify({'message': 'added'}), 200
    else:
        return jsonify({'message': 'track added before you'}), 400


# Обработчик запроса для получения всех трек-номеров из базы данных
@app.route('/alltrack', methods=['GET'])
def get_all_tracking_numbers():
    conn = sqlite3.connect('packages.db')
    cursor = conn.cursor()

    cursor.execute("SELECT tracking_number FROM packages")
    result = cursor.fetchall()

    conn.close()

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(port=3030)

