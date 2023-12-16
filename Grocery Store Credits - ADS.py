from asyncio.windows_events import NULL
from tkinter import *
from tkinter import ttk
from turtle import width
from pymongo import MongoClient
from PIL import ImageTk, Image

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
GroceryCollection = db["Grocery Store"]

class Node:
  def __init__(self, name, ph, address, total, credit = 0):
    self.name = name
    self.phone = ph
    self.address = address
    self.total = total
    self.credit = credit
    self.parent = None
    self.left = None
    self.right = None

class SplayTree:
  def __init__(self):
    self.root = None

  def maximum(self, x):
    while x.right != None:
      x = x.right
    return x
    
  def left_rotate(self, x):
    y = x.right
    x.right = y.left
    if y.left != None:
      y.left.parent = x
    
    y.parent = x.parent
    if x.parent == None: # x is root
      self.root = y
    
    elif x == x.parent.left: # x is left child
      x.parent.left = y
    
    else: # x is right child
      x.parent.right = y
    
    y.left = x
    x.parent = y
    
  def right_rotate(self, x):
    y = x.left
    x.left = y.right
    if y.right != None:
      y.right.parent = x
    
    y.parent = x.parent
    if x.parent == None: #x is root
      self.root = y
    
    elif x == x.parent.right: #x is right child
      x.parent.right = y
    
    else: #x is left child
      x.parent.left = y
    
    y.right = x
    x.parent = y
    
  def splay(self, n):
    n.credit += 1
    while n.parent != None: # node is not root
      if n.parent == self.root: # node is child of root, one rotation
        if n == n.parent.left:
          self.right_rotate(n.parent)
        else:
          self.left_rotate(n.parent)
    
      else:
        p = n.parent
        g = p.parent # grandparent
    
        if n.parent.left == n and p.parent.left == p: # both are left children
          self.right_rotate(g)
          self.right_rotate(p)
    
        elif n.parent.right == n and p.parent.right == p: # both are right children
          self.left_rotate(g)
          self.left_rotate(p)
    
        elif n.parent.right == n and p.parent.left == p:
          self.left_rotate(p)
          self.right_rotate(g)
    
        elif n.parent.left == n and p.parent.right == p:
          self.right_rotate(p)
          self.left_rotate(g)
    
  def insert(self, n):
    y = None
    temp = self.root
    while temp != None:
      y = temp
      if n.name < temp.name:
        temp = temp.left
      else:
        temp = temp.right
    
    n.parent = y
    
    if y == None: # newly added node is root
      self.root = n
    elif n.name < y.name:
      y.left = n
    else:
      y.right = n
    
    self.splay(n)
    
  def search(self, n, custPhone):
    if n != None:
      if custPhone == n.phone:
        self.splay(n)
        return n
      
      elif custPhone < n.phone:
        return self.search(n.left, custPhone)
      elif custPhone > n.phone:
        return self.search(n.right, custPhone)
      else:
        return None
    
  def delete(self, n):
    self.splay(n)
    
    left_subtree = SplayTree()
    left_subtree.root = self.root.left
    if left_subtree.root != None:
      left_subtree.root.parent = None
    
    right_subtree = SplayTree()
    right_subtree.root = self.root.right
    if right_subtree.root != None:
      right_subtree.root.parent = None
    
    if left_subtree.root != None:
      m = left_subtree.maximum(left_subtree.root)
      left_subtree.splay(m)
      left_subtree.root.right = right_subtree.root
      self.root = left_subtree.root
    
    else:
      self.root = right_subtree.root
    
  def inorder(self, n):
    if n != None:
      self.inorder(n.left)
      print("----------")
      print(n.name)
      print(n.phone)
      print(n.address)
      self.inorder(n.right)

name = []
address = []
phone = []
total = []
listOfCustomers = []

