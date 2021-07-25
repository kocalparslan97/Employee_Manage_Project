from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Uygulamamizin gizli anahtari
app.secret_key = "c0532df955dc7e39aa1abf99"

# MySQL ile SQLAlchemy veri tabanini ayarla
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# CRUD veri tabani icin tablo olusturuyoruz
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


# Bu, tüm calisan verilerimizi sorgulayacagimiz dizin rotasıdır
@app.route('/')
def Index():
    # Veri tabaninda kayitli verileri aliyoruz
    all_data = Data.query.all()

    return render_template("index.html", employees=all_data)


# Calisan ekle bolumunde yazilan verileri ekledigimiz yer
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        # islem gerceklestikten sonra kullaniciya gosterilen bilgi mesaji
        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


# Veri tabaninda kayitli calisanin bilgilerini guncellemek icin
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))


# Veri tabaninda kayitli calisanin bilgilerini silmek icin
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
