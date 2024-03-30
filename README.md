# TaskFlow Manager

Web application IT company task manager which allows to track tasks, deadlines, assignees, and projects

## Check it out!

[TaskFlow Manager App](https://taskflow-6pzs.onrender.com)
<br>
(You would need to wait for ~1 minute for the server to wake up)

<i>If you don't want to register you can use the following credentials:</i>

* <i>Login: tester</i>
* <i>Password: Sandbox!1</i>

## Installing locally / Getting started

Python3 must be already installed

```shell
git clone https://github.com/kabust/TaskFlow-Web-App.git
cd TaskFlow-Web-App
python3 -m venv venv
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata generated_data.json
python manage.py runserver
```

After running that code you'll be able to browse the website locally on your computer.

### Features

* Authentication functionality for Worker/User
* Managing tasks and projects from the presented interface
* Following tasks deadlines and assignees
* Filtering and searching
* Admin panel for advanced DB management

## Demo
![Website Interface](demo.png)
