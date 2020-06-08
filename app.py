from __future__ import print_function
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import re

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'MyBD'

mysql = MySQL(app)

# обработка формы
@app.route('/', methods=['GET', 'POST'])
def index():
    # словарь для сообщений об ошибках
    messages = {}
    # словарь для данных из формы
    details = {}
    if request.method == "POST":
        details = request.form
        last_name = details['last_name']
        first_name = details['first_name']
        ot4estvo = details['ot4estvo']
        region = details['region']
        city = details['city']
        email = details['email']
        phone = details['phone']
        message = details['message']
        # если пустое поле имя
        if not last_name:
            messages.update({"last_name": "Введите фамилию!!!"})
        # если пустое поле фамилия
        if not first_name:
            messages.update({"first_name": "Введите имя!!!"})
        # если пустое поле комментарий
        if not message:
            messages.update({"message": "Введите комментарий!!"})
        # сравниваем введенный email с шаблоном
        mo = re.search(r'^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)
        # если email не совпадает с шаблоном и НЕ пустой
        if not mo and email:
            messages.update({"email": "Введите Email в правильной форме example@mail.com!!!"})
        # сравниваем введенный телефон с шаблоном
        mo = re.search(r'\(\d{3}\)\d{7}', phone)
        # если телефон не совпадает с шаблоном и НЕ пустой
        if not mo and phone:
            messages.update({"phone": "Введите телефон в правильной формате: (918)1234567!!!"})
        # если есть ошибки(т.е. словарь message НЕ пустой), перенапрявляем на исходную страницу с сообщениями об ошибках
        if len(messages) != 0:
            messages.update({"ok": "Ошибка ввода"})
            return render_template('index.html', data=messages, post=details)
        # если ввод верный то остовляем сообщение об удачной отправке
        else:
            # обнуляем массив данных
            details = []
            messages.update({"ok": "Спасибо за Ваш комментарий"})
        # отправляем данные в базу
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO anketa(last_name, first_name, ot4estvo, region, city, email, phone_number, message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (last_name, first_name, ot4estvo, region, city, email, phone, message))
        mysql.connection.commit()
        cur.close()
    return render_template('index.html', data=messages, post=details)

# просмотр комментариев
@app.route('/view', methods=['GET', 'POST'])
def view():
    # если метод post, то требуется удаление записи
    if request.method == "POST":
        details = request.form
        # id записи, которую надо удалить
        id = (details['id'], )
        cur = mysql.connection.cursor()
        # удаляем запись из базы
        cur.execute("Delete from anketa where anketa_id=%s", (id, ))
        mysql.connection.commit()
        cur.close()
    # выводим комментарии(без удаленого, если ранее был запрос на удаление строки)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM anketa")
    data = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('view.html', data=data)

# просмотр статистики
@app.route('/stat', methods=['GET', 'POST'])
def stat():
    # если GET(просмотр статистики по регионам)
    if request.method == "GET":
        cur = mysql.connection.cursor()
        # список городов и кол-во комментариев из конкретного региона
        query = "SELECT region, count(region) FROM anketa GROUP BY region;"
        cur.execute(query)
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('stat.html', data=data)
    # если POST(просмотр статистики по городам выбраного региона)
    elif request.method == "POST":
        details = request.form
        id = details['id']
        cur = mysql.connection.cursor()
        # список городов и кол-во комментариев из конкретного региона
        query = "SELECT city, count(city) FROM anketa where region = %s GROUP BY city;"
        cur.execute(query, (id,))
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        # возвращаем список городов на отдельную страницу для просмотра городов
        return render_template('stat_city.html', data=data, region=id)

@app.route('/_get_region/', methods=['POST'])
def _get_region():
    cur = mysql.connection.cursor()
    # список регионов
    # если надо увеличить список регионов, достаточно добавить их в таблицу, код менять не надо
    query ="Select region from region "
    cur.execute(query)
    data = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    # возвращаем список регионов
    return jsonify({'data': data})

@app.route('/_get_city/', methods=['POST'])
def _get_city():
    details = request.form
    id = details['id']
    cur = mysql.connection.cursor()
    # список городов из данного региона
    # если надо увеличить список городов, достаточно добавить их в таблицу, код менять не надо
    query ="Select city from cities where region_id = %s"
    cur.execute(query, (id,))
    data = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    # возвращаем список городов
    return jsonify({'data': data})


if __name__ == "__main__":
    app.run()