# To display a message that the person has received a cashback
def giveCredit(node):
  if (node.credit >= 10):
    top3 = Tk()
    top3.title("GROCERY STORE")
    top3.iconbitmap("C:/Users/91978/Desktop/psg logo.png")
    top3.geometry("1200x800")

    # Define image
    background = ImageTk.PhotoImage(file="C:\\Users\\91978\\Desktop\\GROCERY STORE CREDITS\\Images\\Congratulations.png")

    # Create label
    background_label = Label(root, image=background)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
  else:
    return

# To create another window displaying the customers
def displayCustomers():
  data = listOfCustomers
  top = Toplevel()
  top.geometry("1600x900")
  top.title("CUSTOMERS")

  style = ttk.Style()

  style.theme_use('default')
  style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=80, fieldbackground="#D3D3D3")
  
  # Change selected color
  style.map('Treeview', background=[('selected', "#347083")])

  # Create a Treeview frame
  tree_frame = Frame(top)
  tree_frame.pack(pady=10)

  # Create a Treeview scrollbar
  tree_scroll = Scrollbar(tree_frame)
  tree_scroll.pack(side=RIGHT, fill=Y)

  # Create the Treeview
  my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
  my_tree.pack()

  # Configure the Scrollbar
  tree_scroll.config(command=my_tree.yview)

  # Define the columns
  my_tree['columns'] = ("Name", "Phone", "Address", "Total amount spent", "Frequency of visit")
  my_tree.column("#0", width=0, stretch=NO)
  my_tree.column("Name", anchor=W, width=200)
  my_tree.column("Phone", anchor=W, width=140)
  my_tree.column("Address", anchor=CENTER, width=300)
  my_tree.column("Total amount spent", anchor=CENTER, width=140)
  my_tree.column("Frequency of visit", anchor=CENTER, width=140)

  my_tree.heading("#0", text="", anchor=W)
  my_tree.heading("Name", text="Name", anchor=W)
  my_tree.heading("Phone", text="Phone", anchor=W)
  my_tree.heading("Address", text="Address", anchor=CENTER)
  my_tree.heading("Total amount spent", text="Total amount spent", anchor=CENTER)
  my_tree.heading("Frequency of visit", text="Frequency of visit", anchor=CENTER)
  
  # To change the colors of odd and even rows
  my_tree.tag_configure('oddrow', background="white")
  my_tree.tag_configure('evenrow', background="lightblue")

  global count
  count = 0

  for record in listOfCustomers:
    if count % 2 == 0:
      my_tree.insert(parent='', index='end', iid=count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
    else:
      my_tree.insert(parent='', index='end', iid=count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))
    count += 1

  button_frame = LabelFrame(top, text = "---")
  button_frame.pack(fill="x", expand = "yes", padx=20)
  button_quit = Button(button_frame, text="Exit", command=top.destroy, bg="black")
  button_quit.pack()
  
def getCustomers():
  win = Toplevel()
  # Define image
  background = ImageTk.PhotoImage(file="C:\\Users\\91978\\Downloads\\Grocery_main_page.png")
  win.geometry("1600x900")
  def get_content():
    groceryTree = SplayTree()
    groceryTree.insert(Node(str(eName.get()), str(ePh.get()), str(eAdd.get()), str(eAmt.get())))
    post = {"Name" : str(eName.get()), "PhoneNumber" : str(ePh.get()), "Address" : str(eAdd.get()), "Total(Rs)" : str(eAmt.get())}
    GroceryCollection.insert_one(post)
    eName.delete(0, END)
    ePh.delete(0, END)
    eAdd.delete(0, END)
    eAmt.delete(0, END)

    # Create label
  background_label = Label(win, image=background)
  background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Creating a frame
  frame = Frame(win, padx=1, pady=1, bg='orange', width=500, height=500)
  frame.place(relx=0.5, rely=0.5, anchor=CENTER)

  name_entry = Label(frame, text="Enter the customer name : ", bg='orange', fg='darkgreen')
  eName = Entry(frame, width=50)

  ph_entry = Label(frame, text="Enter the phone number : ", bg='orange', fg='darkgreen')
  ePh = Entry(frame, width=50)

  add_entry = Label(frame, text="Enter the address : ", bg='orange', fg='darkgreen')
  eAdd = Entry(frame, width=50)

  amt_entry = Label(frame, text="Enter the purchase amount : Rs. ", bg='orange', fg='darkgreen')
  eAmt = Entry(frame, width=50)

  name_entry.grid(row=0, column=0)
  eName.grid(row=0, column=2)
  ph_entry.grid(row=4, column=0)
  ePh.grid(row=4, column=2)
  add_entry.grid(row=8, column=0)
  eAdd.grid(row=8, column=2)
  amt_entry.grid(row=12, column=0)
  eAmt.grid(row=12, column=2)

  name.append(eName.get())
  address.append(eAdd.get())
  phone.append(ePh.get())
  total.append(eAmt.get())

  enter = ttk.Button(frame, text= "Enter", command= get_content, width=10).grid(row=16, column=8)

