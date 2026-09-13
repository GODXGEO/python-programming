import mysql.connector as mc
import tkinter as tk
from tkinter import messagebox, simpledialog

co = mc.connect(passwd='1234', host='localhost', user='root')
cu = co.cursor()

cu.execute('CREATE DATABASE IF NOT EXISTS PROJECT;')
cu.execute('USE PROJECT;')

cu.execute('CREATE TABLE IF NOT EXISTS STUDENTS (SID INT PRIMARY KEY AUTO_INCREMENT, NAME VARCHAR(20) NOT NULL, CLASS VARCHAR(4));')

cu.execute("""CREATE TABLE IF NOT EXISTS BOOKS(
BID INT PRIMARY KEY AUTO_INCREMENT,
TITLE VARCHAR(20) NOT NULL,
AUTHOR VARCHAR(20) NOT NULL,
QUANTITY INT NOT NULL
);""")

cu.execute("""CREATE TABLE IF NOT EXISTS ISSUED_BOOKS(
ISID INT PRIMARY KEY AUTO_INCREMENT,
SID INT,
BID INT,
ISDATE DATE NOT NULL,
RDATE DATE
);""")

co.commit()

root = tk.Tk()
root.title("Library Management System")
root.geometry("700x600")


def add_book():
    title = simpledialog.askstring("Add Book", "Enter the title:")
    if title is None:
        return

    author = simpledialog.askstring("Add Book", "Enter the author:")
    if author is None:
        return

    quantity = simpledialog.askinteger("Add Book", "Enter the quantity:")
    if quantity is None:
        return

    e = 'INSERT INTO BOOKS (TITLE,AUTHOR,QUANTITY) VALUES(%s,%s,%s);'
    f = (title, author, quantity)

    cu.execute(e, f)
    co.commit()

    messagebox.showinfo("Success", "Book added successfully!")


def view_books():
    cu.execute('SELECT * FROM BOOKS;')
    books = cu.fetchall()

    result = ""

    if not books:
        result = "No books found."
    else:
        for book in books:
            result += "Book ID: " + str(book[0]) + "\n"
            result += "Title: " + str(book[1]) + "\n"
            result += "Author: " + str(book[2]) + "\n"
            result += "Quantity: " + str(book[3]) + "\n"
            result += "--------------------------------\n"

    messagebox.showinfo("All Books", result)


def search_book():
    title = simpledialog.askstring("Search Book", "Enter the book's name:")

    if title is None:
        return

    cu.execute('SELECT * FROM BOOKS WHERE TITLE=%s;', (title,))
    book = cu.fetchone()

    if book:
        result = f"""
Book ID: {book[0]}
Title: {book[1]}
Author: {book[2]}
Quantity: {book[3]}
"""
        messagebox.showinfo("Book Found", result)
    else:
        messagebox.showinfo("Search", "Book not found!")


def update_book():
    title = simpledialog.askstring(
        "Update Book",
        "Enter the title of the book you wish to update:"
    )

    if title is None:
        return

    cu.execute('SELECT TITLE FROM BOOKS;')
    books = cu.fetchall()

    book_names = []

    for i in range(len(books)):
        book_names.append(books[i][0].lower())

    if title.lower() in book_names:

        choice = simpledialog.askinteger(
            "Update Book",
            "PRESS 1 TO UPDATE TITLE\n"
            "PRESS 2 TO UPDATE AUTHOR\n"
            "PRESS 3 TO UPDATE QUANTITY\n\n"
            "What do you wish to update?"
        )

        if choice == 1:
            new_title = simpledialog.askstring(
                "Update Title",
                "Enter new title:"
            )

            if new_title:
                cu.execute(
                    'UPDATE BOOKS SET TITLE=%s WHERE TITLE=%s;',
                    (new_title, title)
                )
                co.commit()
                messagebox.showinfo("Success", "Title updated successfully!")

        elif choice == 2:
            new_author = simpledialog.askstring(
                "Update Author",
                "Enter new author:"
            )

            if new_author:
                cu.execute(
                    'UPDATE BOOKS SET AUTHOR=%s WHERE TITLE=%s;',
                    (new_author, title)
                )
                co.commit()
                messagebox.showinfo("Success", "Author updated successfully!")

        elif choice == 3:
            new_quantity = simpledialog.askinteger(
                "Update Quantity",
                "Enter the new quantity:"
            )

            if new_quantity is not None:
                cu.execute(
                    'UPDATE BOOKS SET QUANTITY=%s WHERE TITLE=%s;',
                    (new_quantity, title)
                )
                co.commit()
                messagebox.showinfo("Success", "Quantity updated successfully!")

    else:
        messagebox.showinfo("Update Book", "Book not found.")


