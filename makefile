windows:
	python -m venv env
	.\env\Scripts\activate
	pip install -r requirements.txt
	python app.py

linux:
	python3 -m venv env
	./env/bin/python3 -m pip install --upgrade pip
	./env/bin/python3 -m pip install -r requirements.txt
	./env/bin/python3 app.py