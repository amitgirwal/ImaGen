# ImaGen
ImaGen web application for photo effect and tools.

 
#### Quick Run Project
```bash
cd backend
.\venv\Scripts\activate
cd ImaGen
python manage.py runserver

python manage.py makemigrations
python manage.py migrate

http://127.0.0.1:8000/

cd backend
pip install -r requirements.txt
```

 

#### Built with
- Python 
- Django 
- Bootstrap
- Html
- CSS
- JavaScript
 


#### Installation & Setup
- Install virtual env
```bash
python -m pip install --user virtualenv
python -m venv venv
```

- Change the directory for backend
```bash
cd backend
```
- Activate virtual env
```bash
.\venv\Scripts\activate
```
- Install packages
```bash
pip install -r requirements.txt
```

- Goto project folder
```bash
cd ImaGen
```

- Database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

- Run application
```bash
python manage.py runserver
```
- Hit url in browser 
```bash
http://127.0.0.1:8000/
```
 

#### Features
Login and Signup page `design + logic`  
Home Page design completed `navbar + hero sections + subscribe section + footer`  
After `signup active account link` send to the email for verification (Done)
Coloize Image Filter (Done)
        - Sepia
        - Red
        - Sky Blue
        - Dark Pink
        - Lemon Yellow
 

Convert Image Formats (Done)
	- Image to WEBP
	- Image to PNG
	- Image to JPG
	- Image to JPEG

Image Flip (Done)
	- Flip Top To Bottom Popular
	- Flip Left To Right Most Used
	- Rotate 90 degree
	- Rotate 180 degree
	- Rotate 270 degree
	- Transverse

Reduce Image Quality (Done)
	- Reduce image quality to a custom value range from 99 to 1 download it

QR Code Generator (Done)
	- Generator QR Code from any custom text and download it

Image To PDF (Done)
	- Convert Any image format to a PDF document and view, download it

Rotate Image (Done)
	- Rotate Any Image to a custom angle and download it
	
Text utils (Done)
	- UPPER CASE
	- lower case
	- Capitalize Case
	- iNVERSE cASE
	- AlTeRnAtE cAsE
	- Copy Text
	- Clear
	- Sample
 

#### Coming Soon
Articles, Pages, Categories, Tags(Add, Delete, Edit), etc.
Articles and pages support Markdown and highlighting.
Articles support full-text search.
Complete comment feature, include posting reply comment and email notification. Markdown supporting.
Sidebar feature: new articles, most readings, tags, etc.
OAuth Login supported, including Google, GitHub, Facebook, Weibo, QQ.
Memcache supported, with cache auto refresh.
Simple SEO Features, notify Google  when there was a new article or other things.
Simple picture bed feature integrated.
django-compressor integrated, auto-compressed css, js.
Website exception email notification. When there is an unhandle exception, system will send an email notification.
Wechat official account feature integrated. Now, you can use wechat official account to manage your VPS.


 



#### Resources
- [Django](https://www.djangoproject.com/)
- [Django Crispy Forms](https://pypi.org/project/crispy-bootstrap5/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
- [JQuery](https://cdnjs.com/libraries/jquery)
- [Font Awesome](https://cdnjs.com/libraries/font-awesome)
- [Font Awesome Icon](https://fontawesome.com/search?o=r&m=free&s=solid)
- [Image Undraw](https://undraw.co/search)
- [Gradient Color Bootstrap](https://mdbootstrap.com/docs/b4/jquery/css/gradients/)
- [Virutal Env Doc](https://virtualenv.pypa.io/en/latest/installation.html)
- [Django Docs](https://docs.djangoproject.com/en/4.1/intro/tutorial01/)
- [TinyMCE](https://pypi.org/project/django-tinymce/)

 