

import json
from pathlib import Path
from .book import Book # Import the Book class from the same package
import logging # Required for Task 5 [cite: 38]

# Setup basic logging (Task 5)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BOOK_CATALOG_FILE = Path("book_catalog.json") # File path for persistence (Task 3) [cite: 31]

class LibraryInventory:
    """Manages the collection of Book objects."""
    def __init__(self):
        """Initializes the inventory and attempts to load data from file."""
        self.books: list[Book] = []
        self.load_from_file()

    # --- Persistence Methods (Task 3) ---

    def load_from_file(self):
        """Loads book data from the JSON file, handling file exceptions[cite: 30, 32]."""
        try:
            if BOOK_CATALOG_FILE.exists():
                with open(BOOK_CATALOG_FILE, 'r') as f:
                    data = json.load(f)
                    # Recreate Book objects from the loaded dicts
                    self.books = [Book(**book_data) for book_data in data]
                logging.info(f"Successfully loaded {len(self.books)} books from catalog.")
            else:
                logging.warning(f"Catalog file not found at {BOOK_CATALOG_FILE}. Starting with an empty inventory.")
        except json.JSONDecodeError as e:
            # Handles corrupted file (Task 3, 5) [cite: 32, 37]
            logging.error(f"Error decoding JSON from file: {e}")
            self.books = [] # Start fresh if file is corrupted
        except Exception as e:
            # General file handling (Task 5) [cite: 37]
            logging.error(f"An unexpected error occurred during file load: {e}")
            self.books = []

    def save_to_file(self):
        """Saves the current book inventory to the JSON file."""
        try:
            # Convert Book objects back into list of dictionaries
            data_to_save = [book.to_dict() for book in self.books]
            with open(BOOK_CATALOG_FILE, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            logging.info("Catalog successfully saved.")
        except Exception as e:
            logging.error(f"Error saving catalog to file: {e}")

    # --- Core Management Methods (Task 2) ---

    def add_book(self, book: Book):
        """Adds a new Book object to the inventory."""
        self.books.append(book)
        self.save_to_file()
        logging.info(f"Book added: {book.title}")

    def search_by_title(self, query: str) -> list[Book]:
        """Searches for books whose title contains the query string (case-insensitive)."""
        return [book for book in self.books if query.lower() in book.title.lower()]

    def search_by_isbn(self, isbn: str) -> Book | None:
        """Searches for a book by its exact ISBN."""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self):
        """Displays all books in the inventory."""
        if not self.books:
            print("The library catalog is empty.")
            return

        print("\n--- Full Library Catalog ---")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")
        print("----------------------------\n")

    # Add issue_book_by_isbn and return_book_by_isbn methods for CLI
    def issue_book_by_isbn(self, isbn: str) -> bool:
        """Finds a book by ISBN and issues it."""
        book = self.search_by_isbn(isbn)
        if book:
            if book.issue():
                self.save_to_file()
                logging.info(f"Book successfully issued: {book.title}")
                return True
            else:
                print(f"Book '{book.title}' is already issued.")
        else:
            print("Book with that ISBN not found.")
        return False
    
    def return_book_by_isbn(self, isbn: str) -> bool:
        """Finds a book by ISBN and returns it."""
        book = self.search_by_isbn(isbn)
        if book:
            if book.return_book():
                self.save_to_file()
                logging.info(f"Book successfully returned: {book.title}")
                return True
            else:
                print(f"Book '{book.title}' is already available.")
        else:
            print("Book with that ISBN not found.")
        return False