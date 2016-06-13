example: example.mdl lex.py main.py matrix.py mdl.py script.py yacc.py
	python main.py example.mdl

anim-test: gmath.py
	python main.py animtest.mdl

robot: robot.mdl lex.py main.py matrix.py mdl.py script.py yacc.py
	python main.py robot.mdl

clean:
	rm *pyc *out parsetab.py

clear:
	rm *pyc *out parsetab.py *ppm
