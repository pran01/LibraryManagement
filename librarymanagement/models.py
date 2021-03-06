from librarymanagement import db,login_manager
from flask_login import UserMixin
from datetime import datetime

class member(UserMixin,db.Model):
    __tablename__="member"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.Text, unique = True, nullable = False)
    isAdult = db.Column(db.Boolean, nullable = False)
    address = db.Column(db.Text, nullable = False)
    curr_no_books = db.Column(db.Integer, default = 0)
    mobiles = db.relationship("memberMobile", backref = "member", lazy = True)
    member_issueInfo  = db.relationship("issueInfo", backref = "member", lazy = True) 

    def __repr__(self):
        return f"member('{self.id}', '{self.name}', '{self.email}')"

class memberMobile(UserMixin,db.Model):
    __tablename__="membermobile"
    dummy_column=db.Column(db.Integer,primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable = False)
    mobile = db.Column(db.Integer, unique = True, nullable = False)

    def __repr__(self):
        return f"memberMobile('{self.member_id}', '{self.mobile}')"



class librarian(UserMixin,db.Model):
    __tablename__="librarian"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.Text, unique = True, nullable = False)
    password = db.Column(db.String(64), nullable = False)
    address = db.Column(db.Text, nullable = False)
    doj = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    shift_from = db.Column(db.String(4), nullable = False)
    shift_till = db.Column(db.String(4), nullable = False)
    mobiles = db.relationship("librarianMobile", backref = "librarian", lazy = True)
    librarian_issueInfo  = db.relationship("issueInfo", backref = "librarian",lazy=True) 

    def __repr__(self):
        return f"librarian('{self.id}', '{self.name}', '{self.doj}')"

class librarianMobile(UserMixin,db.Model):
    __tablename__="librarianmobile"
    dummy_column=db.Column(db.Integer,primary_key=True)
    lib_id = db.Column(db.Integer, db.ForeignKey("librarian.id"),nullable = False)
    mobile = db.Column(db.Integer, unique = True, nullable = False)

    def __repr__(self):
        return f"librarianMobile('{self.lib_id}', '{self.mobile}')"

@login_manager.user_loader
def load_user(user_id):
    return librarian.query.get(int(user_id))

class book(UserMixin,db.Model):
    __tablename__="book"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    publisher = db.Column(db.String(50), nullable = False)
    isbn = db.Column(db.Integer, unique = True, nullable = True) #May be nullable if the book is old
    is_issued=db.Column(db.Boolean)
    genres = db.relationship("bookGenre", backref = "book", lazy = True)
    authors = db.relationship("bookAuthor", backref = "book", lazy = True)
    book_issueInfo  = db.relationship("issueInfo", backref = "book", lazy = True) 
    issueStatus = db.relationship("issuedOrReturned", backref = "book", lazy = True) 

    def __repr__(self):
        return f"book('{self.id}', '{self.name}', '{self.publisher}', '{self.isbn}', '{self.is_issued}')"

class bookGenre(UserMixin,db.Model):
    __tablename__="bookgenre"
    dummy_column=db.Column(db.Integer,primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable = False)
    genre = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f"bookGenre('{self.book_id}', '{self.genre}')"

class bookAuthor(UserMixin,db.Model):
    __tablename__="bookauthor"
    dummy_column=db.Column(db.Integer,primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable = False)
    author = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f"bookAuthor('{self.book_id}', '{self.author}')"

class issueInfo(UserMixin,db.Model):
    __tablename__="issueinfo"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) #Check if default is required here
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable = False)
    lib_id = db.Column(db.Integer, db.ForeignKey("librarian.id"), nullable = False)
    issueStatus = db.relationship("issuedOrReturned", backref = "issueinfo", lazy = True)

    def __repr__(self):
        return f"issueInfo('{self.id}', '{self.date}', '{self.member_id}', '{self.book_id}', '{self.lib_id}')"

class issuedOrReturned(UserMixin,db.Model):
    __tablename__="issuedorreturned"
    dummy_column=db.Column(db.Integer,primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey("issueinfo.id"), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable = False)
    return_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) #Check if default is required here

    def __repr__(self):
        return f"issuedOrReturned('{self.issue_id}', '{self.book_id}', '{self.return_date}')"