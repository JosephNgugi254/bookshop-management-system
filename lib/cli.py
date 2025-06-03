# lib/cli.py
import os
import sys
import re
from pathlib import Path
project_root = str(Path.cwd())
sys.path.insert(0, project_root)
import click
from sqlalchemy.orm import sessionmaker
from lib.db.connection import engine, Session
from lib.models.book import Book
from lib.models.author import Author
from lib.models.genre import Genre
from lib.models.sale import Sale
from lib.models.cashier import Cashier
from lib.models.customer import Customer
from datetime import datetime, timezone

session = Session()

def add_book():
    """Add a new book to stock."""
    title = click.prompt("Book title", type=str)
    author = click.prompt("Author name", type=str)
    genre = click.prompt("Genre", type=str)
    price = click.prompt("Price", type=float)
    quantity = click.prompt("Quantity", type=int)
    
    if price <= 0 or quantity < 0:
        click.echo("Price must be positive and quantity non-negative.")
        return
    author_obj = session.query(Author).filter_by(name=author).first()
    if not author_obj:
        author_obj = Author(name=author)
        session.add(author_obj)
    genre_obj = session.query(Genre).filter_by(name=genre).first()
    if not genre_obj:
        genre_obj = Genre(name=genre)
        session.add(genre_obj)
    book = Book(title=title, author=author_obj, genre=genre_obj, price=price, quantity=quantity)
    session.add(book)
    session.commit()
    click.echo(f"Added {title} to stock.")

def list_books():
    """List all books in stock."""
    books = session.query(Book).all()
    if not books:
        click.echo("No books in stock.")
        return
    click.echo("Books in stock:")
    book_list = [(book.id, book.title, book.author.name, book.genre.name, book.price, book.quantity) for book in books]
    for book in book_list:
        click.echo(f"{book[0]}. {book[1]} ({book[2]}, {book[3]}) - ${book[4]:.2f}, {book[5]} in stock")

def sell_book():
    """Sell a book and update stock."""
    book_id = click.prompt("Book ID", type=int)
    quantity = click.prompt("Quantity sold", type=int)
    cashier_name = click.prompt("Cashier name", type=str)
    customer_name = click.prompt("Customer name", type=str)
    customer_phone = click.prompt("Customer phone number (07xxxxxxxx)", type=str)
    
    # Validate inputs
    if quantity <= 0:
        click.echo("Quantity sold must be positive.")
        return
    if not re.match(r'^07\d{8}$', customer_phone):
        click.echo("Phone number must be in format 07xxxxxxxx (10 digits starting with 07).")
        return
    
    # Check book
    book = session.query(Book).filter_by(id=book_id).first()
    if not book:
        click.echo(f"Book ID {book_id} not found.")
        return
    if book.quantity < quantity:
        click.echo(f"Error: Only {book.quantity} in stock.")
        return
    
    # Get or create cashier
    cashier = session.query(Cashier).filter_by(name=cashier_name).first()
    if not cashier:
        cashier = Cashier(name=cashier_name)
        session.add(cashier)
        session.commit()  # Commit to get cashier.id
    
    # Get or create customer
    try:
        customer = session.query(Customer).filter_by(phone_number=customer_phone).first()
        if not customer:
            customer = Customer(name=customer_name, phone_number=customer_phone)
            session.add(customer)
            session.commit()  # Commit to get customer.id
        elif customer.name != customer_name:
            click.echo("Phone number already exists with a different name.")
            return
    except ValueError as e:
        click.echo(f"Error: {e}")
        return
    
    # Update stock and record sale
    book.quantity -= quantity
    total_price = book.price * quantity
    sale = Sale(book_id=book.id, cashier_id=cashier.id, customer_id=customer.id, quantity=quantity, total_price=total_price, sale_date=datetime.now(timezone.utc))
    session.add(sale)
    session.commit()
    click.echo(f"Sold {quantity} copies of {book.title}. {book.quantity} remaining.")

def list_authors():
    """List all authors and their book counts."""
    authors = session.query(Author).all()
    author_dict = {author.id: (author.name, len(author.books)) for author in authors}
    if not author_dict:
        click.echo("No authors found.")
        return
    click.echo("Authors:")
    for author_id, (name, count) in author_dict.items():
        click.echo(f"- {name}: {count} books")

def list_genres():
    """List all genres and their book counts."""
    genres = session.query(Genre).all()
    genre_dict = {genre.id: (genre.name, len(genre.books)) for genre in genres}
    if not genre_dict:
        click.echo("No genres found.")
        return
    click.echo("Genres:")
    for genre_id, (name, count) in genre_dict.items():
        click.echo(f"- {name}: {count} books")

def view_sold_books():
    """View all sold books."""
    sales = session.query(Sale).all()
    if not sales:
        click.echo("No sales recorded.")
        return
    click.echo("Sold books:")
    sale_list = [(sale.id, sale.book.title, sale.quantity, sale.total_price, sale.sale_date, sale.cashier.name, sale.customer.name, sale.customer.phone_number) for sale in sales]
    for sale in sale_list:
        click.echo(f"Sale {sale[0]}: {sale[1]} - {sale[2]} copies,Total amount: ${sale[3]:.2f},Date: {sale[4]},Cashier: {sale[5]},Customer: {sale[6]} ({sale[7]})")

def cli():
    """Bookshop Management System CLI with numbered menu."""
    menu = {
        "1": ("Add book", add_book),
        "2": ("List books", list_books),
        "3": ("Sell book", sell_book),
        "4": ("List authors", list_authors),
        "5": ("List genres", list_genres),
        "6": ("View sold books", view_sold_books),
        "7": ("Exit", None)
    }
    
    while True:
        click.echo("\nBookshop Management System")
        for key, (description, _) in menu.items():
            click.echo(f"{key}. {description}")
        choice = click.prompt("Enter choice", type=str)
        
        if choice not in menu:
            click.echo("Invalid choice. Please select a number from 1 to 7.")
            continue
        
        if choice == "7":
            click.echo("Exiting...")
            break
        
        _, func = menu[choice]
        try:
            func()
        except Exception as e:
            click.echo(f"Error: {e}")

if __name__ == "__main__":
    cli()