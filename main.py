from flask import Flask, render_template , request , redirect , session , url_for
from database.db import obj
app = Flask(__name__)

app.secret_key = "1245"

@app.route('/')
def home():
    return render_template("home.html")
@app.route('/menulist')
def menulist():
    foodlist=obj.foodlist()
    return render_template("menu/menulist.html",foodlist=foodlist )

@app.route("/detail/<id>/<nomi>/")
def menudetail(id , nomi):
    ovqat =obj.menudetail(id)
    return render_template("menu/menudetall.html" , ovqat=ovqat ,nomi=nomi)

# @app.route("/savatcha")
# def savatcha():
#     if session.get('username') :
#         zakazlar = obj.savatcha()
#         return render_template("zakaz/savatcha.html" , zakazlar = zakazlar)
#     else:
#         return redirect(url_for('login'))

@app.route("/addsavat/<ovqatid>/")
def addsavat(ovqatid):
    if session.get('username' , False):
        userid = session['username'][0]
        soni = 1
        zakazid = 6
        obj.addsavat(userid , ovqatid ,zakazid ,  soni )
        return redirect(url_for('menulist'))

@app.route("/user/login/",methods = ['GET' , 'POST'])
def login():
    if request.method == 'GET':
         return render_template("users/login.html" , xato= None)
    elif request.method =='POST':
        log = request.form['login']
        parol = request.form['parol']

        user = obj.check_user(log,parol)

        if user:
            session['username'] = user
            return redirect('/')
        else:
            return render_template("users/login.html" , xato="xato")
@app.route('/user/registration' , methods=['GET' , 'POST'])
def reg():
    if request.method =='GET':
        return render_template("users/register.html")
    elif request.method=='POST':
        ism = request.form['ism']
        familiya = request.form['familiya']
        login = request.form['login']
        pasword = request.form['pasword']

        obj.registratsiya(ism , familiya , login , pasword)
        return redirect('/')


@app.route('/user/logout')
def logout():
    session.pop('username' , None )
    return redirect(url_for('login'))

@app.route('/savatcha/')
def savatcha():
    if session.get('username' , False):
        id = session['username'][0]
        zakazlar = obj.user_savat(id)
        print(zakazlar)
        return render_template("zakaz/savatcha.html", zakazlar=zakazlar)
    else:
        return redirect(url_for('login'))
@app.route("/savatcha/delete/<id>")
def delete_mahsulot(id):
    obj.delmahsulot(id)
    return redirect(url_for('savatcha'))

if __name__ == "__main__":
    app.run(debug=True)
