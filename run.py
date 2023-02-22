# python -m flask --app app.py run
# python app.py
# lsof -i :5000
# kill -9 PID

# export FLASK_APP=app.py
# export FLASK_ENV=development
# flask run

from app import app




if __name__ == "__main__":
    app.run()
