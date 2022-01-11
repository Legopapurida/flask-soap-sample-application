python -m venv env;
cd env/scripts/
activate.bat
cd ../..
pip install -r ./requirements.txt
mkdir .env => "
FLASK_APP = project
FLASK_ENV = development
"
flask init-db
flask run
