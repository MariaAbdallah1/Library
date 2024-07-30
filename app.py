import csv
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Path to the CSV file
CSV_FILE = 'books.csv'

def read_books():
    books = []
    try:
        with open(CSV_FILE, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            books = [row for row in reader]
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        pass
    except PermissionError:
        flash('Permission denied: Unable to access the file.', 'error')
    return books

def write_book(title, author):
    try:
        with open(CSV_FILE, 'a', newline='') as csvfile:
            fieldnames = ['title', 'author', 'borrowed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header only if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'title': title, 'author': author, 'borrowed': 'False'})
    except PermissionError:
        flash('Permission denied: Unable to write to the file.', 'error')

def remove_book(title):
    books = read_books()
    books = [book for book in books if book['title'] != title]
    try:
        with open(CSV_FILE, 'w', newline='') as csvfile:
            fieldnames = ['title', 'author', 'borrowed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)
    except PermissionError:
        flash('Permission denied: Unable to write to the file.', 'error')

def borrow_book(title):
    books = read_books()
    books_to_keep = []
    book_found = False

    for book in books:
        if book['title'] == title and book['borrowed'] == 'False':
            book_found = True
        else:
            books_to_keep.append(book)
    
    if book_found:
        try:
            with open(CSV_FILE, 'w', newline='') as csvfile:
                fieldnames = ['title', 'author', 'borrowed']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(books_to_keep)
        except PermissionError:
            flash('Permission denied: Unable to write to the file.', 'error')
        return True
    return False

def return_book(title, author):
    books = read_books()
    book_found = False

    # Check if the book already exists
    for book in books:
        if book['title'] == title and book['author'] == author:
            book_found = True
    
    # If the book is not found, add it back
    if not book_found:
        write_book(title, author)
        return True
    return False

@app.route('/')
def index():
    books = read_books()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        write_book(title, author)
        flash('Book added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove_book_route():
    if request.method == 'POST':
        title = request.form['title']
        remove_book(title)
        flash('Book removed successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('remove_book.html')

@app.route('/borrow', methods=['GET', 'POST'])
def borrow_book_route():
    if request.method == 'POST':
        title = request.form['title']
        if borrow_book(title):
            flash('Book borrowed successfully!', 'success')
        else:
            flash('Book not found or already borrowed.', 'error')
        return redirect(url_for('index'))
    return render_template('borrow_book.html')

@app.route('/return', methods=['GET', 'POST'])
def return_book_route():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        if return_book(title, author):
            flash('Book returned successfully!', 'success')
        else:
            flash('Book not found or already returned.', 'error')
        return redirect(url_for('index'))
    return render_template('return_book.html')
@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('search', '').lower()
    books = read_books()
    if query:
        books = [book for book in books if query in book['title'].lower() or query in book['author'].lower()]
    return render_template('index.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
