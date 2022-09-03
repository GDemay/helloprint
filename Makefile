init:
	export FLASK_APP=$PWD/app/app.py

run:
	flask --app app/app.py --debug run

db:
	python3 init.py

create_env:
	python3 -m venv ~/.venv/bin/flask
	source ~/.venv/bin/flask/bin/activate