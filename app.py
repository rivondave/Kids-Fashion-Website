from flask import Flask, request, url_for, redirect, session, render_template
from flaskext.mysql import MySQL
import pymysql
import re


app = Flask(__name__,template_folder = "templates")
app.secret_key = 'anything'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'kidsfashion'
app.config['MYSQL_DATABASE_PASSWORD'] = '' #if no password, leave blank

mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)

@app.route('/')
def index():
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM products WHERE TREND = 'trend'")
    rows = cursor.fetchall()
    return render_template('index.html',trend = rows)

@app.route('/product/<string:product>')
def single_product(product):
    cursor.execute("SELECT * FROM products WHERE NAME = %s",(product))
    rows = cursor.fetchone()
    return render_template('product.html',product=rows)

@app.route('/bottom')
def bottom():
    cursor.execute("SELECT * FROM products WHERE CATEGORY = 'bottom'")
    rows = cursor.fetchall()
    return render_template('bottom.html',bottom = rows)

@app.route('/top')
def top():
    cursor.execute("SELECT * FROM products WHERE CATEGORY = 'top'")
    rows = cursor.fetchall()
    return render_template('top.html', top=rows)

@app.route('/underwears')
def underwears():
    cursor.execute("SELECT * FROM products WHERE CATEGORY = 'underwears'")
    rows = cursor.fetchall()
    return render_template('underwears.html', underwears = rows)

@app.route('/brands')
def brands():
    return render_template('brands.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

# ICONS LINK

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

#FUNCTIONS
def array_merge( first_array, second_array):
    if isinstance( first_array , list) and isinstance( second_array, list):
        return first_array + second_array
    elif isinstance( first_array, dict) and isinstance( second_array, dict):
        return dict (list(first_array.items() ) + list ( second_array.items() ))
    elif isinstance( first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False

# LOGIN, LOGOUT, REGISTER AND CHANGE_PASSWORD
@app.route('/login', methods = ['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM accounts WHERE USERNAME =%s AND PASSWORD = %s",(username,password))
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
    msg=" "
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            cursor.execute("SELECT * FROM accounts WHERE USERNAME =%s OR PASSWORD = %s",(username,password))
            accounts = cursor.fetchone()
            if accounts:
                msg = "User already exists!"
            else:
                cursor.execute("INSERT INTO accounts VALUES (NULL, %s, %s, %s)",(username,email,password))
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
    session.pop('username', None)
    session.permanent = False
    return redirect(url_for('.index'))

@app.route('/change_password', methods=['GET','POST'])
def change_password():
    msg=" "
    if request.method == 'POST':
        if 'username' in request.form and 'new_password' in request.form and 'confirm_password' in request.form:
            username = request.form['username']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            cursor.execute("SELECT * FROM accounts WHERE USERNAME =%s",(username))
            accounts = cursor.fetchone()
            if accounts:
                if new_password == confirm_password:
                    cursor.execute("UPDATE accounts SET PASSWORD = %s WHERE USERNAME = %s",(new_password, username))
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

#EMPTY CART
@app.route('/empty')
def empty_cart():
    try:
        session.pop('cart_item')
        return redirect(url_for('.cart'))
    except Exception as e:
        print(e)

#REMOVE PRODUCT
@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == code:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
        if all_total_quantity == 0:
            session.pop('cart_item')
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        return redirect(url_for('.cart'))
    except Exception as e:
        print(e)



# CART
@app.route('/add', methods=['POST'])
def add():
    _quantity = int (request.form['quantity'])
    _code = request.form['code']
    #validate the received values
    if _quantity and _code and request.method == 'POST':

        cursor.execute("SELECT * FROM products WHERE CODE=%s", (_code,))
        row = cursor.fetchone()
        
        itemArray = { row['CODE'] : {'name' : row['NAME'], 'code' : row['CODE'], 'quantity' :_quantity, 'price' : row['PRICE'], 'image' : row['IMAGE'], 'total_price': _quantity * row['PRICE'] }}

        all_total_price =0
        all_total_quantity = 0

        session.modified = True
        if 'cart_item' in session:

            if row['CODE'] in session['cart_item']:
                for key,value in session['cart_item'].items():
                    if row['CODE'] == key:
                        old_quantity = session['cart_item'][key]['quantity']
                        total_quantity = old_quantity + _quantity
                        session['cart_item'][key]['quantity'] = total_quantity
                        session['cart_item'][key]['total_price'] = int(total_quantity * row['PRICE'])
            else:   
                session['cart_item'] = array_merge(session['cart_item'], itemArray)

            for key, value in session['cart_item'].items():
                individual_quantity = int(session['cart_item'][key]['quantity'])
                individual_price = float(session['cart_item'][key]['total_price'])
                all_total_quantity = all_total_quantity + individual_quantity
                all_total_price = all_total_price + individual_price

        else:
            session['cart_item'] = itemArray
            all_total_quantity = all_total_quantity+ _quantity
            all_total_price = all_total_price + _quantity * row['PRICE']

        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price

        return redirect(url_for('.single_product',product=row['NAME']))
    else:
        return 'Error while adding item to cart'


if __name__ == '__main__':
    app.run(debug=True)
