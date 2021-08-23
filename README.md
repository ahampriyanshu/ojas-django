# Ojas Django

## Setup

* Activate your virtual env

```
git clone https://github.com/ahampriyanshu/ojas-django.git
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py collectstatic
python3 manage.py runserver
```

* [Click here](https://www.favicon-generator.org/) and update the favicons in `staticfiles/img` 

* Go to the admin panel (_default url is domain/admin_)
    * Create new admin
    * Create new author
    * Update site title and desc

* Open settings.py
    * Set ``DEBUG = False`` 
    * Update 
        - ``SECRET_KEY``, ``ALLOWED_HOSTS``
        - ``LANGUAGE_CODE``, ``LOGO_URL``, ``TIME_ZONE``
        - ``SERVER_EMAIL``, ``EMAIL_HOST_PASSWORD``

## Roadmap

* [x] Tagging funtionality instead of static categories/sections
* [x] Installable PWA with offline support
* [x] Custom error pages
* [x] Responsive for all (sm, md, lg, xl)
* [x] Markdown and RichText Support
* [x] WYSIWYG Editor
* [x] SEO freindly URL
* [x] RSS and Atom Feed 
* [x] Rest API and sitemap
* [x] Unique visitor and views counter
* [x] Replaced datetime and time with timezone
* [x] Subscription newsletter with confirmation and unsubscription
* [x] HTML templates for emails
* [x] Simpler frontend
* [x] Dark Mode
* [x] Better commenting system with captcha verification
* [x] Make all the important details dynamic (blog title,desc,author,keywords,contacts)
* [x] Live preview of post in admin panel
* [x] Additional settings for author at user-end
* [x] Improve support for extra large images and code snippets
* [x] Export data to csv/xlsx
* [x] Better logging system

## Attribution

* [django](https://www.djangoproject.com/)
* [tailwindcss](https://tailwindcss.com/docs/text-color)
* [ckeditor](https://ckeditor.com/)
* [alpinejs](https://github.com/alpinejs/alpine)
* [flaticon](http://www.flaticon.com/)
* [pythonanywhere](https://www.pythonanywhere.com/)

## Resources

* [https://www.packtpub.com/product/django-by-example/9781784391911](https://www.packtpub.com/product/django-by-example/9781784391911)
* [https://www.dyspatch.io/resources/templates/](https://www.dyspatch.io/resources/templates/)
* [https://docs.djangoproject.com/en/3.2/topics/logging/#default-logging-configuration](https://docs.djangoproject.com/en/3.2/topics/logging/#default-logging-configuration)
* [https://www.jujens.eu/posts/en/2020/Feb/29/django-pwa/](https://www.jujens.eu/posts/en/2020/Feb/29/django-pwa/)
* [https://books.agiliq.com/](https://books.agiliq.com/)
* [http://twitter.com/khatabwedaa](http://twitter.com/khatabwedaa)
* [https://www.youtube.com/watch?v=Y4c4ickks2A](https://www.youtube.com/watch?v=Y4c4ickks2A)
* [https://pythoncircle.com/post/657/adding-email-subscription-feature-in-django-application/](https://pythoncircle.com/post/657/adding-email-subscription-feature-in-django-application/)
* [https://stackoverflow.com/questions/61848207/sending-email-notification-in-django](https://stackoverflow.com/questions/61848207/sending-email-notification-in-django)
* [http://www.expertphp.in/article/django-how-to-send-text-and-html-emails-with-dynamic-data-in-python](http://www.expertphp.in/article/django-how-to-send-text-and-html-emails-with-dynamic-data-in-python#:~:text=Email%20Configuration%20in%20Django&text=You%20can%20also%20configure%20the,django-smtp-ssl%20package.&text=In%20order%20to%20use%20the,template)