def delete_book():
    title = simpledialog.askstring(
        "Delete Book",
        "Enter the title of the book you wish to delete:"
    )

    if title is None:
        return

    cu.execute('SELECT TITLE FROM BOOKS;')
    books = cu.fetchall()

    book_names = []

    for i in range(len(books)):
        book_names.append(books[i][0].lower())

    if title.lower() in book_names:
        cu.execute(
            'DELETE FROM BOOKS WHERE TITLE=%s;',
            (title,)
        )
        co.commit()

        messagebox.showinfo("Delete Book", "Done!")

    else:
        messagebox.showinfo("Delete Book", "Book not found.")


def add_student():
    name = simpledialog.askstring(
        "Add Student",
        "Enter the student's name:"
    )

    if name is None:
        return

    student_class = simpledialog.askstring(
        "Add Student",
        "Enter the student's class:"
    )

    if student_class is None:
        return

    cu.execute(
        'INSERT INTO STUDENTS (NAME,CLASS) VALUES(%s,%s);',
        (name, student_class)
    )

    co.commit()

    messagebox.showinfo("Success", "Student added successfully!")


def view_students():
    cu.execute('SELECT * FROM STUDENTS;')
    students = cu.fetchall()

    result = ""

    if not students:
        result = "No students found."
    else:
        for student in students:
            result += "Student ID: " + str(student[0]) + "\n"
            result += "Name: " + str(student[1]) + "\n"
            result += "Class: " + str(student[2]) + "\n"
            result += "--------------------------------\n"

    messagebox.showinfo("All Students", result)


def search_student():
    name = simpledialog.askstring(
        "Search Student",
        "Enter the student's name you wish to view:"
    )

    if name is None:
        return

    cu.execute(
        'SELECT * FROM STUDENTS WHERE NAME=%s;',
        (name,)
    )

    student = cu.fetchall()

    if student:
        result = ""

        for s in student:
            result += "Student ID: " + str(s[0]) + "\n"
            result += "Name: " + str(s[1]) + "\n"
            result += "Class: " + str(s[2]) + "\n"
            result += "--------------------------------\n"

        messagebox.showinfo("Student Found", result)

    else:
        messagebox.showinfo(
            "Search Student",
            "Student does not exist!"
        )


def borrow_book():
    book_name = simpledialog.askstring(
        "Borrow Book",
        "Enter the name of the book you wish to borrow:"
    )

    if book_name is None:
        return

    cu.execute(
        "SELECT BID, QUANTITY FROM BOOKS WHERE TITLE=%s",
        (book_name,)
    )

    book = cu.fetchone()

    if book is None:
        messagebox.showinfo("Borrow Book", "Book not found.")
        return

    book_id = book[0]
    quantity = book[1]

    if quantity <= 0:
        messagebox.showinfo(
            "Borrow Book",
            "Sorry, this book is currently unavailable."
        )
        return

    student_name = simpledialog.askstring(
        "Borrow Book",
        "Enter your name:"
    )

    if student_name is None:
        return

    cu.execute(
        "SELECT SID FROM STUDENTS WHERE NAME=%s",
        (student_name,)
    )

    student = cu.fetchone()

    if student is None:
        messagebox.showinfo(
            "Borrow Book",
            "Student not found."
        )
        return

    student_id = student[0]

    cu.execute("""
        INSERT INTO ISSUED_BOOKS
        (BID, SID, ISDATE)
        VALUES (%s, %s, CURDATE())
    """, (book_id, student_id))

    cu.execute(
        "UPDATE BOOKS SET QUANTITY=QUANTITY-1 WHERE BID=%s",
        (book_id,)
    )

    co.commit()

    messagebox.showinfo(
        "Borrow Book",
        "Book borrowed successfully!"
    )


