import tkinter as tk            #used for Graphical User Interface                             
from tkinter import ttk         
from PIL import Image, ImageTk   #is a library for opening, manipulating, and saving many different image file formats.

class BookStoreApp(tk.Tk):       #that inherits from tk.Tk. By inheriting from tk.Tk, this class will have all the functionality of a Tkinter main application window.
    def __init__(self):          #constructor method 
        super().__init__()       # calls the constructor of the superclass (tk.Tk in this case) to initialize the main application window.
        self.title("Book Store catalog")

        self.notebook = ttk.Notebook(self)      #create's a tabbed notebook-style interface, where each tab contains a different page or content.
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.book_store_frame = BookStoreFrame(self.notebook)
        self.cart_frame = CartFrame(self.notebook)
        self.search_frame = SearchFrame(self.notebook, self.book_store_frame, self.cart_frame)

        self.notebook.add(self.book_store_frame, text="Catalog")
        self.notebook.add(self.cart_frame, text="Cart")
        self.notebook.add(self.search_frame, text="Search")

class BookStoreFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        
        self.books = [
            {"image_path": "book1.jpg", "title": "1984", "author": "George", "cost": "$10"},
            {"image_path": "book2.jpg", "title": "The catcher in the rye", "author": "salinger", "cost": "$15"},
            {"image_path": "book3.jpg", "title": "castby", "author": "leonardo", "cost": "$20"},
            {"image_path": "book4.jpg", "title": "harry potter", "author": "rowling", "cost": "$25"},
            {"image_path": "book5.jpg", "title": "to kill a mockingbird", "author": "harper lee", "cost": "$30"}
        ]

        self.book_frames = []

        for book in self.books:
            book_frame = BookFrame(self, book["image_path"], book["title"], book["author"], book["cost"])
            book_frame.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
            self.book_frames.append(book_frame)

class BookFrame(ttk.Frame):
    def __init__(self, parent, image_path, title, author, cost):
        super().__init__(parent)

        if image_path:
            try:
                image = Image.open(image_path)
                image = image.resize((50, 50), Image.LANCZOS)  #Image.LANCZOS It is used for image resizing operations.
                book_image = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                book_image = ImageTk.PhotoImage(Image.new("RGB", (50, 50), "gray"))
        else:
            book_image = ImageTk.PhotoImage(Image.new("RGB", (50, 50), "gray"))

        self.image_label = ttk.Label(self, image=book_image)  #Label is a widget used to display text or images on a GUI
        self.image_label.image = book_image
        self.image_label.pack(side=tk.LEFT, padx=5)

        self.title_label = ttk.Label(self, text=title)
        self.title_label.pack(side=tk.LEFT, padx=5)

        self.author_label = ttk.Label(self, text=author)
        self.author_label.pack(side=tk.LEFT, padx=5)

        self.cost_label = ttk.Label(self, text=cost)
        self.cost_label.pack(side=tk.LEFT, padx=5)

        self.add_to_cart_button = ttk.Button(self, text="Add to Cart", command=lambda: self.add_to_cart(title, author, cost))
        self.add_to_cart_button.pack(side=tk.RIGHT, padx=5)

    def add_to_cart(self, title, author, cost):
        parent = self.master.master.master  # Get the top-level BookStoreApp instance
        parent.cart_frame.add_to_cart(title, author, cost)

class CartFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.items = []

        label = tk.Label(self, text="Cart", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

    def add_to_cart(self, title, author, cost):
        item = CartItem(self, title, author, cost)
        item.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
        self.items.append(item)

    def remove_from_cart(self, item):
        item.destroy()
        self.items.remove(item)

class CartItem(ttk.Frame):
    def __init__(self, parent, title, author, cost):
        super().__init__(parent)

        self.title_label = ttk.Label(self, text=title)
        self.title_label.pack(side=tk.LEFT, padx=5)

        self.author_label = ttk.Label(self, text=author)
        self.author_label.pack(side=tk.LEFT, padx=5)

        self.cost_label = ttk.Label(self, text=cost)
        self.cost_label.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(self, text="Remove", command=self.remove_from_cart)
        self.remove_button.pack(side=tk.RIGHT, padx=5)

    def remove_from_cart(self):
        parent = self.master
        parent.remove_from_cart(self)

class SearchFrame(tk.Frame):
    def __init__(self, parent, book_store_frame, cart_frame):
        super().__init__(parent)
        self.book_store_frame = book_store_frame
        self.cart_frame = cart_frame

        self.label = tk.Label(self, text="Search", font=("Helvetica", 18))
        self.label.pack(pady=10, padx=10)

        self.search_entry = tk.Entry(self)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self, text="Search & add", command=self.search_book)
        self.search_button.pack(pady=5)

        self.result_label = tk.Label(self, text="", font=("Helvetica", 12), fg="red")
        self.result_label.pack(pady=10)

    def search_book(self):
        search_text = self.search_entry.get()
        found = False
        for item in self.book_store_frame.books:
            if search_text.lower() in item["title"].lower():
                author = item["author"]
                cost = item["cost"]
                self.cart_frame.add_to_cart(item["title"], author, cost)
                found = True
                break
        if found:
            self.result_label.config(text="Book added to cart.", fg="green")
        else:
            self.result_label.config(text="Book not found.", fg="red")


if __name__ == "__main__":
    app = BookStoreApp()
    app.mainloop()
