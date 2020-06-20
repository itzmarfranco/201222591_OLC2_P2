if __name__=='__main__':
	from Graphics import Tkinter
else:
	from .Graphics import Tkinter

if __name__=='__main__':
	from Graphics import Tkinter as tk, tkFileDialog, tkMessageBox 
else:
	from .Graphics import Tkinter as tk, tkFileDialog, tkMessageBox
import time
import threading


class AutoWrite:
	def __init__(self, pad):
		self.text = pad
		path = tkFileDialog.askopenfilename()
		if path:
			self.s = open(path, 'r').read()
			self.insert_words()
		else:
			self.s = None

	def insert_words(self):
		print("[+] Auto Typing Executed")
		for i in self.s:
			self.text.insert("end", str(i))
			time.sleep(0.1)
			self.text.master.update()
			self.text.master.update_idletasks()
		return


if __name__ == '__main__':
	root = Tkinter.Tk()
	t= Tkinter.Text(root)
	t.pack()
	k=AutoWrite(t)
	s=threading.Thread(target=k.insert_words)
	k.insert_words()
	s.start()
	root.mainloop()