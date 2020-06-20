if __name__=='__main__':
	from Graphics import Tkinter as tk, tkFileDialog, tkMessageBox 
else:
	from .Graphics import Tkinter as tk, tkFileDialog, tkMessageBox

class FileHandler:
	def __init__(self, text):
		self.text = text
		self.text.storeobj['OpenFile']=None
		self.functions_key_bindings()
		self.binding_key_configuration()

	def binding_key_configuration(self):
		for key in ['<Control-N>',"<Control-n>"]:
			self.text.bind(key, self.new_file)
		for key in ['<Control-S>',"<Control-s>"]:
			self.text.bind(key, self.save_file)
		for key in ['<Control-Shift-S>',"<Control-Shift-s>"]:
			self.text.bind(key, self.save_as)
		for key in ['<Control-O>',"<Control-o>"]:
			self.text.bind(key, self.open_file)
		for key in ['<Control-q>',"<Control-Q>"]:
			self.text.bind(key, self.quit)
		return

	def functions_key_bindings(self):
		self.text.storeobj['Open']=self.open_file
		self.text.storeobj['Save']=self.save_file
		self.text.storeobj['SaveAs']=self.save_as
		self.text.storeobj['OpenNew']=self.new_file
		self.text.storeobj['Quit']=self.quit
		return

	def open_file(self, event=None):
		path = tkFileDialog.askopenfilename()
		if path:
			data=open(path,"r").read()
			self.text.delete('1.0','end')
			self.text.insert("1.0", data)
			self.text.storeobj['OpenFile']=path
		return

	def save_file(self, event=None):
		if not self.text.storeobj['OpenFile']:
			path = tkFileDialog.asksaveasfilename()
		else:
			path = self.text.storeobj['OpenFile']
		if path:
			data = self.text.get("1.0",'end')
			f_=open(path,"w")
			f_.write(data)
			f_.close()
			self.text.storeobj['OpenFile']=path

		return

	def save_as(self, event=None):
		path = tkFileDialog.asksaveasfilename()
		if path:
			data = self.text.get("1.0",'end')
			f_=open(path,"w")
			f_.write(data)
			f_.close()
		return

	def new_file(self, event=None):
		import os
		os.system("python main.py")
		return

	def quit(self, event=None):
		ask=tkMessageBox.askyesnocancel(title="Save Data Or Not", message="Save changes to New file before closing?")
		if ask==None:
			return
		elif ask==False:
			pass
		else:
			self.save_file()
		if self.text.storeobj['OpenFile']:
			
			f=open("cachememory", 'w')
			f.write(self.text.storeobj['OpenFile'])
			f.close()
		import sys
		sys.exit(0)
		return
	

if __name__ == '__main__':
	root = tk.Tk()
	pad = tk.Text(root)
	pad.pack()
	pad.storeobj={}
	FileHandler(pad)
	root.mainloop()
