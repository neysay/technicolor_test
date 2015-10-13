# technicolor_test

The following instruction manual is mostly copied from 
https://github.com/kirpit/django-sample-app

The sample application comes with:
* [Twitter Bootstrap](http://getbootstrap.com/) v3.3.5

And its current `requirements.txt` file is:

```
Django==1.8.2
django-crispy-forms==1.4.0
wsgiref==0.1.2
```

## Installation

### 1. Download
Now, you need the *JobSnap* project files in your workspace:

    $ cd /path/to/your/workspace
    $ git clone https://github.com/neysay/technicolor_test.git technicolor_test
    $ cd technicolor_test
    $ virtualenv env
    $ source env/bin/activate

### 2. Requirements
Right there, you will find the *requirements.txt* file that has all the great debugging tools, django helpers and some other cool stuff. To install them, simply type:

`$ pip install -r requirements.txt`

### 3. Tweaks

#### SECRET_KEY
If you want you're own secret key:
Go to <http://www.miniwebtool.com/django-secret-key-generator/>, create your secret key, copy it. Open your `technicolor_test/settings.py`, find `SECRET_KEY` line, paste your secret key.


#### Initialize the database
First set the database engine (PostgreSQL, MySQL, etc..) in your settings files; `technicolor_test/settings.py`. Of course, remember to install necessary database driver for your engine. Then define your credentials as well. Time to finish it up:

`python manage.py migrate`

### Ready? Go!
```
$ python manage.py runserver
```


## Explanations
```
    *Django was chosen because it provided a good framework 
    to abstract model/view/controller components of the project. 

    *Handles forms convienantly once you know a few gotchas 
    about how django's form validation process

    *Allowed me to make use of my python knowledge 
    (I haven't done a terrible amount of javascript coding yet)

    *Has built in modules for Users and login authentication

    *Built in ORM to handle queries regardless of database chosen.  
    (Although that abstraction is not so great for the 'group by' case, 
    as I found out while working on this)
    
    *Choose to add bootstrap with crispy-forms for nice form validation
    handling.  Added bonus makes webpage mobile responsive for free.
```


### Things to still Do:
     Add Pagination to search tables -> https://docs.djangoproject.com/en/1.8/topics/pagination/
     Add searching of file system
     Add status checking of all dependent components -> https://docs.djangoproject.com/en/1.8/topics/testing/tools/


### Examples
```
In general you can trigger everything interactively through the webpage, however
if you want to search by using a url endpoint directly you can as such:

http://127.0.0.1:8000/?&searchBy=state&searchSelect=NV&groupBy=city&search=Search

This will fill in the form with the specified data and submit it.
In this case it would search by State , selectedState would be Nevada (NV) and then group them by city

*if you leave 'selectedState' blank (i.e &selectedState=&groupBy=city)  Then it will default to select ALL users and then group by city
```


