Server is tested on Ubuntu 21.04 Environment. 

### Step 1. Virtual Environment Settings

After updating python and pip packages, we need to install related libraries required for packages.

```bash
sudo apt update

sudo apt install python-dev python3-dev
sudo apt install python-pip python3-pip
sudo apt install build-essential libssl-dev libffi-dev
```

We will assume you have a python version of at least Python 3.6.9, if not, please upgrade do meet requirements.

Since we need a virtual environment, we install: `virtualenvwrapper` 

```bash
sudo pip3 install virtualenvwrapper
```

open `.bashrc`  with sudo vi ~/.bashrc, and add following at the bottom of the file.

```bash
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

Reload the updated bashrc file:

```bash
source ~/.bashrc
```

After creating a virtual environment, clone the Histudy repository, and install required Python Modules. 

```bash
mkvirtualenv histudy

git clone https://github.com/dodoyoon/Histudy.git

chmod -R 777 ~/Histudy

cd ~/Histudy

pip3 install -r server_requirements.txt
```

pymysql will occasionally cause errors, which in that case, you can edit:
```bash
cd Histudy/pystagram/__init__.py
```
and edit `pymysql.version_info = (1, 4, 0, "final", 0)`


- Reference : how to activate/deactivate virtual env
    - activate : `source ~/.virtualenvs/histudy/bin/activate`
    - deactivate : `deactivate`

### Step 2. HisSecret Settings

HisSecret is a Django password configuration file that is used for privacy in order to protect it from public github repositories. It is recommended to use personal HisSecret files. Here we show how to create a sample.

django secret key can be generated in the following website.

[Djecrety](https://djecrety.ir/)

First, create a directory called HisSecret inside Histudy and create/edit the secret file.
```bash
mkdir HisSecret
cd HisSecret
touch secret.json
```

Below is a sample secret.json file
```json
{
    "DJANGO_SECRET_KEY": "Django generated key goes here",
    "DB_PASSWORD": "DB password(must be the same as MySQL root account password)"
}
```

Now we change the path of SECRET_BASE in Histudy/pystagram/settings.py file to an absolute path.

```python
SECRET_BASE = '/home/g21300109/HisSecret'
```

Alternatively, you can hard code the path inside Histudy/pystagram/settings.py

### Step 3. Installing and connecting Mysql 

Install MySQL onto the server.

```bash
sudo apt install mysql-server
```

Change the default root password by entering mysql.

```bash
sudo mysql

alter user 'root'@'localhost' identified with mysql_native_password by 'password’;
```

The password must be the same as the password in ~/HisSecret/secret.json


We need to change `default ccharacter set` so that MySQL can take Korean

open `sudo vi /etc/mysql/my.cnf` and add the code.

```sql
[client]
default-character-set=utf8

[mysql]
default-character-set=utf8

[mysqld]
collation-server = utf8_unicode_ci
init-connect='SET NAMES utf8'
character-set-server = utf8
```

Restart MySQL
`sudo service mysql restart`

check utf has changed correctly after restarting MySQL

```sql
mysql -u root -p

status
```


Create a database with the name 'study'. You must change the character set before creating dataase to apply character set to utf.

```sql
CREATE DATABASE study;
```

**Fixing Errors**

[https://dodormitory.tistory.com/8](https://dodormitory.tistory.com/8) If you have more errors, check the link out.

 **Create Table**

[manage.py](http://manage.py) Let's run the actual code after creating the table.
```bash
cd ~/Histudy

python3 manage.py makemigrations

python3 manage.py migrate

# Collects static file to .static_root Directory
python3 manage.py collectstatic
```


### Step 4. Installing and Linking Apache

Use `deactivate` to leave virtual env

**apache** and wsgi Module libapache2-mod-wsgi, Python linking module libapache2-mod-wsgi-py3 needs to be installed.

```bash
sudo apt-get install apache2                  # install apache2 
sudo apt-get install libapache2-mod-wsgi      # wsgi Module
sudo apt-get install libapache2-mod-wsgi-py3
```

`sudo vim /etc/apache2/sites-available/000-default.conf` open 000-default.conf and set is as below:

- Setting file guideline

```bash
<VirtualHost *:80>

ServerAdmin webmaster@localhost

DocumentRoot /var/www/html

ErrorLog ${APACHE_LOG_DIR}/error.log

CustomLog ${APACHE_LOG_DIR}/access.log combined

<Directory {wsgi.py가 있는 디렉토리 주소}>

	<Files wsgi.py>

		Require all granted

	</Files>

</Directory>

Alias {settings.py에 STATIC_URL 변수 값} {settings.py에 STATIC_ROOT 디렉토리의 절대주소}
<Directory {settings.py에 STATIC_ROOT 디렉토리의 절대주소}>
        Require all granted
