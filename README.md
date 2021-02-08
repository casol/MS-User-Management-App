## Release Notes

* Custom user model
* Views for listing all users, viewing, adding, editing and deleting a single user
* Custom template tags
* Outputting CSV file with user list


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing (Linux)

Try it locally:

Download or "git clone" the package:
```
$ git clone https://github.com/casol/MS-User-Management-App
$ cd MS-User-Management-App
```
First install the module, preferably in a virtual environment:
```
$ python3 -m venv env
# activate virtual environment
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```
Initiate the migration and then migrate the database:
```
(env) $ python manage.py makemigrations
(env) $ python manage.py migrate
```
Create an admin user:
```
(env) $ python manage.py createsuperuser
```
Setup a local server:
```
(env) $ python manage.py runserver
```
Goto

[http://127.0.0.1:8000/home/](http://127.0.0.1:8000/home/)

or

[http://127.0.0.1:8000/signup/](http://127.0.0.1:8000/signup/)

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used

## Authors

*  *Initial work* - [casol](https://github.com/casol)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/casol/MS-User-Management-App/blob/master/LICENSE.md) file for details

t