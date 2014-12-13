UW Message Coding
=========

Currently in very early development!


Development Setup
-----------------

To run this project, you can either set up your own machine or
use a virtual Ubuntu machine with Vagrant.
There are separate instructions for each below:


### Run in a VM

There is configuration included to run this project
inside an Ubuntu virtual machine controlled by Vagrant.

This is especially recommended on Windows.
If you go this route, you can skip the Manual Setup
section below.

Instead, follow these steps:

1. Install [Vagrant](https://www.vagrantup.com/downloads.html) and [Virtualbox](https://www.virtualbox.org/wiki/Downloads)

2. Start the virtual machine.

   This will download a basic Ubuntu image, install
   some additional software on it, and perform the initial project setup.

   ```bash
   $ vagrant up
   ```

3. Once your Ubuntu VM is started, you can SSH into it with `vagrant ssh`
   or SSH to `localhost:2222`.

   When you log in, your terminal will automatically drop into
   a Python virtualenv and cd to `/home/vagrant/uw-message-coding`.


### Manual Setup

You will need to have the following packages installed:

- Python 2.7
- MySQL 5.5
- pip
- Node.js with npm
- [Bower](http://bower.io/)

Once you have the above prerequisites, follow these steps
to set up the project:

1. Create a MySQL database.

2. Create a file in the main project folder
   called `.env` with the following:

   ```
   DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
   ```

   There is an example `.env` file in `setup/templates/vagrant_dot_env`.

3. Install additional Python dependencies.

   Note: It is recommended that you create and work in
   a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

   Run this to install needed python modules:

   ```bash
   $ pip install -r requirements/local.txt
   ```

4. Install any additional requirements and run the database migrations:

   ```bash
   $ fab dependencies migrate
   ```

Structure
---------

Below is the basic project file structure:

```
.
├── setup                 # Scripts and templates for setting up running machines
│
├── requirements          # Python dependency lists for pip
│   ├── base.txt         # Requirements for all setups
│   ├── local.txt        # Additional requirements for development setups
│   ├── production.txt   # Additional requirements for production setups
│   └── requirements     # Additional requirements for running tests
│
├── message_coding
│   ├── message_coding     # The Django project files (settings, wsgi.py, main urls.py)
│   ├── base               # Global Django application containing cross-cutting stuff
│   ├── apps               # Site modules
│   │   ├── project       # App for high-level project stuff
│   │   ├── dataset       # App for dataset-related stuff
│   │   └── coding        # App for code schemes and coding stuff
│   │
│   ├── templates          # Global site templates
│   ├── static             # Static files (javascript, css, bower components, etc.)
│   └── manage.py          # The Django management script
│
├── fabfile.py           # Contains common maintenance tasks
└── Vagrantfile          # Defines an Ubuntu VM for testing
```

Workflow
--------

Some common tasks you might need to do...


### Install dependencies

If someone has added Python packages to one of the files in
`requirements/*.txt`, added Bower packages to `bower.json`,
or added NPM packages to `package.json`, you can
update everything with:

```bash
$ fab dependencies
```


### Update the database

If someone has added migrations, you can
run `fab migrate` to run the migrations and update your
development database.

Should you need to reset your database,
you can use `fab reset_db` but be CAREFUL with this.

### Load the test data

There is some test data contained in the file `setup/test_data.json`.
After you run `fab migrate` to create your database structure,
you can load the test data:

```bash
$ fab load_test_data
```

This data contains two user profiles. There is an admin
user that can access the admin controls, as well
as another user who owns a project. Below are their
credentials:

```
Test user: testuser/password
Admin user: admin/admin
```

If you change the database structure or otherwise need to update
the test data file, you can run:

```bash
$ fab make_test_data
```


### Start the webserver

Change to the project directory and start the development
webserver using `fab runserver`.

The Django webservr will listen on port 8000.
If you are running in a Vagrant VM, you can view the site
at http://localhost:8080. Otherwise, use http://localhost:8000.


### Create new styles

Add new CSS files to `message_coding/static/css`.
To load these in a Django template, add the following:

```html
{% load 'staticfiles' %} {# You will need this at the top of your file #}

{% block css %}
    {{ block.super }}
    <link rel="stylesheet" type="text/css" href="{% static 'css/YOUR_PATH_HERE.css' %}">
{% endblock %}
```

You can also write your styles in [LESS](http://lesscss.org),
which will be automatically converted to CSS when it is served to your browser.
Just make sure to set `type="text/less"` in the link tag.

The project includes theme styles in `message_coding/static/css/theme`
that load Bootstrap and allow you to override variables and add additional theme styles.


### Create JavaScript

You can add your own JavaScript files to `message_coding/static/css`.
To load these in a Django template, add the following:

```html
{% load 'staticfiles' %} {# You will need this at the top of your file #}

{% block js %}
   {{ block.super }}
   <script src="{% static 'js/main.js' %}" type="text/javascript"></script>
{% endblock %}
```

The CoffeeScript compiler is also included, and you
can load CoffeeScript in the same way. Just use `type="text/coffeescript"` in
the script tag.


### Add Bower packages

It is recommended to use [Bower](http://bower.io/) to install third party
JavaScript and CSS packages instead of storing the files
in the repo directly.

From the main project folder, you can install
Bower packages like this:

```bash
$ bower install --save d3
```

This will download the relevant package into `message_coding/static/bower`
and add the package to the dependencies list in `bower.json`.

You will then need to add references to the appropriate files
in your templates or wherever they need to go.
