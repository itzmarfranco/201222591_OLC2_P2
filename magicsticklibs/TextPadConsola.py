if __name__=='__main__':
	from Graphics import Tkinter
	from ConfigSettings import Connect
else:
	from .Graphics import Tkinter
	from .ConfigSettings import Connect

class TextPadConsola(Tkinter.Text):
	def __init__(self, *args, **kwargs):
		Tkinter.Text.__init__(self, *args, **kwargs)
		self.storeobj = {"Root": self.master}
		self.insert('insert','>>')
		self.config(bg='black', fg='green', height=8, state='disabled')
		pass

if __name__ == '__main__':
	root = Tkinter.Tk(className = " Test TextPadConsola")
	TextPadConsola(root)
	root.mainloop()
