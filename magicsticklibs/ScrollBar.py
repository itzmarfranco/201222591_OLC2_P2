if __name__=='__main__':
	from Graphics import Tkinter 
else:
	from .Graphics import Tkinter 

class Scrollbar:
	def __init__(self,text):
		self.frame = text.master
		self.text = text
		self.text.configure(wrap='none')
		self.for_x_view()
		self.for_y_view()

	def for_x_view(self):
		# scroll Bar x For width
		scroll_x=Tkinter.Scrollbar(self.frame, orient='horizontal',command=self.text.xview)
		scroll_x.config(command=self.text.xview)
		self.text.configure(xscrollcommand=scroll_x.set)
		scroll_x.pack(side='bottom', fill='x', anchor='w')
		return

	def for_y_view(self):
		# Scroll Bar y For Height
		scroll_y = Tkinter.Scrollbar(self.frame)
		scroll_y.config(command=self.text.yview)
		self.text.configure(yscrollcommand=scroll_y.set)
		scroll_y.pack(side='right', fill='y')		
		return


if __name__ == '__main__':
	root = Tkinter.Tk()
	pad = Tkinter.Text(root,wrap='none')
	Scrollbar(pad)
	pad.pack()
	root.mainloop()
