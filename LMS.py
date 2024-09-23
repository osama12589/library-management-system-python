import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime

# Database connection
conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, year INTEGER, isbn TEXT, issued_to TEXT, issue_date TEXT)''')
conn.commit()

c.execute("SELECT * FROM admin WHERE username=?", ('admin',))
if c.fetchone() is None:
    c.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('admin', 'password'))
    conn.commit()

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    c.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    
    if result:
        admin_panel(result[1])  # result[1] contains the admin username
    else:
        messagebox.showerror("Error", "Invalid Credentials. Please try again.")


def admin_panel(admin_name):
    
    login_window.withdraw()
    
    
    dashboard = tk.Toplevel()
    dashboard.title("Library Management Dashboard")
    
    
    tk.Label(dashboard, text=f"Logged in as: {admin_name}", font=('Helvetica', 12)).pack(pady=10)
    
    
    date_time = tk.Label(dashboard, text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), font=('Helvetica', 12))
    date_time.pack(pady=5)
    
    
    tk.Button(dashboard, text="Add Books", width=20, command=add_books).pack(pady=5)
    tk.Button(dashboard, text="Issue Books", width=20, command=issue_books).pack(pady=5)
    tk.Button(dashboard, text="Edit Books", width=20, command=edit_books).pack(pady=5)
    tk.Button(dashboard, text="Return Books", width=20, command=return_books).pack(pady=5)
    tk.Button(dashboard, text="Delete Books", width=20, command=delete_books).pack(pady=5)
    tk.Button(dashboard, text="Search Books", width=20, command=search_books).pack(pady=5)
    tk.Button(dashboard, text="Show Books", width=20, command=show_books).pack(pady=5)
    tk.Button(dashboard, text="Log Out", width=20, command=lambda: logout(dashboard)).pack(pady=5)

def add_books():
    def save_book():
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()
        isbn = entry_isbn.get()

        c.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)", (title, author, year, isbn))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully")
        add_window.destroy()

    add_window = tk.Toplevel()
    add_window.title("Add Books")
    
    tk.Label(add_window, text="Title:").grid(row=0, column=0, padx=10, pady=10)
    entry_title = tk.Entry(add_window)
    entry_title.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(add_window, text="Author:").grid(row=1, column=0, padx=10, pady=10)
    entry_author = tk.Entry(add_window)
    entry_author.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Label(add_window, text="Year:").grid(row=2, column=0, padx=10, pady=10)
    entry_year = tk.Entry(add_window)
    entry_year.grid(row=2, column=1, padx=10, pady=10)
    
    tk.Label(add_window, text="ISBN:").grid(row=3, column=0, padx=10, pady=10)
    entry_isbn = tk.Entry(add_window)
    entry_isbn.grid(row=3, column=1, padx=10, pady=10)
    
    tk.Button(add_window, text="Save", command=save_book).grid(row=4, column=0, columnspan=2, pady=10)


def issue_books():
    def issue():
        book_id = entry_book_id.get()
        student_name = entry_student_name.get()

        c.execute("SELECT * FROM books WHERE id=? AND issued_to IS NULL", (book_id,))
        book = c.fetchone()

        if book:
            issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
            c.execute("UPDATE books SET issued_to=?, issue_date=? WHERE id=?", (student_name, issue_date, book_id))
            conn.commit()
            messagebox.showinfo("Success", "Book issued successfully")
            issue_window.destroy()
        else:
            messagebox.showerror("Error", "Book not found or already issued")
    
    issue_window = tk.Toplevel()
    issue_window.title("Issue Books")
    
    tk.Label(issue_window, text="Book ID:").grid(row=0, column=0, padx=10, pady=10)
    entry_book_id = tk.Entry(issue_window)
    entry_book_id.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(issue_window, text="Student Name:").grid(row=1, column=0, padx=10, pady=10)
    entry_student_name = tk.Entry(issue_window)
    entry_student_name.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Button(issue_window, text="Issue", command=issue).grid(row=2, column=0, columnspan=2, pady=10)

def edit_books():
    def update_book():
        book_id = entry_book_id.get()
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()
        isbn = entry_isbn.get()

        c.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, book_id))
        conn.commit()
        messagebox.showinfo("Success", "Book updated successfully")
        edit_window.destroy()

    def load_book():
        book_id = entry_book_id.get()
        c.execute("SELECT * FROM books WHERE id=?", (book_id,))
        book = c.fetchone()

        if book:
            entry_title.delete(0, tk.END)
            entry_author.delete(0, tk.END)
            entry_year.delete(0, tk.END)
            entry_isbn.delete(0, tk.END)

            entry_title.insert(0, book[1])
            entry_author.insert(0, book[2])
            entry_year.insert(0, book[3])
            entry_isbn.insert(0, book[4])
        else:
            messagebox.showerror("Error", "Book not found")
    
    edit_window = tk.Toplevel()
    edit_window.title("Edit Books")
    
    tk.Label(edit_window, text="Book ID:").grid(row=0, column=0, padx=10, pady=10)
    entry_book_id = tk.Entry(edit_window)
    entry_book_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(edit_window, text="Load Book", command=load_book).grid(row=0, column=2, padx=10, pady=10)
    
    tk.Label(edit_window, text="Title:").grid(row=1, column=0, padx=10, pady=10)
    entry_title = tk.Entry(edit_window)
    entry_title.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(edit_window, text="Author:").grid(row=2, column=0, padx=10, pady=10)
    entry_author = tk.Entry(edit_window)
    entry_author.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(edit_window, text="Year:").grid(row=3, column=0, padx=10, pady=10)
    entry_year = tk.Entry(edit_window)
    entry_year.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(edit_window, text="ISBN:").grid(row=4, column=0, padx=10, pady=10)
    entry_isbn = tk.Entry(edit_window)
    entry_isbn.grid(row=4, column=1, padx=10, pady=10)
    
    tk.Button(edit_window, text="Update", command=update_book).grid(row=5, column=0, columnspan=3, pady=10)

def return_books():
    def return_book():
        book_id = entry_book_id.get()
        
        c.execute("SELECT * FROM books WHERE id=? AND issued_to IS NOT NULL", (book_id,))
        book = c.fetchone()

        if book:
            c.execute("UPDATE books SET issued_to=NULL, issue_date=NULL WHERE id=?", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Book returned successfully")
            return_window.destroy()
        else:
            messagebox.showerror("Error", "Book not found or not issued")
    
    return_window = tk.Toplevel()
    return_window.title("Return Books")
    
    tk.Label(return_window, text="Book ID:").grid(row=0, column=0, padx=10, pady=10)
    entry_book_id = tk.Entry(return_window)
    entry_book_id.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Button(return_window, text="Return", command=return_book).grid(row=1, column=0, columnspan=2, pady=10)

# Delete Books Function
def delete_books():
    def delete_book():
        book_id = entry_book_id.get()
        
        c.execute("SELECT * FROM books WHERE id=?", (book_id,))
        book = c.fetchone()

        if book:
            c.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Book deleted successfully")
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Book not found")
    
    delete_window = tk.Toplevel()
    delete_window.title("Delete Books")
    
    tk.Label(delete_window, text="Book ID:").grid(row=0, column=0, padx=10, pady=10)
    entry_book_id = tk.Entry(delete_window)
    entry_book_id.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Button(delete_window, text="Delete", command=delete_book).grid(row=1, column=0, columnspan=2, pady=10)

def search_books():
    def search():
        title = entry_title.get()
        author = entry_author.get()

        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")

        if author:
            query += " AND author LIKE ?"
            params.append(f"%{author}%")

        c.execute(query, params)
        results = c.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        for result in results:
            tree.insert('', 'end', values=(result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    search_window = tk.Toplevel()
    search_window.title("Search Books")
    
    tk.Label(search_window, text="Title:").grid(row=0, column=0, padx=10, pady=10)
    entry_title = tk.Entry(search_window)
    entry_title.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(search_window, text="Author:").grid(row=1, column=0, padx=10, pady=10)
    entry_author = tk.Entry(search_window)
    entry_author.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Button(search_window, text="Search", command=search).grid(row=2, column=0, columnspan=2, pady=10)
    
    tree = ttk.Treeview(search_window, columns=("ID", "Title", "Author", "Year", "ISBN", "Issued To", "Issue Date"), show='headings')
    tree.grid(row=3, column=0, columnspan=2)

    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Year", text="Year")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Issued To", text="Issued To")
    tree.heading("Issue Date", text="Issue Date")

def show_books():
    show_window = tk.Toplevel()
    show_window.title("All Books in Library")

    tree = ttk.Treeview(show_window, columns=("ID", "Title", "Author", "Year", "ISBN", "Issued To", "Issue Date"), show='headings')
    tree.pack(padx=10, pady=10)

    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Year", text="Year")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Issued To", text="Issued To")
    tree.heading("Issue Date", text="Issue Date")

    c.execute("SELECT * FROM books")
    rows = c.fetchall()
    
    for row in rows:
        tree.insert('', 'end', values=row)

def logout(dashboard_window):
    dashboard_window.destroy()
    login_window.deiconify()

login_window = tk.Tk()
login_window.title("Library Management System")

tk.Label(login_window, text="Admin Login", font=('Helvetica', 14)).grid(row=0, column=1, pady=10)

tk.Label(login_window, text="Username").grid(row=1, column=0, padx=10, pady=10)
entry_username = tk.Entry(login_window)
entry_username.grid(row=1, column=1, padx=10, pady=10)

tk.Label(login_window, text="Password").grid(row=2, column=0, padx=10, pady=10)
entry_password = tk.Entry(login_window, show="*")
entry_password.grid(row=2, column=1, padx=10, pady=10)

tk.Button(login_window, text="Login", command=login).grid(row=3, column=1, padx=10, pady=10)

login_window.mainloop()

# Close the database connection
conn.close()
