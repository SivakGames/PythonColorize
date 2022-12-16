import re

FG_COLORS = {
	'black': 30,
	'red': 31,
	'green': 32,
	'yellow': 33,
	'blue': 34,
	'magenta': 35,
	'cyan': 36,
	'lightgrey': 37,
	'grey': 90,
	'lightred': 91,
	'lightgreen': 92,
	'lightyellow': 93,
	'lightblue': 94,
	'lightmagenta': 95,
	'lightcyan': 96,
	'white': 97,
}

BG_COLORS = {
	'black': 40,
	'red': 41,
	'green': 42,
	'yellow': 43,
	'blue': 44,
	'magenta': 45,
	'cyan': 46,
	'lightgrey': 47,
	'grey': 100,
	'lightred': 101,
	'lightgreen': 102,
	'lightyellow': 103,
	'lightblue': 104,
	'lightmagenta': 105,
	'lightcyan': 106,
	'white': 107,
}

class styles:
	bold = 1
	fade = 2
	italic = 3
	underline = 4
	reverse = 7


RESET = f"\033[0m"
GRAYSCALE_REGEX = re.compile(r"^gr[a|e]y(?P<greycode>[0-9]{1,2})$", flags=re.IGNORECASE)

#==============================================
def colorize(text, fg=None, bg=None, bold=False, underline=False, italic=False):
	"""
	Apply colors/styling to a string. See colorLookup for more details about assigning color values
	"""

	values = []
	finalFg = colorLookup(fg, isBg=False)
	finalBg = colorLookup(bg, isBg=True)
	boldStyle = [styles.bold] if bold else []
	italicStyle = [styles.italic] if italic else []
	underlineStyle = [styles.underline] if underline else []

	values.extend(finalFg)
	values.extend(finalBg)
	values.extend(boldStyle)
	values.extend(italicStyle)
	values.extend(underlineStyle)
	finalValues = ';'.join(str(item) for item in values)

	return f"\033[{finalValues}m{text}{RESET}"

#==============================================
def colorLookup(code: str | dict, isBg=False):
	"""
	code is the key var and can be the following:
	- A string with a preset color name
	- A string with a 3 digit base 6 code (will be converted to the appropriate 8 bit color)
	- A string with greyXX (value of 0-23)
	- A dictionary with r,g,b keys representing an actual RGB value 
	"""

	target_table = BG_COLORS if isBg else FG_COLORS
	
	finalColors = []

	#Strings
	if (type(code) == str):
		greyGroups = GRAYSCALE_REGEX.match(code)

		if(re.match(r"^[0-5]{3}$", code)):
			colorCode = int(f"{code}", 6) + 16
			finalColors = process8BitAnsiCode(colorCode, isBg)

		elif (greyGroups):
			greyCode = (int(greyGroups.group('greycode')) % 24) + 232
			finalColors = process8BitAnsiCode(greyCode, isBg)
		
		else:
			colorCode = target_table.get(code.lower(), None)
			finalColors = [colorCode] if colorCode != None else []

	#Do an actual RGB value instead
	elif(type(code) == dict):
		r = str(code.get('r', 0) % 256)
		g = str(code.get('g', 0) % 256)
		b = str(code.get('b', 0) % 256)
		typeCode = 48 if isBg else 38
		finalColors = [typeCode,2,r,g,b]
	
	else:
		finalColors = []

	return finalColors


#-----------------------------------------
def process8BitAnsiCode(value: str, isBg: bool = False):
	"""Get the appropriate values for writing an 8 bit color"""

	typeCode = 48 if isBg else 38
	return [typeCode,5,value]


palette = colorize('  ', bg='black')
palette += colorize('  ', bg='grey')
palette += colorize('  ', bg='lightgrey')
palette += colorize('  ', bg='white')

palette += colorize('  ', bg='red')
palette += colorize('  ', bg='lightred')
palette += colorize('  ', bg='green')
palette += colorize('  ', bg='lightgreen')
palette += colorize('  ', bg='yellow')
palette += colorize('  ', bg='lightyellow')
palette += colorize('  ', bg='blue')
palette += colorize('  ', bg='lightblue')
palette += colorize('  ', bg='magenta')
palette += colorize('  ', bg='lightmagenta')
palette += colorize('  ', bg='cyan')
palette += colorize('  ', bg='lightcyan')

print("----------------------------------------")
print("Sample Usage")
print("----------------------------------------")
print(palette)
print(colorize('Foreground', fg='green'))
print(colorize('Background', bg='blue'))
print(colorize('Foreground and Background', fg='yellow', bg='magenta'))
print(colorize('Bold', bold=True))
print(colorize('Italic', italic=True))
print(colorize('Light colors', fg='lightred'))
print(colorize('Light colors', fg='lightblue'))
print(colorize('Light colors', fg='lightgreen'))
print(colorize('Light colors', fg='lightyellow'))
print(colorize('Light colors', fg='lightmagenta'))
print(colorize('Light colors', fg='lightcyan'))
print("----------------------------------------")
print(colorize('8-bit colors (Use a base 6 numeric string for RGB)', fg='100'))
print(colorize('8-bit colors (Use a base 6 numeric string for RGB)', fg='021'))
print(colorize('8-bit colors (Use a base 6 numeric string for RGB)', fg='345'))
print(colorize('Grayscale (0-23)', fg='gray10'))
print(colorize('Grayscale (0-23)', fg='gray15'))
print(colorize('Grayscale (0-23)', fg='gray20'))
print(colorize('True RGB colors', fg={'r':180,'g':30,'b':60}))
print(colorize('True RGB colors', fg={'r':60,'g':180,'b':30}))
print(colorize('True RGB colors', fg={'r':30,'g':60,'b':180}))
