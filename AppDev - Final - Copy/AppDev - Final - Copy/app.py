from flask import Flask, redirect, render_template, url_for, request, session, flash
from forms import ProductForm
from forms1 import CreateUserForm
from userforms import LoginForm, LogoutForm, SignUpForm, ProfileForm, LogoutForm
from werkzeug.utils import secure_filename
from info import Information
import shelve
import os
from usermodal import Data
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config["SECRET_KEY"] = "WmsiMb0D61J9RtMWpTvM8HzmEVjAC2pD"

login_status = False
db_index = -1

# Home Page, Catalogue and Staff Catalogue

@app.route("/")
def home():
    db = shelve.open('users.db')
    return render_template("home.html", logged=login_status, name=db['name'][db_index], admin=db['admin'][db_index], i=db_index)


@app.route("/catalogue")
def catalogue():

    db2 = shelve.open('users.db', 'c')

    data = {}
    try:
        db = shelve.open("info.db", "c")
        data = db["Info"]
        db.close()
    except:
        print("Unable to retrieve information from info.db")
    else: 
        datalist = []
        for key in data:
            info = data.get(key)
            datalist.append(info)
        print('Catalogue page login status: ', login_status)
        return render_template("catalogue.html", datalist=datalist, logged=login_status, name=db2['name'][db_index], admin=db2['admin'][db_index], i=db_index)

    return render_template("catalogue.html", logged=login_status, name=db2['name'][db_index], admin=db2['admin'][db_index], i=db_index)


@app.route("/staffcatalogue", methods=["GET", "POST"])
def staff_catalogue():

    db2 = shelve.open('users.db', 'c')

    form = ProductForm()
    if form.validate_on_submit():
        data = {}
        db = shelve.open("info.db", "c")

        try:
            data = db["Info"]
        except:
            print("Unable to retrieve information from info.db")

        f = form.product_image.data
        filename = secure_filename(f.filename)
        f.save("static/" + filename)    

        info = Information(form.product_name.data, form.product_price.data,
                           form.product_weight.data, filename, form.product_details.data, form.product_category.data)
        data[info.get_id()] = info
        db["Info"] = data

        db.close()

        return redirect(url_for('staff_catalogue'))
    else:
        data = {}
        try:
            db = shelve.open("info.db", "c")
            data = db["Info"]
            db.close()
        except:
            print("Unable to retrieve information from info.db")
        else: 
            datalist = []
            for key in data:
                info = data.get(key)
                datalist.append(info)
            return render_template("staff_catalogue.html", form=form, datalist=datalist, logged=login_status, name=db2['name'][db_index], admin=db2['admin'][db_index], i=db_index)
    return render_template("staff_catalogue.html", form=form, logged=login_status, name=db2['name'][db_index], admin=db2['admin'][db_index], i=db_index)

@app.route("/update/<id>", methods=["GET", "POST"])
def update_product(id):
    form = ProductForm()
    if form.validate_on_submit():
        data = {}
        db = shelve.open("info.db", "w")
        data = db["Info"]

        info = data.get(id)

        # Removes previous image
        filename = info.get_image()
        path = os.path.join("static/" + filename)
        os.remove(path)

        # Uploads new image
        f = form.product_image.data
        filename = secure_filename(f.filename)
        f.save("static/" + filename)

        info.set_name(form.product_name.data)
        info.set_price(form.product_price.data)
        info.set_weight(form.product_weight.data)
        info.set_image(filename)
        info.set_details(form.product_details.data)
        info.set_category(form.product_category.data)

        db["Info"] = data
        db.close()

        return redirect(url_for("staff_catalogue"))
    else:
        data = {}
        db = shelve.open("info.db", "w")
        data = db["Info"]

        info = data.get(id)
        form.product_name.data = info.get_name()
        form.product_price.data = info.get_price()
        form.product_weight.data = info.get_weight()
        form.product_details.data = info.get_details()
        form.product_category.data = info.get_category()

        db["Info"] = data
        db.close()

        return render_template("updateProduct.html", form=form, logged=login_status, name=db['name'][db_index])

@app.route("/deleteProduct/<id>", methods=["POST"])
def delete_product(id):
    data = {}
    db = shelve.open("info.db", "w")
    data = db["Info"]

    info = data.get(id)
    filename = info.get_image()
    path = os.path.join("static/" + filename)
    os.remove(path)
    data.pop(id)

    db["Info"] = data
    db.close()

    return redirect(url_for("staff_catalogue"))

