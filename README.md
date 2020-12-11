Backend for simple forum made with awesome [Piccolo ORM](https://www.piccolo-orm.com/) ecosystem.

Open terminal and run:

```shell
virtualenv -p python3 envname
cd envname
source bin/activate
git clone https://github.com/sinisaos/headless-forum-fastapi.git
cd headless-forum-fastapi
pip install -r requirements.txt
sudo -i -u yourpostgresusername psql
CREATE DATABASE forum;
\q
touch .env
## put this in .env file
## DB_NAME="your db name"
## DB_USER="your db username"
## DB_PASSWORD="your db password"
## DB_HOST="your db host"
## DB_PORT=5432
## SECRET_KEY="your secret key"

## runing migrations for admin
piccolo migrations forwards user
piccolo migrations forwards session_auth
## runing migrations for site
piccolo migrations forwards forum
## create admin user
piccolo user create
uvicorn app:app --port 8000 --host 0.0.0.0 
```
After site is running log in as admin user on [localhost:8000/admin/](http://localhost:8000/admin/) and add categories, topics etc. 

For non admin user go to API docs [localhost:8000/docs/](http://localhost:8000/docs/) where you can register.

After that you can login with Authorize button to access protected routes.


