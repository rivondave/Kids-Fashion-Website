from flask import Flask, request, url_for, redirect, session, render_template
from flaskext.mysql import MySQL
from datetime import datetime
import pymysql
import re

def get_time():
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    return time

def get_date():
    now = datetime.now()
    date = now.strftime("%y-%m-%d")
    return date

def decrypt(list):
    length = len(list)
    new_list = []
    result = []
    for i in list:
        value = i*length
        new_list.append(value)
    for i in new_list:
        new = chr(int(i))
        result.append(new)
    return result

def encrypt(char):
    length = len(char)
    list = []
    for i in char:
        value = ord(i)
        value = value/length
        list.append(value)
    return list


app = Flask(__name__,template_folder = "templates")
app.secret_key = 'anything'

app.config['MYSQL_DATABASE_HOST'] = ''
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = '' #if no password, leave blank

mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)

def get_total_quantity():
    username = session['username']
    cursor.execute("SELECT * FROM cart WHERE username = %s",(username))
    rows = cursor.fetchall()
    count = 0
    total_quantity = 0
    while count < len(rows):
        quantity = rows[count]['QUANTITY']
        total_quantity += quantity
        count+=1
    return total_quantity

def get_total_price():
    username = session['username']
    cursor.execute("SELECT * FROM cart WHERE username = %s",(username))
    rows = cursor.fetchall()
    count = 0
    total_price = 0
    while count < len(rows):
        price = rows[count]['TOTAL_PRICE']
        total_price += price
        count+=1
    return total_price

@app.route('/')
def index():
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM products WHERE TREND = 'trend'")
    rows = cursor.fetchall()
    if 'loggedin' in session:
        total = get_total_quantity()
    else:
        total = 0
    return render_template('index.html',trend = rows,total=total)

@app.route('/product/<string:product>')
def single_product(product):
    cursor.execute("SELECT * FROM products WHERE NAME = %s",(product))
    rows = cursor.fetchone()
    if 'loggedin' in session:
        total = get_total_quantity()
    else:
        total = 0
    return render_template('product.html',product=rows,total=total)

@app.route('/bottom')
def bottom():
    cursor.execute("SELECT * FROM products WHERE CATEGORY = 'bottom'")
    rows = cursor.fetchall()
    if 'loggedin' in session:
        total = get_total_quantity()
    else:
        total = 0
    return render_template('bottom.html',bottom = rows, total=total)

@app.route('/top')
def top():
    cursor.execute("SELECT * FROM products WHERE CATEGORY = 'top'")
    rows = cursor.fetchall()
    if 'loggedin' in session:
        total = get_total_quantity()
    else:
        total = 0
    return render_template('top.html', top=rows, total=total)

@app.route('/underwears')
def underwears():
    cursor.execute("SELECT * FROM products WHERE CATEGORY = 'underwears'")
    rows = cursor.fetchall()
    if 'loggedin' in session:
        total = get_total_quantity()
    else:
        total = 0
    return render_template('underwears.html', underwears = rows, total=total)

@app.route('/brands')
def brands():
    if 'loggedin' in session:
        total = get_total_quantity()
    else:
        total = 0
    return render_template('brands.html', total=total)

@app.route('/explore')
def explore():
    if 'loggedin' in session:
        total = get_total_quantity()
    else:
        total = 0
    return render_template('explore.html', total=total)

# ICONS LINK
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        total = get_total_quantity()
    else:
        total = 0
    return render_template('profile.html',total=total)



@app.route('/cart')
def cart():
    username = session['username']
    cursor.execute("SELECT * FROM cart WHERE username = %s",(username))
    rows = cursor.fetchall()
    if 'loggedin' in session:
        total = get_total_quantity()
        total_price = get_total_price()
    else:
        total = 0
        total_price = 0
    return render_template('cart.html',product=rows,total=total,total_price=total_price)



