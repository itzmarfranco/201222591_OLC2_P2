if __name__=='__main__':
	from Graphics import Tkinter
	from ConfigSettings import Connect
else:
	from .Graphics import Tkinter
	from .ConfigSettings import Connect

class TextPad(Tkinter.Text):
	def __init__(self, *args, **kwargs):
		Tkinter.Text.__init__(self, *args, **kwargs)
		self.storeobj = {"Root": self.master}
		self.Connect_External_Module_Features()
		self._pack()

	def Connect_External_Module_Features(self):
		Connect(self)
		return

	def _pack(self):
		self.pack(expand = True, fill = "both")
		return
	
if __name__ == '__main__':
	root = Tkinter.Tk(className = " Test TextPad")
	TextPad(root)
	root.mainloop()
