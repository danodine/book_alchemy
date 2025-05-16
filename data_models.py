from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String)
  birth_date = db.Column(db.String)
  date_of_death = db.Column(db.String)

  def __repr__(self):
    return f'<Author {self.name}>'

  def __str__(self):
    return self.name

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  isbn = db.Column(db.String)
  title = db.Column(db.String)
  publication_year = db.Column(db.Integer)
  author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

  author = db.relationship('Author', backref=db.backref('books', lazy=True))

  def __repr__(self):
    return f'<Book {self.title}>'

  def __str__(self):
    return self.title
  