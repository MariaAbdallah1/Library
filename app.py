import csv
import os
from flask import Flask, render_template, request, redirect, url_for

class Book:
    def __init__(self, book_id, title, author, year):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self):
        return f'{self.book_id} - {self.title} by {self.author} ({self.year})'

class Library:
    def __init__(self):
        self.books = []
        self.borrowed_books = {}
        self.books_file = 'books.csv'
        self.borrowed_books_file = 'borrowed_books.csv'
        self.ensure_files_exist()
        self.load_books()
        self.load_borrowed_books()

    def ensure_files_exist(self):
        if not os.path.exists(self.books_file):
            with open(self.books_file, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(['book_id', 'title', 'author', 'year'])

        if not os.path.exists(self.borrowed_books_file):
            with open(self.borrowed_books_file, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(['book_id', 'user'])

    def load_books(self):
        with open(self.books_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.books.append(Book(row['book_id'], row['title'], row['author'], row['year']))

    def save_books(self):
        with open(self.books_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['book_id', 'title', 'author', 'year'])
            writer.writeheader()
            for book in self.books:
                writer.writerow({'book_id': book.book_id, 'title': book.title, 'author': book.author, 'year': book.year})

    def load_borrowed_books(self):
        with open(self.borrowed_books_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.borrowed_books[row['book_id']] = row['user']

    def save_borrowed_books(self):
        with open(self.borrowed_books_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['book_id', 'user'])
            writer.writeheader()
            for book_id, user in self.borrowed_books.items():
                writer.writerow({'book_id': book_id, 'user': user})

    def add_book(self, title, author, year):
        book_id = str(len(self.books) + 1)
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id):
        self.books = [book for book in self.books if book.book_id != book_id]
        self.save_books()

    def search_book(self, query):
        return [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]

    def borrow_book(self, book_id, user):
        if book_id not in self.borrowed_books:
            self.borrowed_books[book_id] = user
            self.save_borrowed_books()

    def return_book(self, book_id):
        if book_id in self.borrowed_books:
            del self.borrowed_books[book_id]
            self.save_borrowed_books()

app = Flask(__name__)
library = Library()

@app.route('/')
def index():
    return render_template('index.html', books=library.books, borrowed_books=library.borrowed_books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        library.add_book(title, author, year)
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/remove_book', methods=['GET', 'POST'])
def remove_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        library.remove_book(book_id)
        return redirect(url_for('index'))
    return render_template('remove_book.html')

@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    if request.method == 'POST':
        query = request.form['query']
        results = library.search_book(query)
        return render_template('search_book.html', results=results)
    return render_template('search_book.html', results=[])

@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        user = request.form['user']
        library.borrow_book(book_id, user)
        return redirect(url_for('index'))
    return render_template('borrow_book.html')

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        library.return_book(book_id)
        return redirect(url_for('index'))
    return render_template('return_book.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')