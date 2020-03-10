# Setup

Make a new virtual environment and Install requirements
``` shell
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt

deactivate # To deactivate environment after use
```
To support Selenium, one of these web-drivers needs to be installed based the browser you want to test
https://selenium-python.readthedocs.io/installation.html#drivers

To run the server for development
``` shell
export FLASK_APP=app.py
export FLASK_DEBUG=1    # To reload when app.py changes
python app.py
```

Setting up EC2 for deployment
``` shell
# -D to demonize it in the background
# after running app.pid will have the pid of the process
# -b to to bind it to a specific ip so we can connect to it in nginx config
gunicorn app:app -p app.pid -b 127.0.0.1:8000 -D

# To kill gunicorn anytime
kill -HUP `cat app.pid`
kill `cat app.pid`

# This file configure nginx to connect to the gunicorn server that is running in the port below
server {
    listen 80;
    server_name 3.87.48.159;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
# This file configure nginx to connect to the gunicorn server that is running in the port below

# make file and then make a symlink enable the available site
sudo su
vi /etc/nginx/sites-available/assignment1
ln -s /etc/nginx/sites-available/assignment1 /etc/nginx/sites-enabled/assignment1

# With the file in that directory, we can test for syntax errors by typing:
sudo nginx -t

sudo systemctl restart nginx
sudo systemctl stop nginx

# Check logs
sudo tail -30 /var/log/nginx/error.log
```

# References

- https://realpython.com/flask-google-login/
- https://selenium-python.readthedocs.io/
