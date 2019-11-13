venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip3 install  --ignore-installed -Ur requirements.txt
	touch venv/bin/activate

init: venv
	. venv/bin/activate

test: init
	. venv/bin/activate ; python3 manage.py test --pattern="test*.py"

run: venv
	. venv/bin/activate ; find -iname "*.pyc" -delete; python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000

makemigrations: init
	. venv/bin/activate ; python3 manage.py makemigrations

migrate: init
	. venv/bin/activate ; python3 manage.py migrate; python3 manage.py createcachetable

