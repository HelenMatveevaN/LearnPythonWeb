from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#generate_password_hash - делает такое шифрование, которое потом расшифровать нельзя
#check_password_hash - шифрует тем же образом, что и generate_password_hash, потом сравнивает
#при шифровании используется SECRET_KEY (поэтому его нельзя нигде публиковать)

db = SQLAlchemy()

#описание модели News
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    #научим модель работать с паролями
    #важно никогда не хранить пароль в БД в открытом виде
    #поэтому важно сначала пароль зашифровать
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password) 
        #сравнивает зашифрованный пароль и зашифрованную строку от пользователя, return True/False

    @property #декоратор, который позволяет вызвать метод как атрибут, без скобок
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User name={} id={}'.format(self.username, self.id)

    """def get_id(self):
        return set(self.user_id)"""