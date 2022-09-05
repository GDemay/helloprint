run:
	flask --app app/app.py --debug run

create_env:
	python3 -m venv ~/.venv/bin/flask

start_env:
	source ~/.venv/bin/flask/bin/activate

test: 
	python3 -m pytest --disable-pytest-warnings --verbose
