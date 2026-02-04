from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)  # auto-increment PK
    name = db.Column(db.String(200), nullable=False, unique=True)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship("Book", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Author id={self.id} name={self.name!r}>"

    def __str__(self):
        return self.name


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)  # auto-increment PK
    isbn = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(300), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    author = db.relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book id={self.id} title={self.title!r} isbn={self.isbn!r}>"

    def __str__(self):
        return self.title
