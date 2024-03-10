Backend for simple forum made with [FastAPI](https://fastapi.tiangolo.com/) and [Piccolo ORM](https://www.piccolo-orm.com/) ecosystem.

-------------------------------------------------------

### Instalation

Clone repository in fresh virtualenv.

```bash
git clone https://github.com/sinisaos/headless-forum-fastapi.git
```

### Install requirements


```bash
cd headless-forum-fastapi
pip install -r requirements/requirements.txt
```

### Create database table


```bash
sudo -i -u yourpostgresusername psql
CREATE DATABASE forum;
\q;
```

### Setup
-------------------------------------------------------
Create ``.env`` file in root of the project.

```bash
DB_NAME=your db name
DB_USER=your db username
DB_PASSWORD=your db password
DB_HOST=your db host
DB_PORT=your db port
SECRET_KEY=your secret key
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Migrations

```bash
./scripts/migrations.sh
```

### Create admin user

```bash
./scripts/user.sh
```

### Getting started 

```bash
./scripts/start.sh
```

After site is running log in as admin user on [localhost:8000/admin/](http://localhost:8000/admin/) and add categories, topics etc. 

For non admin user go to API docs [localhost:8000/docs/](http://localhost:8000/docs/) where you can register.

After that you can login with Authorize button to access protected routes.