from getpass import getpass #аналог input, но для ввода пароля, не печатает то, что вводит пользователь
import sys #модуль для взаимодействия с системными функциями

from webapp import create_app
from webapp.model import User, db

app = create_app()

with app.app_context():
    username = input('Введите имя пользователя: ')

    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)
    
    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        print('Пароли не одинаковые')
        sys.exit()
    
    new_user = User(username=username, role='admin')
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))
    #стоит дополнительно проверять, что пользователь не использует дополнительные пароли