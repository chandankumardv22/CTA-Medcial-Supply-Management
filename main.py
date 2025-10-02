from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import json

# Load config
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

# Flask app setup
local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Database configuration
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['proud_uri']

db = SQLAlchemy(app)

# Models
class Medicines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    medicines = db.Column(db.String(500), nullable=False)
    products = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mid = db.Column(db.String(120), nullable=False)

class Posts(db.Model):
    mid = db.Column(db.Integer, primary_key=True)
    medical_name = db.Column(db.String(80), nullable=False)
    owner_name = db.Column(db.String(200), nullable=False)
    phone_no = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(120), nullable=False)

class Addmp(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    medicine = db.Column(db.String, nullable=False)

class Addpd(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String, nullable=False)

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.String, nullable=True)
    action = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(100), nullable=False)

# Routes
@app.route("/")
def hello():
    return render_template('index.html', params=params)

@app.route("/index")
def home():
    if 'user' in session and session['user'] == params['user']:
        posts = Posts.query.all()
        return render_template('dashbord.html', params=params, posts=posts)
    else:
        flash("Please login first.", "warning")
        return redirect('/login')

@app.route("/search", methods=['GET','POST'])
def search():
    if request.method == 'POST':
        name = request.form.get('search')
        post = Addmp.query.filter_by(medicine=name).first()
        pro = Addpd.query.filter_by(product=name).first()
        if post or pro:
            flash("Item is available.", "success")
        else:
            flash("Item is not available.", "danger")
    return render_template('search.html', params=params)

@app.route("/details", methods=['GET','POST'])
def details():
    if 'user' in session and session['user'] == params['user']:
        posts = Logs.query.all()
        return render_template('details.html', params=params, posts=posts)
    else:
        flash("Please login first.", "warning")
        return redirect('/login')

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html', params=params)

@app.route("/insert", methods=['GET','POST'])
def insert():
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    if request.method == 'POST':
        mid = request.form.get('mid')
        medical_name = request.form.get('medical_name')
        owner_name = request.form.get('owner_name')
        phone_no = request.form.get('phone_no')
        address = request.form.get('address')
        new_post = Posts(mid=mid, medical_name=medical_name, owner_name=owner_name, phone_no=phone_no, address=address)
        db.session.add(new_post)
        db.session.commit()
        flash("Thanks for submitting your details.", "success")
    return render_template('insert.html', params=params)

@app.route("/addmp", methods=['GET','POST'])
def addmp():
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    if request.method == 'POST':
        newmedicine = request.form.get('medicine')
        entry = Addmp(medicine=newmedicine)
        db.session.add(entry)
        db.session.commit()
        flash("Thanks for adding new items.", "success")
    return render_template('search.html', params=params)

@app.route("/addpd", methods=['GET','POST'])
def addpd():
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    if request.method == 'POST':
        newproduct = request.form.get('product')
        entry = Addpd(product=newproduct)
        db.session.add(entry)
        db.session.commit()
        flash("Thanks for adding new items.", "success")
    return render_template('search.html', params=params)

@app.route("/list", methods=['GET','POST'])
def post_list():
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    posts = Medicines.query.all()
    return render_template('post.html', params=params, posts=posts)

@app.route("/items", methods=['GET','POST'])
def items():
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    posts = Addmp.query.all()
    return render_template('items.html', params=params, posts=posts)

@app.route("/items2", methods=['GET','POST'])
def items2():
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    posts = Addpd.query.all()
    return render_template('items2.html', params=params, posts=posts)

@app.route("/sp", methods=['GET','POST'])
def sp():
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    posts = Medicines.query.all()
    return render_template('store.html', params=params, posts=posts)

@app.route("/logout")
def logout():
    session.pop('user', None)
    flash("You are logged out.", "primary")
    return redirect('/login')

@app.route("/login", methods=['GET','POST'])
def login():
    if 'user' in session and session['user'] == params['user']:
        return redirect('/index')

    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('password')
        if username == params['user'] and password == params['password']:
            session['user'] = username
            flash("You are logged in.", "success")
            return redirect('/index')
        else:
            flash("Wrong username or password.", "danger")

    return render_template('login.html', params=params)

@app.route("/edit/<int:mid>", methods=['GET','POST'])
def edit(mid):
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    post = Posts.query.filter_by(mid=mid).first()
    if request.method == 'POST':
        post.medical_name = request.form.get('medical_name')
        post.owner_name = request.form.get('owner_name')
        post.phone_no = request.form.get('phone_no')
        post.address = request.form.get('address')
        db.session.commit()
        flash("Data updated successfully.", "success")
        return redirect(f'/edit/{mid}')
    return render_template('edit.html', params=params, post=post)

@app.route("/delete/<int:mid>", methods=['GET','POST'])
def delete(mid):
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    post = Posts.query.filter_by(mid=mid).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        flash("Deleted successfully.", "warning")
    return redirect('/login')

@app.route("/deletemp/<int:id>", methods=['GET','POST'])
def deletemp(id):
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    post = Medicines.query.filter_by(id=id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        flash("Deleted successfully.", "success")
    return redirect('/list')

@app.route("/medicines", methods=['GET','POST'])
def medicine():
    if 'user' not in session or session['user'] != params['user']:
        flash("Please login first.", "warning")
        return redirect('/login')

    if request.method == 'POST':
        mid = request.form.get('mid')
        name = request.form.get('name')
        medicines = request.form.get('medicines')
        products = request.form.get('products')
        email = request.form.get('email')
        amount = request.form.get('amount')

        entry = Medicines(mid=mid, name=name, medicines=medicines, products=products, email=email, amount=amount)
        db.session.add(entry)
        db.session.commit()
        flash("Data added successfully.", "success")

    return render_template('medicine.html', params=params)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

