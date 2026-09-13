import mysql.connector as mc
co=mc.connect(passwd='1234',host='localhost',user='root')
cu=co.cursor()
cu.execute('CREATE DATABASE IF NOT EXISTS PROJECT;')
cu.execute('USE PROJECT;')
cu.execute('CREATE TABLE IF NOT EXISTS STUDENTS (SID INT PRIMARY KEY AUTO_INCREMENT, NAME VARCHAR(20) NOT NULL, CLASS VARCHAR(4));')
cu.execute("""CREATE TABLE IF NOT EXISTS BOOKS(BID INT PRIMARY KEY AUTO_INCREMENT,TITLE VARCHAR(20) NOT NULL,
AUTHOR VARCHAR(20) NOT NULL, QUANTITY INT NOT NULL);""")
cu.execute('CREATE TABLE IF NOT EXISTS ISSUED_BOOKS(ISID INT PRIMARY KEY AUTO_INCREMENT, SID INT,BID INT,ISDATE DATE NOT NULL,RDATE DATE);')
zx=1
while zx==1:
    print("""========================================
   LIBRARY MANAGEMENT SYSTEM
========================================

          BOOKS
----------------------------------------
1. Add Book
2. View All Books
3. Search Book
4. Update Book
5. Delete Book

        STUDENTS
----------------------------------------
6. Add Student
7. View All Students
8. Search Student

      BORROW / RETURN
----------------------------------------
9. Borrow Book
10. Return Book
11. View Issued Books

----------------------------------------
12. Exit
========================================""")
    a=int(input("Enter your choice:"))
    def books():
        if a==1:
            c=input("Enter the title:")
            d=input("Enter the author:")
            quantity=int(input("Enter the quantity:"))
            e='INSERT INTO BOOKS (TITLE,AUTHOR,QUANTITY) VALUES(%s,%s,%s);'
            f=(c,d,quantity)
            cu.execute(e,f)
        co.commit()
        if a==2:
            cu.execute('select TITLE from books;')
            g=cu.fetchall()
            print(g)
        if a==3:
            h=input("Enter the book's name:")
            cu.execute('SELECT * FROM BOOKS WHERE TITLE=%s;',(h,))
            i=cu.fetchone()
            if i:
                print(f"""
                Book ID:{i[0]}
                Title:{i[1]}
                Author:{i[2]}
                Quantity:{i[3]}""")
            else:
                print("Book not found!")
        if a==4:
            j=input("Enter the title of the book you wish to update:")
            cu.execute('SELECT TITLE FROM BOOKS;')
            o=cu.fetchall()
            p=[]
            for i in range(len(o)):
                p.append(o[i][0].lower())
            if j.lower() in p:
                print("""
                PRESS 1 TO UPDATE TITLE
                PRESS 2 TO UPDATE AUTHOR
                PRESS 3 TO UPDATE QUANTITY
                """)
                k=int(input("What do you wish to update?:"))
                if k==1:
                    l=input("Enter new title:")
                    cu.execute(f"UPDATE BOOKS SET TITLE=%s WHERE TITLE=%s;",(l,j))
                if k==2:
                    m=input("Enter new author:")
                    cu.execute(f"UPDATE BOOKS SET AUTHOR=%s WHERE TITLE=%s;",(m,j))
                if k==3:
                    n=int(input("Enter the new quantity:"))
                    cu.execute(f'UPDATE BOOKS SET QUANTITY=%s WHERE TITLE=%s;',(n,j))
                co.commit()
            else:
                print("Book not found.")
        if a==5:
            s=[]
            q=input("Enter the title of the book you wish to delete:")
            cu.execute('SELECT TITLE FROM BOOKS;')
            r=cu.fetchall()
            for i in range(len(r)):
                s.append(r[i][0].lower())
            if q.lower() in s:
                cu.execute('DELETE FROM BOOKS WHERE TITLE=%s;',(q,))
                co.commit()
                print("Done!")
            else:
                print("Book not found.")
    def students():
        if a==6:
            u=input("Enter the student's name:")
            v=input("Enter the student's class:")
            cu.execute('INSERT INTO STUDENTS (NAME,CLASS) VALUES(%s,%s);',(u,v))
            co.commit()
            print("Done!")
        if a==7:
            cu.execute('SELECT NAME FROM STUDENTS;')
            print(cu.fetchall())
        if a==8:
            w=input("Enter the student's name you wish to view:")
            cu.execute('SELECT * FROM STUDENTS WHERE NAME=%s;',(w,))
            x=cu.fetchall()
            if x:
                print(x)
            else:
                print("Student does not exist!")
    def issue():
        if a==9:
            y=input("Enter the name of the book you wish to borrow: ")
            cu.execute("SELECT BID, QUANTITY FROM BOOKS WHERE TITLE=%s",(y,))
            book=cu.fetchone()
            if book is None:
                print("Book not found.")
            else:
                book_id = book[0]
                quantity = book[1]
                if quantity<=0:
                    print("Sorry, this book is currently unavailable.")
                else:
                    z=input("Enter your name:")
                    cu.execute("SELECT SID FROM STUDENTS WHERE NAME=%s",(z,))
                    student = cu.fetchone()
                    if student is None:
                        print("Student not found.")
                    else:
                        student_id = student[0]
                        cu.execute("""
                            INSERT INTO ISSUED_BOOKS
                            (BID, SID, ISDATE)
                            VALUES (%s, %s, CURDATE())
                        """, (book_id, student_id))
                        cu.execute("UPDATE BOOKS SET QUANTITY=QUANTITY-1 WHERE BID=%s",(book_id,))
                        co.commit()
                        print("Book borrowed successfully!")
        if a==10:
            aa=input("Enter your name:")
            cu.execute("SELECT SID FROM STUDENTS WHERE NAME=%s",(aa,))
            bb=cu.fetchone()
            if bb is None:
                print("Student not found.")
            else:
                cc=bb[0]
                dd=input("Enter the name of the book you wish to return:")
                cu.execute("SELECT BID FROM BOOKS WHERE TITLE=%s",(dd,))
                ee=cu.fetchone()
                if ee is None:
                    print("Book not found.")
                else:
                    ff=ee[0]
                    cu.execute("SELECT ISID FROM ISSUED_BOOKS WHERE SID=%s AND BID=%s AND RDATE IS NULL",(cc,ff))
                    gg=cu.fetchone()
                    if gg is None:
                        print("No record found of you borrowing this book.")
                    else:
                        hh=gg[0]
                        cu.execute("UPDATE ISSUED_BOOKS SET RDATE=CURDATE() WHERE ISID=%s",(hh,))
                        cu.execute("UPDATE BOOKS SET QUANTITY=QUANTITY+1 WHERE BID=%s",(ff,))
                        co.commit()
                        print("Book returned successfully!")
        if a==11:
            cu.execute("""SELECT STUDENTS.NAME, BOOKS.TITLE, ISSUED_BOOKS.ISDATE, ISSUED_BOOKS.RDATE
                          FROM ISSUED_BOOKS
                          JOIN STUDENTS ON ISSUED_BOOKS.SID=STUDENTS.SID
                          JOIN BOOKS ON ISSUED_BOOKS.BID=BOOKS.BID;""")
            ii=cu.fetchall()
            print(ii)
    students()            
    books()
    issue()
    if a==12:
        zx=0
        print("Thank you for using this application!")
    else:
        zz=input('Do you wish to continue?(y/n):')    
        if zz in 'Yy':
            zx=1
        else:
            zx=0
            print("Thank you for using this application!")
