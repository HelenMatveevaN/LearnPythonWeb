from flask import Flask, render_template
from webapp.python_org_news import get_python_news 
from webapp.weather import weather_by_city

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    #http://api.worldweatheronline.com/premium/v1/weather.ashx?key=893cba22780d456aab894047200301&q=Moscow,Russia&format=json&num_of_days=1&lang=ru
    @app.route('/') #декоратор
    def index():
        title = "Новости Python"
        weather = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        news_list = get_python_news()
        '''if weather:
            weather_text = f"Температура: {weather['temp_C']}, ощущается как {weather['FeelsLikeC']}" #work with python 3.6 (earlier: command 'format')
        else:
            weather_text = "Сервис погоды временно недоступен" #Сервер не упадет, а напишет разумный ответ'''
        #передаем название шаблона, Flask сам ищет папку template
        #шаблон занимается отображением, python получает данные для отображения
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)
    return app
