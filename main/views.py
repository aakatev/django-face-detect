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
        out_image_w, out_image_h = out_image.size
    
        face_locations = face_recognition.face_locations(in_image)
    

        for (top, right, bottom, left) in face_locations:
            out_image=out_image.crop((left-(out_image_w*.1), top-(out_image_h*.17), right+(out_image_w*.1), bottom+(out_image_h*.2)))

        out_image.save("./output.jpeg")

        image_data = open("./output.jpeg", "rb").read()
        return HttpResponse(image_data, content_type="image/jpeg")

    return render(request, 'src/html/image_upload.html')