def return_book():
    student_name = simpledialog.askstring(
        "Return Book",
        "Enter your name:"
    )

    if student_name is None:
        return

    book_name = simpledialog.askstring(
        "Return Book",
        "Enter the book name:"
    )

    if book_name is None:
        return

    cu.execute(
        "SELECT SID FROM STUDENTS WHERE NAME=%s",
        (student_name,)
    )

    student = cu.fetchone()

    if student is None:
        messagebox.showinfo(
            "Return Book",
            "Student not found."
        )
        return

    student_id = student[0]

    cu.execute(
        "SELECT BID FROM BOOKS WHERE TITLE=%s",
        (book_name,)
    )

    book = cu.fetchone()

    if book is None:
        messagebox.showinfo(
            "Return Book",
            "Book not found."
        )
        return

    book_id = book[0]

    cu.execute("""
        SELECT ISID
        FROM ISSUED_BOOKS
        WHERE SID=%s AND BID=%s AND RDATE IS NULL
    """, (student_id, book_id))

    issued = cu.fetchone()

    if issued is None:
        messagebox.showinfo(
            "Return Book",
            "This book is not currently issued to this student."
        )
        return

    issued_id = issued[0]

    cu.execute(
        "UPDATE ISSUED_BOOKS SET RDATE=CURDATE() WHERE ISID=%s",
        (issued_id,)
    )

    cu.execute(
        "UPDATE BOOKS SET QUANTITY=QUANTITY+1 WHERE BID=%s",
        (book_id,)
    )

    co.commit()

    messagebox.showinfo(
        "Return Book",
        "Book returned successfully!"
    )


def view_issued_books():
    cu.execute("""
        SELECT
        ISSUED_BOOKS.ISID,
        STUDENTS.NAME,
        BOOKS.TITLE,
        ISSUED_BOOKS.ISDATE,
        ISSUED_BOOKS.RDATE
        FROM ISSUED_BOOKS
        JOIN STUDENTS ON ISSUED_BOOKS.SID = STUDENTS.SID
        JOIN BOOKS ON ISSUED_BOOKS.BID = BOOKS.BID
    """)

    issued_books = cu.fetchall()

    result = ""

    if not issued_books:
        result = "No issued books found."
    else:
        for book in issued_books:
            result += "Issue ID: " + str(book[0]) + "\n"
            result += "Student: " + str(book[1]) + "\n"
            result += "Book: " + str(book[2]) + "\n"
            result += "Issue Date: " + str(book[3]) + "\n"
            result += "Return Date: " + str(book[4]) + "\n"
            result += "--------------------------------\n"

    messagebox.showinfo(
        "Issued Books",
        result
    )


def exit_application():
    co.close()
    root.destroy()


title = tk.Label(
    root,
    text="LIBRARY MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold")
)

title.pack(pady=20)

books_label = tk.Label(
    root,
    text="BOOKS",
    font=("Arial", 16, "bold")
)

books_label.pack()

tk.Button(
    root,
    text="1. Add Book",
    width=30,
    command=add_book
).pack(pady=3)

tk.Button(
    root,
    text="2. View All Books",
    width=30,
    command=view_books
).pack(pady=3)

tk.Button(
    root,
    text="3. Search Book",
    width=30,
    command=search_book
).pack(pady=3)

tk.Button(
    root,
    text="4. Update Book",
    width=30,
    command=update_book
).pack(pady=3)

tk.Button(
    root,
    text="5. Delete Book",
    width=30,
    command=delete_book
).pack(pady=3)

students_label = tk.Label(
    root,
    text="STUDENTS",
    font=("Arial", 16, "bold")
)

students_label.pack(pady=(15, 0))

tk.Button(
    root,
    text="6. Add Student",
    width=30,
    command=add_student
).pack(pady=3)

tk.Button(
    root,
    text="7. View All Students",
    width=30,
    command=view_students
).pack(pady=3)

tk.Button(
    root,
    text="8. Search Student",
    width=30,
    command=search_student
).pack(pady=3)

borrow_label = tk.Label(
    root,
    text="BORROW / RETURN",
    font=("Arial", 16, "bold")
)

borrow_label.pack(pady=(15, 0))

tk.Button(
    root,
    text="9. Borrow Book",
    width=30,
    command=borrow_book
).pack(pady=3)

tk.Button(
    root,
    text="10. Return Book",
    width=30,
    command=return_book
).pack(pady=3)

tk.Button(
    root,
    text="11. View Issued Books",
    width=30,
    command=view_issued_books
).pack(pady=3)

tk.Button(
    root,
    text="12. Exit",
    width=30,
    command=exit_application
).pack(pady=15)

root.mainloop()
