# Live Test Scores

This application shows the current esam scores in tests performed by students.

Install dependencies, and create empty virtual environment:

```sh
virtualenv --python=python3 venv
. venv/bin/activate
pip3 install -r requirements.txt
python manage.py migrate
python manage.py test
```

Run the application:
```sh
python manage.py runserver
```

Available endpoints:

```
curl http://localhost:8000/students/
curl http://localhost:8000/students/<id>
curl http://localhost:8000/exams/
curl http://localhost:8000/exams/<number>
```
