from flask import Flask, render_template, redirect, url_for
from models import db_session
from forms.register_form import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required
from forms.login_form import LoginForm
from models.users import User

app = Flask(__name__, template_folder='html')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init('db/base.db')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    return render_template('index.html', url_for=url_for)


@app.route('/btc')
def btc():
    # btc_model = ModelProcessor('BTC', 'BTC_model')  Canvas Api
    # plot_url = btc_model.build_plot()
    # return f'<img src="data:image/png;base64, {plot_url}">'
    return render_template('BTC.html')


@app.route('/eth')
def eth():
    # btc_model = ModelProcessor('ETH', 'ETH_model')  Canvas Api
    # plot_url = btc_model.build_plot()
    # return f'<img src="data:image/png;base64, {plot_url}">'
    return render_template('ETH.html')


@app.route('/ada')
def ada():
    # btc_model = ModelProcessor('ADA', 'ADA_model')  Canvas Api
    # plot_url = btc_model.build_plot()
    # return f'<img src="data:image/png;base64, {plot_url}">'
    return render_template('ADA.html')


@app.route('/sol')
def sol():
    # btc_model = ModelProcessor('SOL', 'SOL_model')  Canvas Api
    # plot_url = btc_model.build_plot()
    # return f'<img src="data:image/png;base64, {plot_url}">'
    return render_template('SOL.html')


@app.route('/matic')
def matic():
    # btc_model = ModelProcessor('MATIC', 'MATIC_model')  Canvas Api
    # plot_url = btc_model.build_plot()
    # return f'<img src="data:image/png;base64, {plot_url}">'
    return render_template('MATIC.html')


@app.route('/link')  # ChainLink Crypto
def link():
    # btc_model = ModelProcessor('LINK', 'LINK_model')  Canvas Api
    # plot_url = btc_model.build_plot()
    # return f'<img src="data:image/png;base64, {plot_url}">'
    return render_template('LINK.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')