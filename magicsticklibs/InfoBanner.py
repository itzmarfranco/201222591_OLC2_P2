from Graphics import Tkinter
from Graphics import tkFont, ttk
import time
from threading import Thread

WIDTH=250
HEIGHT=150
class Banner:
	def __init__(self, widget, text, width=None, height=None):
		self.widget = widget
		self.text = text
		self.FocusLine = False
		self.window = None
		self.width=width
		self.height=height
		self.MouseBindings()

	def AutoHide(self):
		time.sleep(5)
		self.HideInfo()
		return

	def MouseBindings(self):
		# Show Banner
		for key in ['<Enter>']:
			self.widget.bind(key, self.ShowInfo)
		
		for key in ['<Leave>']:
			self.widget.bind(key, self.HideInfo)
		return
		


	def HideInfo(self, event=None):
		if self.window:
			self.window.destroy()
			self.window=None
		return

	def ShowInfo(self, event=None):
		if not self.window:
			self.window=Tkinter.Toplevel()
			self.window.overrideredirect(True)
			WIDTH = self.width or len(self.text)*10
			HEIGHT = self.height or (len(self.text.split('\n'))+1)*10
			self.window.geometry("%dx%d+%d+%d" % (WIDTH,HEIGHT,
				event.x_root+10,
				event.y_root+10
				))
			Label=Tkinter.Label(self.window, text=self.text, font=("arial 10 bold"), fg='white', bg='black')
			Label.pack(expand=True, fill='both')
			self.window.wait_visibility(self.window)
			self.window.attributes('-alpha',0.7)
			t= Thread(target=self.AutoHide)
			t.start()
		return

if __name__=='__main__':       
	root = Tkinter.Tk()
	Button = Tkinter.Button(root, text="Point Mouse Here")
	Button.pack(padx=20, pady=20)
	Banner(Button, """Testing Windows""")
	root.mainloop()
