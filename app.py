import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from config import get_db_connection


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm() 
    msg = None  
    if form.validate_on_submit():  
        username = form.username.data
        password = form.password.data
        if username == 'admin' and password == '123':
            session['logged_in'] = True
            return redirect(url_for('home_page'))
        else:
            msg = 'Thông tin đăng nhập sai!!'
    return render_template('login.html', form=form, msg=msg)

@app.route('/home')
def home_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees ORDER BY id DESC LIMIT 10")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('home.html', results=results)
    

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        doj = request.form['doj']
        email = request.form['email']
        gender = request.form['gender']
        contact = request.form['contact']
        address = request.form['address']
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO employees (name, age, doj, email, gender, contact, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, age, doj, email, gender, contact, address))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home_page'))
    return render_template('add.html')

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_no = request.form.get('id')
        name = request.form['name']
        age = request.form['age']
        doj = request.form['doj']
        email = request.form['email']
        gender = request.form['gender']
        contact = request.form['contact']
        address = request.form['address']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("Update employees set name=%s, age=%s, doj=%s, email=%s, gender=%s, contact=%s, address=%s where id=%s", (name, age, doj, email, gender, contact, address, id_no))
        conn.commit()
        return redirect(url_for('home_page'))
  

@app.route('/delete/<string:id_no>', methods=['GET'])
def delete(id_no):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (id_no,))
    conn.commit()
    return redirect(url_for('home_page'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = request.args.get('query')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE name ILIKE %s OR email ILIKE %s", 
                   (f'%{search_query}%', f'%{search_query}%'))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('home.html', results=results)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
