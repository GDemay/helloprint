init:
	export FLASK_APP=main.py

run:
	flask --app main.py --debug run

db:
	python3 init.py

create_env:
	python3 -m venv ~/.venv/bin/flask
	source ~/.venv/bin/flask/bin/activate

scheduled:
	flask --app main.py scheduled