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
```

Make a file to configure nginx
``` shell
sudo su
vi /etc/nginx/sites-available/jabber

# This file configure nginx to connect to the gunicorn server that is running in the port below, add the **correct** IP in line 3.
server {
    listen 80;
    server_name 3.87.48.159;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Symlink the file to enabled directory, you should be root
``` shell
ln -s /etc/nginx/sites-available/jabber /etc/nginx/sites-enabled/jabber
```

With the file in that directory, we can test for syntax errors and start
``` shell
sudo nginx -t

# Now restart nginx
sudo systemctl restart nginx
sudo systemctl stop nginx

# Check logs
sudo tail -30 /var/log/nginx/error.log

# Connecttion refused errors might mean you forgot to start gunicorn
```

Use ngrok for testing like this
``` shell
~/ngrok http 80
```

# Database Structure

``` python
user = {
	"id" : user_id from google,
	"name" : Users first name
	"email" : email authenticating google
	"profile_pic" : google profile pic
	"linkedIn" : {
		"email": linkedIn email
		"pwd": linkedIn password
	}
}
```


# References
- https://realpython.com/flask-google-login/
- https://selenium-python.readthedocs.io/
- https://console.developers.google.com/apis/credentials
