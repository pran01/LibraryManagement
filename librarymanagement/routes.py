from librarymanagement import app,login_manager,db
from librarymanagement.forms import loginForm, issueForm, returnForm
from flask import render_template,redirect,url_for,flash,request,jsonify,make_response
from flask_login import login_required,current_user,login_user,logout_user
from librarymanagement.models import librarian,issueInfo,member,book,issuedOrReturned
from werkzeug.security import check_password_hash
from datetime import datetime

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
    unique_bookid=[]
    issues=issueInfo.query.filter_by(member_id=memberid).all()
    for issue in issues:
        curr_book=book.query.filter_by(id=issue.book_id).first()
        if curr_book and curr_book.is_issued and (curr_book.id not in unique_bookid):
            res_dict["bookid"].append({"name":curr_book.name,"id":curr_book.id})
            unique_bookid.append(curr_book.id)
    else:
        res = make_response(jsonify(res_dict), 200)
        return res

@app.route("/submit-return",methods=["POST","GET"])
@login_required
def submitreturn():
    returnId=request.get_json()
    returnBookId=returnId["bookid"]
    for bookId in returnBookId:
        issued=issueInfo.query.filter_by(book_id=bookId).first()
        returned=issuedOrReturned(issue_id=issued.id,book_id=issued.book_id)
        issued.book.is_issued=0
        issued.member.curr_no_books-=1
        db.session.add(returned)
        db.session.commit()
    else:
        res = make_response(jsonify({"message":"JSON received"}), 200)
        return res


@app.route("/calculate-fine",methods=["POST","GET"])
@login_required
def calculatefine():
    returnId=request.get_json()
    returnBookId=returnId["bookid"]
    fine={"fine":0}
    for bookId in returnBookId:
        issued=issueInfo.query.filter_by(book_id=bookId).first()
        now=datetime.utcnow()
        now=now.strftime("%Y-%m-%d %H:%M:%S")
        curr_year=int(now[0:4])
        curr_month=int(now[5:7])
        curr_day=int(now[8:10])
        issued_date=str(issued.date)
        issued_year=int(issued_date[0:4])
        issued_month=int(issued_date[5:7])
        issued_day=int(issued_date[8:10])
        calculated_fine=curr_day-issued_day
        fine["fine"]+=calculated_fine
    else:
        res = make_response(jsonify(fine), 200)
        return res

@app.route("/submit-issue",methods=['POST','GET'])
@login_required
def submitIssue():
    req=request.get_json()
    l=len(req["bookid"])
    for i in range(l):
        newIssue=issueInfo(member_id=int(req["memberid"]),book_id=int(req["bookid"][i]),lib_id=current_user.id)
        curr_book=book.query.filter_by(id=int(req["bookid"][i])).first()
        mem=member.query.filter_by(id=int(req["memberid"])).first()
        if(curr_book.is_issued==0 and mem):
            db.session.add(newIssue)
            mem.curr_no_books+=1
            curr_book.is_issued=1
            db.session.commit()
        else:
            flash("Book already issued","Danger")
    else:
        res = make_response(jsonify({"message": "JSON received"}), 200)
        return res

@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))