# Bookshop Management System

A simple CLI application to manage a bookshop's inventory and sales, built with Python, SQLAlchemy, and Click. This project demonstrates a user-friendly interface for adding books, tracking sales, and viewing data, using a SQLite database and ORM.

## Features

- **Add books** to stock with title, author, genre, price, and quantity.
- **List all books** with details (ID, title, author, genre, price, stock).
- **Sell books**, update stock, and record sales.
- **View authors and genres** with their book counts.
- **Display sold books** with quantity, total price, and sale date.

## Setup

1. **Install Pipenv:**
    ```bash
    pip install pipenv
    ```

2. **Set up environment and run:**
    ```bash
    pipenv install
    pipenv shell
    python3 lib/db/seed.py
    python3 lib/cli.py
    ```

3. **Run tests:**
    ```bash
    pytest
    ```

## Usage

Run `python3 lib/cli.py` to start the CLI. Choose options 1–7 to manage books:

1. **Add book:** Enter book details to add to stock.
2. **List books:** View all books in stock.
3. **Sell book:** Sell a book by ID and quantity.
4. **List authors:** See authors and their book counts.
5. **List genres:** See genres and their book counts.
6. **View sold books:** View sales history.
7. **Exit:** Close the application.

## Project Structure

- `lib/cli.py`: CLI interface with numbered menu.
- `lib/db/`: Database connection (`connection.py`) and seed script (`seed.py`).
- `lib/models/`: SQLAlchemy models (`author.py`, `book.py`, `genre.py`, `sale.py`).
- `tests/`: Pytest files for models.
- `bookshop.db`: SQLite database.

## Technologies

- **Python 3.12:** Core programming language.
- **SQLAlchemy:** ORM for database management.
- **Click:** CLI framework for user input.
- **SQLite:** Lightweight database.
- **Pytest:** Testing framework.

## Troubleshooting

- **ModuleNotFoundError:** Run scripts from project root or check `sys.path` in scripts.
- **Database issues:** Re-run `python3 lib/db/seed.py` to reset `bookshop.db`.
- **Test failures:** Use `pytest -s` for details.
- **Dependencies:** Install with `pipenv install sqlalchemy click pytest`.
- **Timezone errors:** Ensure `timezone.utc` is used for datetimes.

## License

MIT License. Created by Joseph Ngugi for Phase 3 project submission.
