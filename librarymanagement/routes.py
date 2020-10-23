from librarymanagement import app,login_manager,db
from librarymanagement.forms import loginForm, issueForm, returnForm
from flask import render_template,redirect,url_for,flash,request,jsonify,make_response
from flask_login import login_required,current_user,login_user,logout_user
from librarymanagement.models import *
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
        calculated_fine=0
        if(curr_day-issued_day>15):
            calculated_fine=(curr_day-issued_day)*2
        else:
            calculated_fine=0
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

@app.route("/register",methods=["POST","GET"])
@login_required
def register():
    return render_template("register.html")

@app.route("/register-member",methods=["POST","GET"])
@login_required
def registermember():
    registerDetails=request.get_json()
    new_member=member(name=registerDetails["name"],email=registerDetails["email"],address=registerDetails["address"],isAdult=registerDetails["isAdult"])
    db.session.add(new_member)
    db.session.commit()
    if(len(registerDetails["mobile"])):
        for mobile in registerDetails["mobile"]:
            mem_mobile=memberMobile(member_id=new_member.id,mobile=mobile)
            db.session.add(mem_mobile)
            db.session.commit()
    res=make_response(jsonify({"message":"JSON received"}),200)
    return res

@app.route("/show-books",methods=["POST","GET"])
@login_required
def showbooks():
    return render_template("showbooks.html")

@app.route("/show-books/show",methods=["GET"])
@login_required
def show():
    available_json={"books":[],"authors":[],"genres":[]}
    available_books=book.query.filter_by(is_issued=0).all()
    for available_book in available_books:
        bookid=available_book.id
        bookname=available_book.name
        bookauthor=bookAuthor.query.filter_by(book_id=bookid).first().author
        bookgenres=[]
        genres=bookGenre.query.filter_by(book_id=bookid).all()
        for genre in genres:
            bookgenres.append(genre.genre)
        available_json["books"].append({"id":bookid,"name":bookname,"author":bookauthor,"genres":bookgenres})
    authors=bookAuthor.query.all()
    for author in authors:
        if(author.author not in available_json["authors"]):
            available_json["authors"].append(author.author)
    all_genres=bookGenre.query.all()
    for genre in all_genres:
        if(genre.genre not in available_json["genres"]):
            available_json["genres"].append(genre.genre)
    return jsonify(available_json)


@app.route("/filter-books",methods=["POST","GET"])
@login_required
def filterbooks():
    filter_details=request.get_json()
    filtered_authors=filter_details["authors"]
    filtered_genres=filter_details["genres"]
    available_json={"books":[]}
    available_books=book.query.filter_by(is_issued=0).all()
    for available_book in available_books:
        bookid=available_book.id
        bookname=available_book.name
        bookauthor=bookAuthor.query.filter_by(book_id=bookid).first().author
        bookgenres=[]
        genres=bookGenre.query.filter_by(book_id=bookid).all()
        for genre in genres:
            bookgenres.append(genre.genre)
        if(len(filtered_authors)):
            if(bookauthor in filtered_authors):
                if(len(filtered_genres)):
                    if(len(set(bookgenres)-set(filtered_genres))!=len(set(bookgenres))):
                        available_json["books"].append({"id":bookid,"name":bookname,"author":bookauthor,"genres":bookgenres})
                else:
                    available_json["books"].append({"id":bookid,"name":bookname,"author":bookauthor,"genres":bookgenres})
        else:
            if(len(filtered_genres)):
                if(len(set(bookgenres)-set(filtered_genres))!=len(set(bookgenres))):
                    available_json["books"].append({"id":bookid,"name":bookname,"author":bookauthor,"genres":bookgenres})
            else:
                available_json["books"].append({"id":bookid,"name":bookname,"author":bookauthor,"genres":bookgenres})
    
    res=make_response(jsonify(available_json),200)
    return res

@app.route("/issued-by-me",methods=["POST","GET"])
@login_required
def issuedbyme():
    issues=issueInfo.query.filter_by(lib_id=current_user.id).all()
    return render_template("issuedbyme.html",current_user=current_user,issues=issues)

