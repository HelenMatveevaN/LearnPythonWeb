from flask import Flask, render_template, flash, redirect, url_for
#flash-позволяет передавать сообщения между route-ами
#redirect-делает перенаправление мользователя на другую страницу
#url_for-помогает получить url по имени функции, которая этот url обрабатывает
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from webapp.forms import LoginForm
from webapp.model import db, News, User
from webapp.weather import weather_by_city

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app) #инициализируем базу данных после конфигурации (т.к.нужен путь к sqlAlchemy)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    #http://api.worldweatheronline.com/premium/v1/weather.ashx?key=893cba22780d456aab894047200301&q=Moscow,Russia&format=json&num_of_days=1&lang=ru
    @app.route('/') #декоратор
    def index():
        title = "Новости Python"
        weather = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        news_list = News.query.order_by(News.published.desc()).all()
        #передаем название шаблона, Flask сам ищет папку template
        #шаблон занимается отображением, python получает данные для отображения
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)
    
    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('index')) #переадресация на главную страницу
        
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login')) #переадресация на страниу логина
    
    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))
    
    @app.route('/admin')
    @login_required #еще один декоратор (оба декоратора обработаются перед вызовом нижеуказанной функции)
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ!'
        else:
            return 'Вы не админ!'

    return app