def changeTotal():
  data = listOfCustomers
  top2 = Toplevel()
  top2.geometry("1600x900")
  top2.title("CUSTOMERS")

  style = ttk.Style()

  style.theme_use('default')
  style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=60, fieldbackground="#D3D3D3")
  
  # Change selected color
  style.map('Treeview', background=[('selected', "#347083")])

  # Create a Treeview frame
  tree_frame = Frame(top2)
  tree_frame.pack(pady=10)

  # Create a Treeview scrollbar
  tree_scroll = Scrollbar(tree_frame)
  tree_scroll.pack(side=RIGHT, fill=Y)

  # Create the Treeview
  my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
  my_tree.pack()

  # Configure the Scrollbar
  tree_scroll.config(command=my_tree.yview)

  # Define the columns
  my_tree['columns'] = ("Name", "Phone", "Address", "Total amount spent", "Frequency of visit")
  my_tree.column("#0", width=0, stretch=NO)
  my_tree.column("Name", anchor=W, width=200)
  my_tree.column("Phone", anchor=W, width=140)
  my_tree.column("Address", anchor=CENTER, width=300)
  my_tree.column("Total amount spent", anchor=CENTER, width=140)
  my_tree.column("Frequency of visit", anchor=CENTER, width=140)

  my_tree.heading("#0", text="", anchor=W)
  my_tree.heading("Name", text="Name", anchor=W)
  my_tree.heading("Phone", text="Phone", anchor=W)
  my_tree.heading("Address", text="Address", anchor=CENTER)
  my_tree.heading("Total amount spent", text="Total amount spent", anchor=CENTER)
  my_tree.heading("Frequency of visit", text="Frequency of visit", anchor=CENTER)
  
  # To change the colors of odd and even rows
  my_tree.tag_configure('oddrow', background="white")
  my_tree.tag_configure('evenrow', background="lightblue")

  global count
  count = 0

  for record in listOfCustomers:
    if count % 2 == 0:
      my_tree.insert(parent='', index='end', iid=count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('evenrow',))
    else:
      my_tree.insert(parent='', index='end', iid=count, text = '', values = (record[0], record[1], record[2], record[3]), tags = ('oddrow',))
    count += 1

  # Add record entry boxes
  data_frame = LabelFrame(top2, text="Record")
  data_frame.pack(fill="x", expand="yes", padx=20)

  fn_label = Label(data_frame, text="Name")
  fn_label.grid(row=0, column=0, padx=10, pady=10)
  fn_entry = Entry(data_frame)
  fn_entry.grid(row=0, column=1, padx=10, pady=10)

  ph_label = Label(data_frame, text="Phone")
  ph_label.grid(row=0, column=2, padx=10, pady=10)
  ph_entry = Entry(data_frame)
  ph_entry.grid(row=0, column=3, padx=10, pady=10)

  add_label = Label(data_frame, text="Address")
  add_label.grid(row=0, column=4, padx=10, pady=10)
  add_entry = Entry(data_frame)
  add_entry.grid(row=0, column=5, padx=10, pady=10)

  total_label = Label(data_frame, text="Total")
  total_label.grid(row=0, column=6, padx=10, pady=10)
  total_entry = Entry(data_frame)
  total_entry.grid(row=0, column=7, padx=10, pady=10)

  # Clear Entry boxes
  def clear_record():
    # Clear Entry boxes
    fn_entry.delete(0, END)
    ph_entry.delete(0, END)
    add_entry.delete(0, END)
    total_entry.delete(0, END) 

  # Select Record
  def select_record(e):
    # Clear Entry boxes
    fn_entry.delete(0, END)
    ph_entry.delete(0, END)
    add_entry.delete(0, END)
    total_entry.delete(0, END)

    # Grab record number
    selected = my_tree.focus()
    # Grab record values
    values = my_tree.item(selected, 'values')

    # Ouput Entry boxes
    fn_entry.insert(0, values[0])
    ph_entry.insert(0, values[1])
    add_entry.insert(0, values[2])
    total_entry.insert(0, values[3])

  # Update Record
  def update_record():
    # Grab the record number
    selected = my_tree.focus()
    # Update Record
    my_tree.item(selected, text="", values=(fn_entry.get(), ph_entry.get(), add_entry.get(), total_entry.get(),))

    # Clear Entry boxes
    fn_entry.delete(0, END)
    ph_entry.delete(0, END)
    add_entry.delete(0, END)
    total_entry.delete(0, END)

    giveCredit(total_entry)

  # Add Buttons
  button_frame = LabelFrame(top2, text="Commands")
  button_frame.pack(fill="x", expand="yes", padx=20)

  update = Button(button_frame, text="Update", command=update_record)
  update.grid(row=0, column=0, padx=10, pady=10) 

  selectRecord = Button(button_frame, text="Clear Entry", command=clear_record)
  selectRecord.grid(row=0, column=1, padx=10, pady=10)  
  
  exit = Button(button_frame, text="Exit", command=top2.destroy)
  exit.grid(row=0, column=2, padx=10, pady=10)  

  my_tree.bind("<ButtonRelease-1>", select_record)  


