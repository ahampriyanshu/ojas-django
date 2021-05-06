# Ojas

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](track-covid-react.netlify.app)
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://ahampriyanshu.pythonanywhere.com)
[![size](https://img.shields.io/github/repo-size/ahampriyanshu/ojas?style=flat-square)](https://ahampriyanshu.pythonanywhere.com)
[![Website status](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://ahampriyanshu.pythonanywhere.com)

<p align="center" >
<img src="https://user-images.githubusercontent.com/54521023/100444973-56a74400-30d2-11eb-89d5-3408e760944b.png" width="100%">
<br><br>
<h2 align="center"> Lighthouse Audit </h2>
<img src="https://user-images.githubusercontent.com/54521023/100444975-57d87100-30d2-11eb-908b-9ba1de033192.png" width="40%">
</p>


* [Home](https://ahampriyanshu.pythonanywhere.com/admin)
* [Admin Panel](https://ahampriyanshu.pythonanywhere.com/admin)
* [Api](https://ahampriyanshu.pythonanywhere.com/api)
* [Sitemap](https://ahampriyanshu.pythonanywhere.com/sitemap.xml)
* [RSS Feed](https://ahampriyanshu.pythonanywhere.com/feed)
* [User Agent](https://ahampriyanshu.pythonanywhere.com/me)

## Home
![home](https://user-images.githubusercontent.com/54521023/100063392-2c961d80-2e57-11eb-8840-2b4320b49f70.png)

## Blog
![blog](https://user-images.githubusercontent.com/54521023/100063377-27d16980-2e57-11eb-862f-c9469967a182.png)

## Author
![author](https://user-images.githubusercontent.com/54521023/100063366-23a54c00-2e57-11eb-8d20-c31c0bf3d4ec.png)

## Comment
![comment](https://user-images.githubusercontent.com/54521023/100063381-2a33c380-2e57-11eb-9506-574d16b9c5ad.png)

## Search Result
![Screenshot from 2020-11-27 16-51-04](https://user-images.githubusercontent.com/54521023/100444995-5eff7f00-30d2-11eb-967f-eb1467cd4cca.png)

## User-Agent
![Screenshot from 2020-11-27 16-49-58](https://user-images.githubusercontent.com/54521023/100445024-6de63180-30d2-11eb-9921-b384a01a73ca.png)


## Installation

```bash

git clone https://github.com/ahampriyanshu/ojas.git
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver

```

## Deployment

* Set ``DEBUG = False`` 
* Change the ``SECRET_KEY``
* Run ``python3 manage.py collectstatic``

## Dependencies

| Dependency | Version |
| --- | --- | 
| Django | 3.2.4 | 
| django-ckeditor | 6.0.0 |
| django-crispy-forms | 1.10.0  |
| django-embed-video | 1.3.3  |
| django-richtextfield | 1.6  |
| django-taggit | 1.3.0  |
| django-user-agents | 0.4.0  |
| django-user-visit | 0.4.1  |
| djangorestframework | 3.12.2  |
| Markdown | 3.3.3  |
| Pillow | 8.0.1  | 
| Tailwind | 2.0.4  |

## Special thanks to
.
* [FlatIcon](http://www.flaticon.com/) for all the wonderfull svg icons.
* [PythonAnywhere](https://www.pythonanywhere.com/) for hosting this project.

## 

- [x] Tagging funtionality instead of static categories/sections
- [x] Installable
- [x] Cache and offline support with PWA
- [x] Custom error pages
- [x] Responsive
- [x] Markdown support
- [x] RichText Support
- [x] WYSIWYG Editor
- [x] Sitemap
- [x] SEO freindly URL
- [x] RSS Feed 
- [x] Rest_framework
- [x] Unique visitor and generic views counter
- [x] Parsing User-agent
- [ ] Subscription newsletter
- [ ] More natural frontend
- [ ] Dark Mode
- [ ] More ajax
- [ ] Better lazy loading
- [ ] Better comment system
- [ ] Migrate to Postgre
