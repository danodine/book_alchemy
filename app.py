import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

app = Flask(__name__)

app.secret_key = 'super-secret-key-123'

db_path = os.path.join(os.getcwd(), 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

# with app.app_context():
    # db.create_all()

@app.route('/')
def home():
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort')

    query = Book.query

    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))

    if sort == "title":
        query = query.order_by(Book.title)
    elif sort == "author":
        query = query.join(Author).order_by(Author.name)

    books = query.all()
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

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)
    db.session.commit()

    if len(author.books) == 0:
        db.session.delete(author)
        db.session.commit()
        flash(f"Book '{book.title}' and author '{author.name}' deleted successfully.")
    else:
        flash(f"Book '{book.title}' deleted successfully.")

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)