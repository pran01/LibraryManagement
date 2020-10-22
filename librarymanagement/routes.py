from librarymanagement import app,login_manager,db
from librarymanagement.forms import loginForm, issueForm, returnForm
from flask import render_template,redirect,url_for,flash,request,jsonify,make_response
from flask_login import login_required,current_user,login_user,logout_user
from librarymanagement.models import librarian,issueInfo,member,book
from werkzeug.security import check_password_hash


@app.route("/",methods=["GET","POST"])
def login():
    if(current_user.is_authenticated):
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
    rForm = returnForm()
    return render_template("home.html", issueForm=issueF, returnForm=rForm, current_user=current_user, book=book)


@app.route("/get-book-details",methods=["POST","GET"])
@login_required
def getBooks():
    req=request.get_json()
    memberid=int(req["memberid"])
    res_dict={"memberid":req["memberid"],"bookid":[]}
    issues=issueInfo.query.filter_by(member_id=memberid).all()
    for issue in issues:
        curr_book=book.query.filter_by(id=issue.book_id).first()
        if curr_book:
            res_dict["bookid"].append({"name":curr_book.name,"id":curr_book.id})
    else:
        res = make_response(jsonify(res_dict), 200)
        return res

@app.route("/submit-issue",methods=['POST','GET'])
@login_required
def submitIssue():
    req=request.get_json()
    l=len(req["bookid"])
    for i in range(l):
        newIssue=issueInfo(member_id=int(req["memberid"]),book_id=int(req["bookid"][i]),lib_id=current_user.id)
        db.session.add(newIssue)
        db.session.commit()
        mem=member.query.filter_by(id=int(req["memberid"])).first()
        num_of_books=issueInfo.query.filter_by(member_id=int(req["memberid"])).count()
        if(mem and num_of_books):
            mem.curr_no_books+=1
            db.session.commit()
    else:
        res = make_response(jsonify({"message": "JSON received"}), 200)
        return res

@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))