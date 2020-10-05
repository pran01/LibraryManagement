from librarymanagement import db

class member(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    isAdult = db.Column(db.Boolean, nullable = False)
    address = db.Column(db.Text, nullable = False)
    curr_no_books = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return "<Task %r>" % self.id

