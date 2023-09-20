# FLASK Deployment
The FLASK Deployment repo is created for implementation of FLASK project \
(Users-Authors-Articles) in Docker containers.
The project can be implemented either as python application or as a set of containers.

## Project stack:
- Flask
  - werkzeug
  - requests
  - sqlalchemy
  - json
  - swagger
  - docker
  - docker-compose

### User Authorisation
Authorisation implemented on login - password pair (Example user1: 123)

### API Documentation
API documentation is implemented with swagger package.
API documentation is available at live demo via link: 
```shell
/api/docs
```

### Live Demo 
Live Demo of the project is available by your request to 
```shell
mailto: ecrvmal@yandex.ru 
```



## Implementation with docker-compose:
1. Create docker image
```shell
docker-compose build
```
1. Create new virtual env
```shell
docker-compose up -d
```

## Implementation  as an python app
1. Create new virtual env
```shell
python3 -m venv ./venv
```
2. copy `example.env` to `.env` and set `SECRET_KEY`
3. activate virtual env
```shell
source venv/bin/activate
```
4. install dependencies
```shell
pip install -r requirements.txt
```
5. Run command for init db and create user
```shell
flask init-db
flask create-init-user
```
6. Run flask application
```shell
flask run
```