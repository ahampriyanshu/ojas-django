# Ojas

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](track-covid-react.netlify.app)
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://ahampriyanshu.pythonanywhere.com)
[![size](https://img.shields.io/github/repo-size/ahampriyanshu/ojas?style=flat-square)](https://ahampriyanshu.pythonanywhere.com)
[![Website status](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://ahampriyanshu.pythonanywhere.com)

## Dependencies

* [Django](https://www.djangoproject.com/)
* [Tailwind](https://tailwindcss.com/docs/text-color)
* [CKEditor](https://ckeditor.com/)
* [AlpineJS](https://github.com/alpinejs/alpine)
* [Jquery](https://jquery.com/)

## Setup

* Activate your virtual env

```bash
git clone https://github.com/ahampriyanshu/ojas.git
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic
python3 manage.py runserver
```

* Update all the favicons in  `staticfiles/img`

* Go to the admin panel(_default url is domain/admin_)
    * Create an admin record
    * Create a new author

* Open settings.py
    * Set ``DEBUG = False`` 
    * Update ``SECRET_KEY``, ``LOGO_URL``, ``ALLOWED_HOSTS``,
    * Update language and timezone setting : ``LANGUAGE_CODE``, ``TIME_ZONE``
    * Update SMTP setting : ``EMAIL_HOST_PASSWORD``, ``EMAIL_HOST_USER``, ``DEFAULT_FROM_EMAIL``

## Roadmap

* [x] Tagging funtionality instead of static categories/sections
* [x] Installable PWA with offline support
* [x] Custom error pages
* [x] Responsive for all (sm, md, lg, xl)
* [x] Markdown support
* [x] RichText Support
* [x] WYSIWYG Editor
* [x] Sitemap
* [x] SEO freindly URL
* [x] RSS Feed 
* [x] Rest API
* [x] Unique visitor and views counter (which doesn't rely on ctrl + r)
* [x] Parsing User Agent
* [x] replace datetime and time with timezone
* [x] Subscription newsletter
* [x] HTML templates for emails
* [x] Simpler frontend
* [x] Dark Mode which respects both user's and os's preferences
* [x] Better commenting system with captcha verification
* [x] Make all the important details dynamic (blog title,desc,author,keywords,contacts)
* [ ] Migrate to Postgre
* [ ] More robust ServiceWorker
* [ ] Get rid of alpine-js
* [ ] Provide a better POST API
* [x] Provide a better GET API
* [x] Live preview of post in Admin panel
* [x] Additional options for author at user-end
* [ ] Improve support for images and code snippets
* [ ] Better Admin Panel
* [x] A method to export the db data to a csv/xls file.
* [ ] Build a more powerfull logger

## Attribution

* [https://www.packtpub.com/product/django-by-example/9781784391911](https://www.packtpub.com/product/django-by-example/9781784391911)
* [https://www.dyspatch.io/resources/templates/](https://www.dyspatch.io/resources/templates/)
* [https://docs.djangoproject.com/en/3.2/topics/logging/#default-logging-configuration](https://docs.djangoproject.com/en/3.2/topics/logging/#default-logging-configuration)
* [https://www.jujens.eu/posts/en/2020/Feb/29/django-pwa/](https://www.jujens.eu/posts/en/2020/Feb/29/django-pwa/)
* [https://books.agiliq.com/](https://books.agiliq.com/)
* [http://twitter.com/khatabwedaa](http://twitter.com/khatabwedaa)
* [https://www.youtube.com/watch?v=Y4c4ickks2A](https://www.youtube.com/watch?v=Y4c4ickks2A)
* [https://pythoncircle.com/post/657/adding-email-subscription-feature-in-django-application/](https://pythoncircle.com/post/657/adding-email-subscription-feature-in-django-application/)
* [https://stackoverflow.com/questions/61848207/sending-email-notification-in-django](https://stackoverflow.com/questions/61848207/sending-email-notification-in-django)
* [http://www.expertphp.in/article/django-how-to-send-text-and-html-emails-with-dynamic-data-in-python](http://www.expertphp.in/article/django-how-to-send-text-and-html-emails-with-dynamic-data-in-python#:~:text=Email%20Configuration%20in%20Django&text=You%20can%20also%20configure%20the,django-smtp-ssl%20package.&text=In%20order%20to%20use%20the,template.)

## Special thanks to

* [FlatIcon](http://www.flaticon.com/) for all the wonderfull svg icons.
* [PythonAnywhere](https://www.pythonanywhere.com/) for hosting this project.
