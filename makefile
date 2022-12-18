f: freeze
freeze:
	pip freeze > requirements.txt

i: install
install:
	pip install -r requirements.txt

r: run
run:
	python3 face.py

rw: run_watch
run_watch:
	watchmedo shell-command \
	--patterns="*.py" \
	--command='python "${watch_src_path}"' \
	.
