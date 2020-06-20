if __name__=='__main__':
	
	from Graphics import Tkinter as tk
	from TextPad import TextPad
	from TextPadConsola import TextPadConsola

	import tkinter 
	import os	 

else:
	
	from .Graphics import Tkinter as tk
	from .TextPad import TextPad
	from .TextPadConsola import TextPadConsola

class TextPad_Window(tk.Tk):


	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self._text_pad_()
		#self._text_pad_consola()

	def _text_pad_(self):
		TextPad(self).pack()
		TextPadConsola(self).pack()
		
		return

	#
	#def _text_pad_consola(self):
	#	TextPadConsola(self).pack()
	#	return
	#

if __name__=='__main__':
	
	from Graphics import Tkinter as tk
	from TextPad import TextPad
	from TextPadConsola import TextPadConsola
	
else:
	#print ("Except")
	pass
