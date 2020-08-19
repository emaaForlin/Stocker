from tkinter import ttk
from tkinter import *
import sqlite3


class Product:

	dbname = 'database.db'
	def __init__(self, window):
		self.wind = window
		self.wind.title('Products App')

		#Create a frame container
		frame = LabelFrame(self.wind, text='Resgiter a new Product')
		frame.grid(row=0, column=0 ,columnspan=3, pady=20)

		#Name input
		Label(frame, text='Name: ').grid(row=1, column=0)
		self.name = Entry(frame)
		self.name.focus()
		self.name.grid(row=1, column=1)

		#Price input
		Label(frame, text='Price: ').grid(row=2, column= 0)
		self.price = Entry(frame)
		self.price.grid(row=2, column=1)

		#Button save
		ttk.Button(frame, text='Save product', command=self.add_product).grid(row=3, columnspan=2, sticky=W+E)

		#Output messages RED
		self.message = Label(text='', fg='red')
		self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)
		#Table
		self.tree = ttk.Treeview(height=10, columns=2)
		self.tree.grid(row=4,column=0, columnspan=2)
		self.tree.heading('#0', text='Name', anchor=CENTER)
		self.tree.heading('#1', text='Price', anchor=CENTER)
		
		#Buttons
		ttk.Button(text='DELETE', command=self.delete_products).grid(row=5, column=0, sticky=W+E)
		ttk.Button(text='EDIT', command=self.edit_product).grid(row=5, column=1, sticky=W+E)
		#Filling the rows
		self.get_products()




	def query(self, query, parameters = ()):
		with sqlite3.connect(self.dbname) as conn:
			cursor = conn.cursor()
			result = cursor.execute(query, parameters)
			conn.commit()
			return result

	def get_products(self):
		#Clean table
		records = self.tree.get_children()
		for element in records:
			self.tree.delete(element)

		#quering data	
		query = 'SELECT * FROM product ORDER BY name DESC'
		db_rows = self.query(query)
		for row in db_rows:
			self.tree.insert('', 0, text=row[1], values=row[2])
	
	def validation(self):
		return len(self.name.get()) != 0 and len(self.price.get()) != 0

	def add_product(self):
		if self.validation():
			parameters = (self.name.get().capitalize(), self.price.get())
			query = 'INSERT INTO product VALUES(NULL, ?, ?)'
			
			self.query(query, parameters)
			self.get_products()
			self.message['text'] = 'Product {} added succesfully'.format(self.name.get().capitalize())
			self.name.delete(0, END)
			self.price.delete(0, END)
		else:
			self.message['text'] = 'Name and Price are REQUIRED'

	def delete_products(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text']
		except IndexError:
			self.message['text'] = 'Please select a record'
			return 
		name = self.tree.item(self.tree.selection())['text']
		query = 'DELETE FROM product WHERE name = ?'
		self.query(query, (name,))
		if name != '':
			self.message['text'] = 'Record {} deleted succesfully'.format(name)
		self.get_products()

	def edit_product(self):
		self.message['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text'][0]
		except IndexError:
			self.message['text'] = 'Please select a record'
			return
		name = self.tree.item(self.tree.selection())['text']
		old_price = self.tree.item(self.tree.selection())['values'][0]
		self.edit_wind = Toplevel()
		self.edit_wind.title('Edit product')

		#Old name
		Label(self.edit_wind, text='Old Name:').grid(row=0, column=1)
		Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)

		#New name
		Label(self.edit_wind, text='New Name:').grid(row=1, column=1)
		new_name = Entry(self.edit_wind)
		new_name.grid(row=1,column=2)


		#Old price
		Label(self.edit_wind, text='Old Price:').grid(row=2, column=1)
		Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)

		#New price
		Label(self.edit_wind, text='New Price:').grid(row=3, column=1)
		new_price = Entry(self.edit_wind)
		new_price.grid(row=3,column=2)

		#Button
		Button(self.edit_wind, text='Update', command=lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2, sticky=W+E)

	def edit_records(self, new_name, name, new_price, old_price):
		query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
		parameters = (new_name, new_price, name, old_price)
		self.query(query, parameters)
		self.edit_wind.destroy()
		self.message['text'] = 'The record {} updated to {}'.format(name, new_name)
		self.get_products()


window = Tk()
app = Product(window)
window.mainloop()
