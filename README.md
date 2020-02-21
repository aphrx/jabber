# Setup

Make a new virtual environment and Install requirements
``` shell
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

deactivate # To deactivate environment after use
```

To run the server for development
``` shell
export FLASK_APP=app.py
export FLASK_DEBUG=1    # To reload when app.py changes
flask run
```

# References

- https://realpython.com/flask-google-login/
