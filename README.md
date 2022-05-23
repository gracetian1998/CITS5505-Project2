# CITS5505-Project2
# Online daily Puzzle

## Describe

This is a Puzzle game , user could control the person move at the map
When user face to the box, user could push and move the box.
Push all the box to right place will win the game.
The step you used will be stored, and let's try to use the least step to win the game


## Develop

### Front END

Dependence path: static/lib
  * bootstrap
  * jquery


### Back END
### Use env

```shell
# create env
/xxx/xxx/bin/virtualenv  -p  /xxx/xxx/bin/python3  env

# install package
python  -m pip install   -r requirements.txt 

```

### Not use env

```shell
# install package
python  -m pip install   -r requirements.txt 
```

### Dependence

```shell
    click==8.1.3
    Flask==2.1.2
    Flask-SQLAlchemy==2.5.1
    greenlet==1.1.2
    importlib-metadata==4.11.3
    itsdangerous==2.1.2
    Jinja2==3.1.2
    MarkupSafe==2.1.1
    SQLAlchemy==1.4.36
    Werkzeug==2.1.2
    zipp==3.8.0
```
### DB
db config

```python 
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

app.db

| filed    | type        | attr        | default |
|----------|-------------|-------------|--------|
| id       | Integer     | primary_key |     |
| name     | String(80)  | unique      |        |
| password | String(120) | unique      |        |
| bestStep | Integer     | unique      |        |
| imgPath  | String(200) | unique      |../static/img/0.png|

## Author
```
#Wenbo Gao 23335934 

Mainly responsible for the preparation of web front-end programs focusing on game design, 
user registration and login, paging. JS can be edited with object-oriented ideas. 
For example, in this project, game.html JS is edited in an object-oriented way. The game objects include init, createMap and controlPerson.
Size (number of map squares),level(initialization registration),stepNum(number of steps),mapDate(map data) are all attributes of the object.
```

```
#Yazhen Tian 22942152

I am mainly responsible for the back-end development of this project. 
The main work is the design and implementation of the backend logic of the website 
and the saving and reading of user and website data. Creating user environments and beautifying web pages and game effects.

For example, user registration and login in our website, user registration information is sent to the backend through the frontend,
and the backend saves it in the database, 
when the user logs into the website, the backend needs to determine whether the user has permission to log in 
by whether the user name and password entered by the user are the same as those in the database.
I think the most difficult part is to combine the front-end and back-end. I spent a lot of time working on this part.
```


