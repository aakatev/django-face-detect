# django-face-detect

Django back end with Python Face Recongition API configuired for easy heroku deployment

***

**Build with:**

* Django
* Python
* [Face Recognition](https://github.com/ageitgey/face_recognition)
* Pillow

***

## Documentation


### Simple examples

#### Detect face

<code>views.py</code>
```python
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        import face_recognition
        from PIL import Image, ImageDraw

        in_image = face_recognition.load_image_file(myfile)

        out_image = Image.fromarray(in_image)
        draw = ImageDraw.Draw(out_image)

        face_locations = face_recognition.face_locations(in_image)
    
        for (top, right, bottom, left) in face_locations:
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        out_image.save("./output.jpeg")

        image_data = open("./output.jpeg", "rb").read()
        return HttpResponse(image_data, content_type="image/jpeg")

    return render(request, 'src/html/image_upload.html')
```

<code>image_upload.html</code>
```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Simple File Upload</title>
  </head>
  <body>
    {% load static %}

    {% block content %}
      <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <input type="file" name="myfile">
        <button type="submit">Upload</button>
      </form>
      
    {% endblock %}
  </body>
</html>
```

#### Crop picture to avatar ()

<code>views.py</code>

```python
def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        import face_recognition
        from PIL import Image, ImageDraw

        in_image = face_recognition.load_image_file(myfile)

        out_image = Image.fromarray(in_image)
        out_image_w, out_image_h = out_image.size
    
        face_locations = face_recognition.face_locations(in_image)

        for (top, right, bottom, left) in face_locations:
            out_image=out_image.crop((left-(out_image_w*.1), top-(out_image_h*.17), right+(out_image_w*.1), bottom+(out_image_h*.2)))

        out_image.save("./output.jpeg")

        image_data = open("./output.jpeg", "rb").read()
        return HttpResponse(image_data, content_type="image/jpeg")

    return render(request, 'src/html/image_upload.html')
```



### Developer Section
***

**Installation**

Clone repository and cd inside downloaded folder

```
$ git clone https://github.com/aakatev/django-face-detect.git && cd django-face-detect
```

Configure virtual environment (In this example, I am using [Virtualenv](https://virtualenv.pypa.io/en/stable/), but you are free to do it your own way!)


First, check Python version installed

On Linux, one of the possible ways is to enter <code>$ /usr/bin/python</code> in your terminal and hit <code>Tab</code> key twice

This would show all the available vesrsions 

```
python             python3            python3.6m         python3m
python2            python3.6          python3.6m-config  python3m-config
python2.7          python3.6-config   python3-config     
```


Now, create environment with desired version of Python specified, as <code>--python=PY_VERSION</code> (Note: Django 2.x.. requres Python 3.x.. version!) 


```
$ virtualenv MY_ENV --python=python3.6
```


Activate your environment, and install Django and other dependencies

Note: If your environment name differs from <code>MY_ENV</code>, you would have to use <code>source YOUR_ENV_NAME/bin/activate</code> as first command

```
$ source activate &&  pip install -r requirements_dev.txt
```

***

**Development**


Start development server

```
(MY_ENV)$ python manage.py runserver
```

In case, you want to save your current dependencies in a text file 

```
(MY_ENV)$ pip freeze > requirements_dev.txt
```

***


**Deployment on Heroku**

Most of Django configuration has already been preset, and you only need to modify <code>setting.py</code> file to use deployment(heroku) settings instead of development one

```python
# Development settings
#from .development import *
# Deployment settings (heroku)
from .deployment import *
```

Now, create a new heroku app, <code> SECRET_KEY</code> to your app(use same names as in Python), and push project folder to heroku master. Don't forget to migrate database after you push! 