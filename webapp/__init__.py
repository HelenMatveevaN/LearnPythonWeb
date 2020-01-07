from flask import Flask, render_template

from webapp.model import db, News
from webapp.weather import weather_by_city

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app) #инициализируем базу данных после конфигурации (т.к.нужен путь к sqlAlchemy)

    #http://api.worldweatheronline.com/premium/v1/weather.ashx?key=893cba22780d456aab894047200301&q=Moscow,Russia&format=json&num_of_days=1&lang=ru
    @app.route('/') #декоратор
    def index():
        title = "Новости Python"
        weather = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        news_list = News.query.order_by(News.published.desc()).all()
        #передаем название шаблона, Flask сам ищет папку template
        #шаблон занимается отображением, python получает данные для отображения
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)
    return app
