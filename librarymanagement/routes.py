from librarymanagement import app,login_manager
from librarymanagement.forms import loginForm, issueForm, returnForm
from flask import render_template,redirect,url_for,flash,request,jsonify,make_response
from flask_login import login_required,current_user,login_user,logout_user
from librarymanagement.models import librarian
from werkzeug.security import check_password_hash


@app.route("/",methods=["GET","POST"])
def login():
    if(current_user.is_authenticated()):
        return redirect(url_for("home"))
    form=loginForm()
    if form.validate_on_submit():
        user=librarian.query.filter_by(email=form.email.data).first()
        if user:
            if(check_password_hash(user.password,form.password.data)):
                login_user(user)
                flash("Login Successful","success")
                return redirect(url_for('home'))
            else:
                flash("Password Incorrect",'danger')
                return redirect(url_for('login'))
        else:
            flash("user does not exist",'danger')
            return redirect(url_for('login'))
    return render_template("login.html",form=form)

@app.route("/home",methods=['POST','GET'])
@login_required
def home():
    issueF = issueForm()
    returnF = returnForm()
    
    return render_template("home.html", issueForm=issueF, returnForm=returnF)

@app.route("/submit-issue",methods=['POST','GET'])
@login_required
def submitIssue():
    req=request.get_json()
    print(req)
    res = make_response(jsonify({"message": "JSON received"}), 200)
    return res



@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))