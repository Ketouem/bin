APP_MODULE := "manage.py"

install:
	pip install -r requirements.txt

run:
	FLASK_APP=$(APP_MODULE) FLASK_DEBUG=1 flask run

console:
	FLASK_APP=$(APP_MODULE) flask shell
