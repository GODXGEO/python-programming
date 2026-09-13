import tkinter as tk
a=tk.Tk()
a.title("Python project learning")
label=tk.Label(a,text="Hello user")
label.place(x=110, y=40)
button=tk.Button(a, text="Click me", command= lambda: label.config(text="You clicked the button"))
button.place(x=200,y=180)
a.mainloop()
