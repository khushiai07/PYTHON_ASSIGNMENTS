# library_manager/book.py

class Book:
    """Represents a single book in the library inventory."""
    def __init__(self, title: str, author: str, isbn: str, status: str = "available"):
        """Initializes a new Book object."""
        self.title = title
        self.author = author
        self.isbn = isbn
        # Status can be 'available' or 'issued' 
        self.status = status

    def __str__(self) -> str:
        """Returns a user-friendly string representation of the Book (magic method)[cite: 23]."""
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {self.status.capitalize()}"

    def to_dict(self) -> dict:
        """Returns a dictionary representation for JSON serialization[cite: 23, 30]."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }
        
    def issue(self) -> bool:
        """Changes the book status to 'issued' if it is available[cite: 24]."""
        if self.is_available():
            self.status = "issued"
            return True
        return False
    
    def return_book(self) -> bool:
        """Changes the book status to 'available' if it is issued[cite: 24]."""
        if not self.is_available():
            self.status = "available"
            return True
        return False

    def is_available(self) -> bool:
        """Checks if the book is currently available[cite: 24]."""
        return self.status == "available"

# Example of how to use this class:
# book1 = Book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "978-0345391803")
# print(book1)
# print(book1.to_dict())