# Setup

Deployed here: https://jabber.store

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

# Setting up EC2 for deployment

Followed this setup elastic ip, custom domain and an SSL certificate using certbot
https://blog.cloudboost.io/setting-up-an-https-sever-with-node-amazon-ec2-nginx-and-lets-encrypt-46f869159469

nginx config file ended up like this
``` shell
sudo su
vi /etc/nginx/sites-available/jabber

# This file configure nginx to connect to the gunicorn server that is running in the port below
server {
       listen 80;
       listen [::]:80;
       server_name jabber.store www.jabber.store;
       return 301 https://$server_name$request_uri;
}

server {
       listen 443 ssl http2 default_server;
       listen [::]:443 ssl http2 default_server;
       server_name jabber.store www.jabber.store;

location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
}

ssl_certificate /etc/letsencrypt/live/jabber.store/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/jabber.store/privkey.pem;
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
ssl_prefer_server_ciphers on;
ssl_ciphers EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;

ssl_session_cache shared:SSL:5m;
ssl_session_timeout 1h;
add_header Strict-Transport-Security “max-age=15768000” always;
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

Now run gunicorn which will start the proxy serving connecting to the specific port
``` shell
# -D to demonize it in the background
# after running app.pid will have the pid of the process
# -b to to bind it to a specific ip so we can connect to it in nginx config
gunicorn app:app -p app.pid -b 127.0.0.1:8000 -D

# To kill gunicorn anytime
kill -HUP `cat app.pid`
kill `cat app.pid`
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
	"cv": cv template text data
}
```

# References
- https://realpython.com/flask-google-login/
- https://selenium-python.readthedocs.io/
- https://console.developers.google.com/apis/credentials
- https://certbot.eff.org/lets-encrypt/ubuntuxenial-nginx
- https://blog.cloudboost.io/setting-up-an-https-sever-with-node-amazon-ec2-nginx-and-lets-encrypt-46f869159469