</Directory>

WSGIDaemonProcess tutor python-path={manage.py가 있는 디렉토리의 절대주소} python-home={이 프로젝트를 돌릴 때에 사용하는 virtual environment의 절대주소}
WSGIProcessGroup {프로젝트이름}
WSGIScriptAlias / {wsgi.py가 있는 디렉토리의 주소/wsgi.py}

</VirtualHost>
```

Settings for Histudy

```bash
<VirtualHost *:80>

# The ServerName directive sets the request scheme, hostname and port that
# the server uses to identify itself. This is used when creating
# redirection URLs. In the context of virtual hosts, the ServerName
# specifies what hostname must appear in the request's Host: header to
# match this virtual host. For the default virtual host (this file) this
# value is not decisive as it is used as a last resort host regardless.
# However, you must set it for any further virtual host explicitly.
#ServerName www.example.com

ServerAdmin webmaster@localhost
DocumentRoot /var/www/html

# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
# error, crit, alert, emerg.
# It is also possible to configure the loglevel for particular
# modules, e.g.
#LogLevel info ssl:warn

ErrorLog ${APACHE_LOG_DIR}/error.log
CustomLog ${APACHE_LOG_DIR}/access.log combined

<Directory /home/g21300109/Histudy/pystagram>
	<Files wsgi.py>
		Require all granted
	</Files>
</Directory>

# Static file(js, css 등등)이 들어있는 폴더에 Apache가 접근하게 함
Alias /static /home/g21300109/Histudy/staticfiles
<Directory /home/g21300109/Histudy/staticfiles>
        Require all granted
</Directory>

WSGIDaemonProcess histudy python-path=/home/g21300109/Histudy python-home=/home/g21300109/.virtualenvs/histudy
WSGIProcessGroup histudy
WSGIScriptAlias / /home/g21300109/Histudy/pystagram/wsgi.py

</VirtualHost>
```

Reactivate virtual env

```bash
source ~/.virtualenvs/{virtualenv name}/bin/activate
```

Install Python Module `uwsgi`

```bash
pip install uwsgi
```

if uwsgi cannot be installed properly, check reference below

[pip3 install uwsgi install error:Failed building wheel for uwsgi](https://integer-ji.tistory.com/294)


Now we need to open ports with Django 

First we use ufw to open firewall ports on the iptables. Now we can check if ports are open on the Server

```bash
sudo ufw allow 8000 

sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT

python manage.py runserver 0.0.0.0:8000 
```

Server_IP_Address:8000 should now show Histudy.

`sudo vi /etc/apache2/ports.conf` to open ports.conf and add the opened ports above: 

```bash
#Listen 추가포트
Listen 80
Listen 8000
```

`sudo service apache2 restart` to restart Apache

Now `Server_Ip_Address:8000`will show histutor successfully.

### Step 5. Register Social App for Google Logins

[[Django] Login with Google Account (Local/Real Server)](https://dodormitory.tistory.com/9)

Reference above post to use Google OAuth to upload Domain address with Django for Google Social Application.


### Step 6. Use Let's Encrypt for https 

[Use Let's Encrypt for HTTPS ](https://dodormitory.tistory.com/11)


After configuring https, check the reference in Step4 and add https to the domain.

### Step 7. Set current year and semester

Histudy needs current year and semester information to run properly. To do this you need admin access, and you can create it through:
```bash
cd ~/Histudy/ 
python3 manage.py createsuperuser
```

`https://{histudy ip address}/admin` will show the admin page
After logging in as admin, go to: https://www.histudy.cafe24.com/set_current and set the current year and semester.

### Tips
**1. Enabling debug mode**

Often times if a server error occurs, the Server will only show Server Internal Error without the exact cause.

We can view this by enabling 'DEBUG' variable to True in:~/Histudy/pystagram/settings.py 

DEBUG has security issues in deployment and must be set to FALSE later


**2. Editing or adding Static Files**

Statif files in Django (such as css, js, etc) are kept in one place.

Thus edited or added static files must be added to that single directory.

	1. Enable virtual env: source ~/.virtualenvs/histudy/bin/activate
	2. cd ~/Histudy
	3. python3 manage.py collectstatic

There will be a confirmation: 'This will overwrite existing files!' which you can accept.


**4. Common commands in the server**

```bash
# Apache related
1. Error log file path: /var/log/apache2/error.log
2. Apache config file path: /etc/apache2/sites-available/000-default-le-ssl.conf
3. Restart Apache: sudo service apache2 restart

```


### Reference

[https://dodormitory.tistory.com/](https://dodormitory.tistory.com/2)

[http://wanochoi.com/?p=3575](http://wanochoi.com/?p=3575)

[https://calvinjmkim.tistory.com/23](https://calvinjmkim.tistory.com/23)
