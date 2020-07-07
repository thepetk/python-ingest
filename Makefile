PYCODE = import flask.ext.statics as a; print a.__path__[0]

default:
	@echo "\nPython Ingest make commands\n"
	@echo "Commands available:\n"
	@echo "    make image		# builds a python-ingest image."

run:
	docker build -t python-ingest:v1 .