@app.route('/checkout', methods=['GET','POST'])
def checkout():
    if request.method == 'POST':
        if 'name' in request.form and 'price' in request.form and 'code' in request.form and 'image' in request.form and 'quantity' in request.form:
            username = session['username']
            name_list = request.form.getlist('name')
            price_list = request.form.getlist('price')
            code_list = request.form.getlist('code')
            image_list = request.form.getlist('image')
            quantity_list = request.form.getlist('quantity')
            list_length = len(name_list)
            count = 0
            while count < list_length:
                total = int(quantity_list[count]) * int(price_list[count])
                cursor.execute("SELECT * FROM cart WHERE USERNAME = %s AND CODE = %s",(username,code_list[count]))
                user_cart = cursor.fetchone()        
                if user_cart:
                    cursor.execute("INSERT INTO history VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(username,name_list[count],code_list[count],int(quantity_list[count]),price_list[count],total,get_time(),get_date(),image_list[count]))
                    cursor.execute("DELETE FROM cart WHERE USERNAME = %s",(username))
                    conn.commit()
                    count = count+1
                else:
                    cursor.execute("INSERT INTO history VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(username,name_list[count],code_list[count],int(quantity_list[count]),price_list[count],total,get_time(),get_date(),image_list[count]))
                    cursor.execute("DELETE FROM cart WHERE USERNAME = %s",(username))
                    conn.commit()
                    count = count+1
    return render_template('checkout.html')

@app.route('/proceed')
def proceed():
    username = session['username']
    cursor.execute("SELECT * FROM cart WHERE username = %s",(username))
    rows = cursor.fetchall()
    if 'loggedin' in session:
        total = get_total_quantity()
        total_price = get_total_price()
    else:
        total = 0
        total_price = 0
    return render_template('proceed.html',product=rows,total=total,total_price=total_price)

@app.route('/profile/history')
def history():
    username = session['username']
    cursor.execute("SELECT * FROM history WHERE USERNAME = %s",(username))
    rows = cursor.fetchall()
    if 'loggedin' in session:
        total = get_total_quantity()
    else:
        total = 0
    return render_template('history.html',product=rows,total=total)



# LOGIN, LOGOUT, REGISTER AND CHANGE_PASSWORD
@app.route('/login', methods = ['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        enc_password = str(encrypt(password))        
        cursor.execute("SELECT * FROM accounts WHERE USERNAME =%s AND PASSWORD = %s",(username,enc_password))
        accounts = cursor.fetchone()
        if accounts:
            session['loggedin'] = True
            session['email'] = accounts['EMAIL']
            session['username'] = accounts['USERNAME']
            return redirect(url_for('.index'))
        else:
            msg = 'Incorrect username or password'
            return render_template('login.html',msg = msg)
        
    elif request.method == 'POST':
        msg = "Fill in form details"
    return render_template('login.html',msg=msg)

@app.route('/register', methods = ['GET','POST'])
def register():
    msg=''
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            enc_password = str(encrypt(password))
            print(enc_password)
            cursor.execute("SELECT * FROM accounts WHERE USERNAME =%s",(username))
            accounts = cursor.fetchone()
            if accounts:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif len(password) < 8:
                msg = 'Password cannot be less than 8 characters'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                cursor.execute("INSERT INTO accounts VALUES (NULL, %s, %s, %s)",(username,email,enc_password))
                conn.commit()
                msg = 'Account created successfully'
            return render_template('register.html',msg=msg)

        else:
            msg = 'Account could not be created!'    

    elif request.method == 'POST':
        msg = "Fill in form details"
    return render_template('register.html',msg=msg)

@app.route('/logout', methods = ['GET','POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    # session.permanent = False
    return redirect(url_for('.index'))

@app.route('/change_password', methods=['GET','POST'])
def change_password():
    msg=" "
    if request.method == 'POST':
        if 'username' in request.form and 'new_password' in request.form and 'confirm_password' in request.form:
            username = request.form['username']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            enc_password = str(encrypt(new_password))
            cursor.execute("SELECT * FROM accounts WHERE USERNAME =%s",(username))
            accounts = cursor.fetchall()
            if accounts:
                if new_password == confirm_password:
                    cursor.execute("UPDATE accounts SET PASSWORD = %s WHERE USERNAME = %s",(enc_password, username))
                    conn.commit()
                    msg = 'Password updated successfully'
                else:
                    msg = "Password doesn't match"
            else:
                msg = "User doesn't exist"
            return render_template('change_password.html',msg=msg)

        else:
            msg = 'Password could not be updated!'
        
    elif request.method == 'POST':
        msg = "Fill in form details"
    return render_template('change_password.html',msg=msg)

@app.route('/increase/<string:code>')
def increase_quantity(code):
    username = session['username']
    cursor.execute("SELECT * FROM cart WHERE USERNAME = %s AND CODE = %s",(username,code))
    user = cursor.fetchone()
    if user:
        quantity = user['QUANTITY']
        price = user['PRICE']
        total_price = user['TOTAL_PRICE']
        quantity = quantity  + 1
        total_price = int(quantity) * int(price)
        cursor.execute("UPDATE cart SET QUANTITY = %s, TOTAL_PRICE = %s WHERE USERNAME = %s AND CODE = %s",(quantity,total_price,username,code))
        conn.commit()
    return redirect(url_for('.cart'))

@app.route('/decrease/<string:code>')
def decrease_quantity(code):
    username = session['username']
    cursor.execute("SELECT * FROM cart WHERE USERNAME = %s AND CODE = %s",(username,code))
    user = cursor.fetchone()
    if user:
        quantity = user['QUANTITY']
        if quantity > 1:
            price = user['PRICE']
            total_price = user['TOTAL_PRICE']
            quantity = quantity - 1
            total_price = int(quantity) * int(price)
            cursor.execute("UPDATE cart SET QUANTITY = %s, TOTAL_PRICE = %s WHERE USERNAME = %s AND CODE = %s",(quantity,total_price,username,code))
            conn.commit()
    return redirect(url_for('.cart'))


#CART FUNCTIONALITIES WITHOUT SESSION
@app.route('/add', methods=['GET','POST'])
def add():
    
    if request.method == 'POST':
        if 'name' in request.form and 'price' in request.form and 'code' in request.form and 'image' in request.form and 'quantity' in request.form:
            name = request.form['name']
            price = request.form['price']
            code = request.form['code']
            image  = request.form['image']
            quantity = request.form['quantity']
            username = session['username']
            total = int(price)*int(quantity)
            
            cursor.execute("SELECT * FROM cart WHERE USERNAME = %s AND CODE = %s",(username,code))
            user_cart = cursor.fetchone()        
            if user_cart:
                old_quantity = user_cart['QUANTITY']
                new_quantity = int(quantity) + int(old_quantity)
                new_total = int(price) * new_quantity
                cursor.execute("UPDATE cart SET TOTAL_PRICE = %s, QUANTITY=%s WHERE USERNAME = %s AND CODE = %s",(new_total,new_quantity,username,code))
                conn.commit()
            else:
                cursor.execute("INSERT INTO cart VALUES(%s,%s,%s,%s,%s,%s,%s)",(name,price,code,image,int(quantity),username,total))
                conn.commit()
        return redirect(url_for('.single_product',product=name))

@app.route('/delete/<string:code>')
def delete(code):
    username = session['username']
    cursor.execute("DELETE FROM cart WHERE CODE = %s AND USERNAME = %s",(code,username))
    conn.commit()
    return redirect(url_for('.cart'))

@app.route('/empty')
def empty():
    username = session['username']
    cursor.execute("DELETE FROM cart WHERE USERNAME = %s",(username))
    conn.commit()
    return redirect(url_for('.cart'))

if __name__ == '__main__':
    app.run(debug=True)
