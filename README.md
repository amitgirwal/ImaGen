# ImaGen
ImaGen web application for photo effect and tools.

<br>
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

<br>

#### Built with
- Python 
- Django 
- Bootstrap
- Html
- CSS
- JavaScript
<br>
![home page]()
<br>

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
<br>

#### Features
- Coloize Image with Effact ex. Sepia, Red, Sky Blue, Dark Pink Lemon Yellow, Dark Grey.
- Convert Image Format to WEBP, PNG, JPG, JPEG
-  Flip the Image
    Flip Top To Bottom Popular*
    Flip Left To Right Most Used*
    Rotate 90 degree
    Rotate 180 degree
    Rotate 270 degree
    Transverse(Short to apply above effect)
- Reduce Quality reduce the image quality by custom value 1-99%
- QR Generator Generate any QR Code for any text or url
- Image 2 PDF Convert any image formate to pdf document
- Rotate an Image By Custom angle with expand options*
<br>

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
<br>

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

 