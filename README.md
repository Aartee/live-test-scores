# live-test-scores

virtualenv --python=python3 venv
. venv/bin/activate
pip3 install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver

django-admin startproject channelmeter_server
django-admin startapp app_channelmeter_live_test_scores
