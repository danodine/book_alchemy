import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

app = Flask(__name__)

db_path = os.path.join(os.getcwd(), 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

# with app.app_context():
    # db.create_all()

@app.route('/')
def home():
    sort = request.args.get('sort')
    if sort == "title":
        books = Book.query.order_by(Book.title).all()
    elif sort == "author":
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.all()
    return render_template("home.html", books=books)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    message = ''
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form['date_of_death']
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        message = 'Author added successfully!'
    return render_template("add_author.html", message=message)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
  message = ''
  authors = Author.query.all()  # Send authors to template for dropdown
  if request.method == 'POST':
      title = request.form['title']
      isbn = request.form['isbn']
      publication_year = request.form['publication_year']
      author_id = request.form['author_id']
      new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
      db.session.add(new_book)
      db.session.commit()
      message = 'Book added successfully!'
  return render_template("add_book.html", authors=authors, message=message)

if __name__ == '__main__':
    app.run(debug=True)