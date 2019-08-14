def cssRead (style):
	if style != "ł" or style!="" or style!=None:
		css = {"color":" ","background-color":" ","padding":" ","font-size":" "}
		if style != None:
			tcss = style.split(";")
			for cs in tcss:
				css[cs.split(":")[0].replace(" ","")] = cs.split(":")[1].replace(" ","")
	else:
		css = "ð"
	if css != "ð":
		for sub in list(css):
			if css[sub] == " ":
				del css[sub]
	return css
def cssWrite(style):
	c = ""
	if not style == "":
		for sub in list(style):
			if style[sub] == " ":
				del style[sub]
		c = str(style).replace("{","").replace("}","").replace(",",";").replace('\'',"").replace("\"","")
	return c
