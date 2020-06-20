
if __name__=='__main__':
	from Graphics import Tkinter 
else:
	from .Graphics import Tkinter 

"""
SelectAll
DeselectAll
OpenFile
Cut
Redo
SaveAs
Save
Root
Undo
FindAll
FontChooser
ReplaceAll
OpenNew
ConfigApply
SaveConfig
Open
ResetTags
Copy
Paste
Find
Replace
ColorMode

"""

class MenuBar:
	def __init__(self, text):
		self.text = text
		self.create_menubar()

	def create_menubar(self):
		self.bar = Tkinter.Menu(self.text.storeobj['Root'])


		# Creating Sub menu
		sub_menu=Tkinter.Menu(self.bar, tearoff=0)
		self.bar.add_cascade(label='Archivo', menu=sub_menu)

		sub_menu.add_command(label="Nuevo", accelerator="Ctrl+N",compound="left", underline=0, command=self.text.storeobj['OpenNew'])
		sub_menu.add_command(label="Abrir", accelerator="Ctrl+O",compound="left", underline=0, command=self.text.storeobj['Open'])
		sub_menu.add_separator()
		sub_menu.add_command(label="Guardar", accelerator="Ctrl+S",compound="left", underline=0, command=self.text.storeobj['Save'])
		sub_menu.add_command(label="Guardar Como", accelerator="Ctrl+Shift+S",compound="left", underline=0, command=self.text.storeobj['SaveAs'])
		sub_menu.add_separator()
		sub_menu.add_command(label="Salir", accelerator="Ctrl+Q",compound="left", underline=0, command=self.text.storeobj['Quit'])

		# Creating Sub menu
		sub_menu=Tkinter.Menu(self.bar, tearoff=0)
		self.bar.add_cascade(label='Editar', menu=sub_menu)

		sub_menu.add_command(label="Adelante", accelerator="Ctrl+Shift+Z",compound="left", underline=0, command=self.text.storeobj['Redo'])
		sub_menu.add_command(label="Atras", accelerator="Ctrl+Z",compound="left", underline=0, command=self.text.storeobj['Undo'])
		sub_menu.add_separator()
		sub_menu.add_command(label="Copiar", accelerator="Ctrl+C",compound="left", underline=0, command=self.text.storeobj['Copy'])
		sub_menu.add_command(label="Cortar", accelerator="Ctrl+X",compound="left", underline=0, command=self.text.storeobj['Cut'])
		sub_menu.add_command(label="Pegar", accelerator="Ctrl+P",compound="left", underline=0, command=self.text.storeobj['Paste'])
		sub_menu.add_separator()
		sub_menu.add_command(label="Selec Todo", accelerator="Ctrl+A",compound="left", underline=0, command=self.text.storeobj['SelectAll'])
		sub_menu.add_command(label="Deselect Todo", accelerator="",compound="left", underline=0, command=self.text.storeobj['DeselectAll'])
		

		# Creating Sub menu
		sub_menu=Tkinter.Menu(self.bar, tearoff=0)
		self.bar.add_cascade(label='Interpretar', menu=sub_menu)		
		sub_menu.add_command(label="Ejecutar", accelerator="Ctrl+R",compound="left", underline=0, command=self.text.storeobj['Interpretar'])

		# Creating Sub menu
		sub_menu=Tkinter.Menu(self.bar, tearoff=0)
		self.bar.add_cascade(label='Herramienta', menu=sub_menu)

		sub_menu.add_command(label="Encontrar", accelerator="Ctrl+F",compound="left", underline=0, command=self.text.storeobj['Find'])
		sub_menu.add_command(label="Encontrar Todos", accelerator="Ctrl+Shift+F",compound="left", underline=0, command=self.text.storeobj['FindAll'])
		sub_menu.add_separator()
		sub_menu.add_command(label="Reemplazar", accelerator="Ctrl+H",compound="left", underline=0, command=self.text.storeobj['Replace'])
		sub_menu.add_command(label="Reemplazar Todo", accelerator="Ctrl+Shift+H",compound="left", underline=0, command=self.text.storeobj['ReplaceAll'])
		
		# Creating Sub menu
		sub_menu=Tkinter.Menu(self.bar, tearoff=0)
		self.bar.add_cascade(label='Preferencias', menu=sub_menu)

		sub_menu.add_command(label="Font", accelerator="Ctrl+F1",compound="left", underline=0, command=self.text.storeobj['FontChooser'])
		sub_menu.add_separator()
		sub_menu.add_command(label="Modo Nocturno", accelerator="",compound="left", underline=0, command=self.text.storeobj['ColorMode'])
		sub_menu.add_command(label="Modo Claro", accelerator="",compound="left", underline=0, command=self.text.storeobj['ColorMode2'])
		
		# Creating Sub menu
		sub_menu=Tkinter.Menu(self.bar, tearoff=0)
		self.bar.add_cascade(label='Ayuda', menu=sub_menu)

		sub_menu.add_command(label="Plugins", accelerator="",compound="left", underline=0, command=self.text.storeobj['OpenNew'])
		sub_menu.add_command(label="Acerca De", accelerator="",compound="left", underline=0, command=self.text.storeobj['OpenNew'])
		





		self.text.storeobj['Root'].configure(menu=self.bar)
		
		
		return

if __name__ == '__main__':
	root= Tkinter.Tk()
	pad=Tkinter.Text(root)
	pad.pack()
	pad.storeobj={"Root":root}
	MenuBar(pad)
	root.mainloop()