# Login, Sign Up, Users Page


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():

    db = shelve.open('users.db','c')

    sign_up_form = SignUpForm(request.form)
    if request.method == 'POST' and sign_up_form.validate():

      db['name'] += [sign_up_form.username.data]
      db['password'] += [sign_up_form.password.data]

      db['email'] += [sign_up_form.email.data]
      db['location'] += [sign_up_form.location.data]

      db['admin'] += [False]

      global db_index, login_status
      db_index = len(db['name']) - 1
      login_status = True

      return redirect(url_for('home'))
    return render_template('signUp.html', form=sign_up_form, admin=db['admin'][db_index])

@app.route('/Login', methods=['GET', 'POST'])
def Login():

  error_msg = None
  db = shelve.open('users.db', 'c')

  login_form = LoginForm(request.form)
  if request.method == 'POST' and login_form.validate():

    if login_form.login_name.data in db['name']:
      print('Login form: Username match')

      i = db['name'].index(login_form.login_name.data)

      if login_form.login_pass.data == db['password'][i]:
        print('Login form: Password match')
        error_msg = None

        global db_index, login_status
        db_index = i
        login_status = True

        if db['admin'][i] == True:
          return redirect(url_for('users'))
        else:
          return redirect(url_for('home'))

    error_msg = 'Invalid username or password. Please try again'
  return render_template('login.html', form=login_form, error=error_msg, admin=db['admin'][db_index])

@app.route("/users")
def users():

  db = shelve.open('users.db', 'c')

  return render_template('users.html', logged=login_status, length=len(db['name']), database=db, admin=db['admin'][db_index], name=db['name'][db_index], i=db_index)

@app.route("/profile/<account_name>", methods=['GET', 'POST'])
def profile(account_name):
  
  global db_index
  db = shelve.open('users.db', 'c', writeback=True)

  profile_form = ProfileForm(request.form)
  if profile_form.validate():
    db['name'][db_index] = str(profile_form.profile_name.data)
    db['password'][db_index] = str(profile_form.profile_pass.data)
    db['email'][db_index] = str(profile_form.profile_email.data)
    db['location'][db_index] = str(profile_form.profile_location.data)

    print(profile_form.profile_pass.data + ' -> ' + db['password'][db_index])
    print('Updated user profile')

    db.close()

    return redirect(url_for('home'))

  logout_form = LogoutForm(request.form)
  if logout_form.validate():
    print('Logged user out')

    global login_status
    db_index = -1
    login_status = False

    db.close()

    return redirect(url_for('home'))

  return render_template('profile.html', logged=login_status, form=profile_form, form2=logout_form, database=db, admin=db['admin'][db_index], name=db['name'][db_index], i=db_index)

# Checkout, Cart Persistence
idlist = []

@app.route("/cart/<id>")
def cart(id):
    global idlist

    idlist.append(id)
    session["ID"] = idlist

    return redirect(url_for("catalogue"))

@app.route("/order")
def checkout():
    ids = session.get("ID")

    db = shelve.open("info.db", "c")
    data = db["Info"]
    db.close()

    datalist = []

    for x in ids:
        info = data.get(x)
        datalist.append(info)
    return render_template("order.html", datalist=datalist)

@app.route("/checkout")
def checkout():
    ids = session.get("ID")

    db = shelve.open("info.db", "c")
    data = db["Info"]
    db.close()

    datalist = []

    for x in ids:
        info = data.get(x)
        datalist.append(info)
    return render_template("checkout.html", datalist=datalist)

@app.route('/index')
def index():
    ids = session.get("ID")

    db = shelve.open("info.db", "c")
    data = db["Info"]
    db.close()

    datalist = []

    for x in ids:
        info = data.get(x)
        datalist.append(info)
    
    data1 = Data.query.all()
    return render_template('index.html', datalist=datalist, data1=data1)

@app.route("/order")
def order():
    ids = session.get("ID")

    db = shelve.open("info.db", "c")
    data = db["Info"]
    db.close()

    datalist = []

    for x in ids:
        info = data.get(x)
        datalist.append(info)
    return render_template("order.html", datalist=datalist)

@app.route('/checkout', methods=['GET', 'POST'])
def create_customer():
    form = CreateUserForm()

    if form.validate_on_submit():
        new_data = Data(
            email = form.email.data,
            state = form.state.data,
            postalcode = form.postalcode.data,
            contact = form.contact.data,
            paymentmethod = form.paymentmethod.data,
            cardholder = form.cardholder.data,
            cardnumber = form.cardnumber.data,
            expiry = form.expiry.data,
            cvc = form.cvc.data,
        )
        db.session.add(new_data)
        db.session.commit()

        flash(f'Data has been submitted!')
        return redirect(url_for('success'))

    return render_template('checkout.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/deleteuser/<int:id>', methods=['POST'])
def delete_user(user_id):

    try:
        obj = db.session.query(Data).filter_by(id=user_id)
        db.session.delete(obj)
    except:
        print("User is not found")

    return redirect(url_for('staffpage.html'))

if __name__ == "__main__":
    app.run(debug=True)