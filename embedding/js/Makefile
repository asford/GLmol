all: GLmol.full.js GLmol.full.min.js

GLmol.full.js: csscolorparser.js three.js GLmol.js 
	./setup_js.py -b csscolorparser.js three.js GLmol.js > GLmol.full.js

GLmol.full.min.js: csscolorparser.js three.js GLmol.js 
	./setup_js.py csscolorparser.js three.js GLmol.js > GLmol.full.min.js
