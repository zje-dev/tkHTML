from tkinter import *
from tkinter import ttk
from lxml import etree
from io import StringIO, BytesIO
from tkCSS import cssRead
import os
xp = 0
yp = 0
textTag = ["b","i","sup","sub","span","h1","h2","h3","h4","h5","h6","a"]
contTag = ["div","header","footer","form","center"]
class Finput:
	TKelement = None
	def __init__(self,elem,parent,tp):
		element = etree.fromstring(elem)
		global xp, yp
		if tp == "button" or tp == "submit":
			self.TKelement = Button(parent)
			if "value" in element.attrib:
				self.TKelement.configure(text=element.get("value"))
		else:
			self.TKelement = Entry(parent)
			if "value" in element.attrib:
				self.TKelement.insert(0,element.get("value"))
		self.TKelement.grid(row=yp,column=xp,sticky=N+W)
		if "style" in element.attrib:
			css = cssRead(element.get("style"))
			if "background-color" in css.keys():
				self.TKelement["bg"] = css["background-color"]
			else:
				self.TKelement["bg"] = self.TKelement.master["bg"]
			if "color" in css.keys():
				self.TKelement.configure(fg=css["color"])
class div:
	DOMelement = ""
	TKelement = None
	def __init__(self,elem,parent,iam):
		self.DOMelement = elem
		element = etree.fromstring(elem)
		self.TKelement = Frame(parent)
		global xp, yp
		if iam == "div" or iam == "header" or iam == "footer" or iam == "form":
			self.TKelement.grid(row=yp,column=xp,sticky=N+W)
		elif iam == "center":
			self.TKelement.grid(row=yp,column=xp,sticky=N)
		if "style" in element.attrib:
			css = cssRead(element.get("style"))
			if "background-color" in css.keys():
				self.TKelement["bg"] = css["background-color"]
			else:
				self.TKelement["bg"] = self.TKelement.master["bg"]
			if "padding" in css.keys():
				self.TKelement.configure(padx=css["padding"],pady=css["padding"])
		else:
			self.TKelement["bg"] = self.TKelement.master["bg"]
		for QEdoom in element:
			parOne(self.TKelement,etree.tostring(QEdoom))
class text:
	font_size = 11
	font_family = "Helvetica"
	def __init__(self,elem,par):
		element = etree.fromstring(elem)
		tfont = "bold"
		if element.tag == "b":
			tfont = "bold"
			self.font_size = 12
		elif element.tag == "i":
			tfont = "italic"
		elif element.tag in ["h1","h2","h3","h4","h5","h6"]:
			self.font_size = 18 - int(int(element.tag[1]) * 2)
		else:
			tfont = "normal"
		t = Label(par,text=element.text, font=tfont)
		t.grid(row=yp,column=xp,sticky=N+W)
		if "style" in element.attrib:
			css = cssRead(element.get("style"))
			if "background-color" in css.keys():
				t["bg"] = css["background-color"]
			else:
				t["bg"] = t.master["bg"]
			if "color" in css.keys():
				t.configure(fg=css["color"])
			if "font-size" in css.keys():
				self.font_size = css["font-size"]
			if "padding" in css.keys():
				t.configure(padx=css["padding"],pady=css["padding"])
		else:
			t["bg"] = t.master["bg"]
			t.configure(fg="black")
		ont = (self.font_family, self.font_size, tfont)
		t.configure(font=ont)
def formaHTML (canvas, isL):
	global xp, yp
	xp = 0
	yp = 0
	for element in canvas.winfo_children():
		element.destroy()
	inf =  os.popen("cat "+ isL).read()
	parser = etree.HTMLParser()
	canvas.configure(borderwidth = 0,highlightthickness=0)
	tree = etree.parse(StringIO(inf), parser).getroot()
	if "style" in tree[1].attrib:
		css = cssRead(tree[1].get("style"))
		if "background-color" in css.keys():
			canvas.configure(bg=css["background-color"])
	for elemint in tree[1]:
		parOne(canvas,etree.tostring(elemint))
def parOne (parent,data):
	if len(data) > 1:
		ele = etree.fromstring(data)
		global xp, yp
		if ele.tag in textTag:
			text(etree.tostring(ele),parent)
			xp += 1
			if ele.tag in ["h1","h2","h3","h4","h5","h6"]:
				xp = 0
				yp += 1
		elif ele.tag == "br":
			xp = 0
			yp += 1
		elif ele.tag in contTag:
			div(etree.tostring(ele),parent,ele.tag)
			yp += 1
		elif ele.tag == "input":
			if "type" in ele.attrib:
				Finput(etree.tostring(ele),parent,ele.get("type"))
