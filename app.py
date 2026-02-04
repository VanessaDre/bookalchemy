import os
from datetime import date

from flask import Flask, render_template, request
from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def _parse_date(value: str | None) -> date | None:
    """Parse YYYY-MM-DD from <input type="date"> into a date object."""
    if not value:
        return None
    return date.fromisoformat(value)


@app.route("/")
def home():
    sort = request.args.get("sort", "title")

    if sort == "author":
        books = (
            Book.query.join(Author)
            .order_by(Author.name.asc(), Book.title.asc())
            .all()
        )
    else:
        books = Book.query.order_by(Book.title.asc()).all()

    return render_template("home.html", books=books, sort=sort)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    success = None
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        birth_date = _parse_date(request.form.get("birth_date"))
        date_of_death = _parse_date(request.form.get("date_of_death"))

        if not name:
            error = "Name ist erforderlich."
            return render_template("add_author.html", success=success, error=error)

        if Author.query.filter_by(name=name).first():
            error = "Autor existiert bereits."
            return render_template("add_author.html", success=success, error=error)

        author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()
        success = "Autor erfolgreich hinzugefügt."

    return render_template("add_author.html", success=success, error=error)


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    success = None
    error = None
    authors = Author.query.order_by(Author.name.asc()).all()

    if request.method == "POST":
        isbn = request.form.get("isbn", "").strip()
        title = request.form.get("title", "").strip()
        publication_year_raw = request.form.get("publication_year", "").strip()
        author_id_raw = request.form.get("author_id", "").strip()

        if not authors:
            error = "Bitte zuerst mindestens einen Autor hinzufügen."
            return render_template("add_book.html", authors=authors, success=success, error=error)

        if not isbn or not title or not author_id_raw:
            error = "ISBN, Titel und Autor sind erforderlich."
            return render_template("add_book.html", authors=authors, success=success, error=error)

        if Book.query.filter_by(isbn=isbn).first():
            error = "Diese ISBN existiert bereits."
            return render_template("add_book.html", authors=authors, success=success, error=error)

        publication_year = int(publication_year_raw) if publication_year_raw else None
        author_id = int(author_id_raw)

        book = Book(
            isbn=isbn,
            title=title,
            publication_year=publication_year,
            author_id=author_id,
        )
        db.session.add(book)
        db.session.commit()
        success = "Buch erfolgreich hinzugefügt."

    return render_template("add_book.html", authors=authors, success=success, error=error)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
