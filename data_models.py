"""
Database models for a simple library system using SQLAlchemy.

This module defines two models:
- Author: Represents a book author.
- Book: Represents a book associated with an author.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """
    Author model for storing author information.

    Attributes:
        id (int): Primary key, auto-incremented.
        name (str): Name of the author.
        birth_date (str): Date of birth (as string).
        date_of_death (str): Date of death (as string).
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    date_of_death = db.Column(db.String)

    def __repr__(self):
        """
        String representation for debugging.
        """
        return f'<Author {self.name}>'

    def __str__(self):
        """
        User-friendly string representation.
        """
        return self.name


class Book(db.Model):
    """
    Book model for storing book information.

    Attributes:
        id (int): Primary key, auto-incremented.
        isbn (str): ISBN identifier of the book.
        title (str): Title of the book.
        publication_year (int): Year the book was published.
        author_id (int): Foreign key referencing Author.
        author (Author): Relationship to the Author model.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String)
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        """
        String representation for debugging.
        """
        return f'<Book {self.title}>'

    def __str__(self):
        """
        User-friendly string representation.
        """
        return self.title