if __name__ == '__main__':
  groceryTree = SplayTree()
    
  allCustomers = []  
  CustomerNames = GroceryCollection.distinct("Name")   

  for i in range(len(CustomerNames)):
    result = GroceryCollection.find({"Name":CustomerNames[i]})
    allCustomers.append(list(result))
    
  def getGroceryData(grocery):
    for i in range(len(grocery)):
      name.append(grocery[i]['Name']) 
      total.append(grocery[i]['Total(Rs)'])
      address.append(grocery[i]['Address'])
      phone.append(grocery[i]['PhoneNumber'])
    return  

  for i in range(len(allCustomers)):
    getGroceryData(allCustomers[i])
  for i in range(len(allCustomers)):
    newNode = Node(name[i], phone[i], address[i], total[i])
    groceryTree.insert(newNode)

  groceryTree.inorder(groceryTree.root)

  for i in range(len(name)):
    listOfCustomers.append([name[i], phone[i], address[i], total[i]])

  root = Tk()
  root.title("GROCERY STORE")
  root.iconbitmap("C:/Users/91978/Desktop/psg logo.png")
  root.geometry("1200x800")

# Define image
background = ImageTk.PhotoImage(file="C:\\Users\\91978\\Downloads\\Grocery_main_page.png")

# Create label
background_label = Label(root, image=background)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Creating a frame
frame = LabelFrame(root, text="Select from the following menu", padx=1, pady=1)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Creating buttons
myButton1 = Button(frame, text = "Display Customers", padx=50, pady=10, command=lambda : displayCustomers(), fg = 'white', bg = 'black', width=50)
myButton2 = Button(frame, text = "Add a Customer", padx=50, pady=10, command=lambda : getCustomers(), fg = 'white', bg = 'black', width=50)
myButton3 = Button(frame, text = "Change Total", padx=50, pady=10, command=lambda : changeTotal(), fg = 'white', bg = 'black', width=50)

button_quit = Button(frame, text="Exit", command=root.destroy, bg="red")

myButton1.pack()
myButton2.pack()
myButton3.pack()
button_quit.pack()

root.attributes('-fullscreen', True)

root.mainloop()