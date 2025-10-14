from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from workers.models import Worker
from crops.models import Crops
from buyier.models import Buyier
from chat.models import Chat
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


# views.py
from django.http import StreamingHttpResponse
from django.shortcuts import render
from .a import FaceRecognitionSystem  # Your existing class


# views.py
from django.http import StreamingHttpResponse
from django.shortcuts import render
from .a import VideoCamera
import time
import threading



def login_signup(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "signup":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            role = request.POST.get('role')

            if password != confirm_password:
                return HttpResponse("Password and Confirm Password do not match")

            if User.objects.filter(username=name).exists():
                return HttpResponse("Username already exists")

            new_user = User.objects.create_superuser(username=name, email=email, password=password)
            new_user.first_name = phone
            new_user.last_name = role
            new_user.save()
            return redirect('login_signup')

        elif form_type == "login":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # or redirect wherever needed
            else:
                return HttpResponse("Invalid username or password")

    return render(request, "login_signup.html")



def logout_page(request):   
    logout(request)
    return redirect('logout_page')




def header(request):
    user = request.user
    phone = user.first_name    
    role = user.last_name 
    return render(request, "header.html", {'user': user,'phone':phone,'role':role})



@login_required(login_url='login_signup')
def sellCrop(request):
    if request.method == "POST" and 'delete_id' in request.POST:
        crop_id = request.POST.get('delete_id')
        crop = get_object_or_404(Crops, id=crop_id, user=request.user)
        crop.delete()
        return redirect('sell_crop')  # refresh the page after deletion

    user = request.user
    phone = user.first_name    
    role = user.last_name 
    
    crop_image =''
    farmer_name = ''
    farmer_age = ''
    crop_name = ''
    crop_dryness = ''
    crop_bread = ''
    crop_type = ''
    crop_description = ''
    crop_quantity = ''
    expected_price = ''
    farming_location = ''
    croping_duration = ''

    data = {}
    try:
        if request.method=="POST":
            
            
            crop_image =  request.FILES.get('crop_image')
            farmer_name = request.POST.get('farmer_name')
            farmer_age = request.POST.get('farmer_age')
            crop_name = request.POST.get('crop_name')
            crop_dryness = request.POST.get('crop_dryness')
            crop_bread = request.POST.get('crop_bread')
            crop_type = request.POST.get('crop_type')
            crop_description = request.POST.get('crop_description')
            crop_quantity = request.POST.get('crop_quantity')
            expected_price = request.POST.get('expected_price')
            farming_location = request.POST.get('farming_location')
            croping_duration = request.POST.get('croping_duration')
           
            
            crop_data = Crops(
                user=request.user,
                crop_image=crop_image,
                farmer_name=farmer_name,
                farmer_age=farmer_age,
                crop_name=crop_name,
                crop_dryness=crop_dryness,
                crop_bread=crop_bread,
                crop_type=crop_type,
                crop_description=crop_description,
                crop_quantity=crop_quantity,
                expected_price=expected_price,
                farming_location=farming_location,
                croping_duration=croping_duration,
            )
            crop_data.save()
            
            return redirect('sell_crop')
        
        data = { 
            "crop_image": crop_image,
            "farmer_name": farmer_name,
            "farmer_age": farmer_age,
            "crop_name": crop_name,
            "crop_dryness": crop_dryness,
            "crop_bread": crop_bread,
            "crop_type": crop_type,
            "crop_description": crop_description,
            "crop_quantity": crop_quantity,
            "expected_price": expected_price,
            "farming_location": farming_location,
            "croping_duration": croping_duration,
        }
        
        data = Crops.objects.all()
        
    except:
        pass
    data = Crops.objects.filter(user=request.user)
    return render(request, "sellCrop.html",{'data':data,'user': user,'phone':phone,'role':role})





@login_required(login_url='login_signup')
def buyier(request):
    crops = Crops.objects.all()
    myupload = Crops.objects.all()
  
    paginator = Paginator(myupload,6)
   
    page_number = request.GET.get('page')
    crops = paginator.get_page(page_number)
    user = request.user
    phone = user.first_name    
    role = user.last_name

  # default crop list

    if request.method == "POST":
        # Handle crop search
        search = request.POST.get('search')
        if search!=None:
            crops = Crops.objects.filter(crop_name__icontains=search)

        # Handle form submission
        buyer_name = request.POST.get('buyer_name')
        buyer_address = request.POST.get('buyer_address')
        purchase_quantity = request.POST.get('purchase_quantity')
        negotiation_price = request.POST.get('negotiation_price')
        crop_name = request.POST.get('crop_name')
        farmer_name = request.POST.get('farmer_name')
        buyer_phone = request.POST.get('buyer_phone')

        if buyer_name and crop_name:
            buyier_data = Buyier(
                buyer_name=buyer_name,
                buyer_address=buyer_address,
                purchase_quantity=purchase_quantity,
                negotiation_price=negotiation_price,
                crop_name=crop_name,
                farmer_name=farmer_name,
                buyer_phone=buyer_phone,
            )
            buyier_data.save()
            return redirect('buyier')
    # Show all purchase requests
    all_buyier_requests = Buyier.objects.all()

    return render(request, "buyier.html", {
        'data': crops,
        'buyier_data': all_buyier_requests,
        'user': user,
        'phone': phone,
        'role': role
    })
    


@login_required(login_url='login_signup')
def farmMonitiring(request):
    
    user = request.user
    phone = user.first_name    
    role = user.last_name 
    return render(request,"farmMonitiring.html",{'user': user,'phone':phone,'role':role})


@login_required(login_url='login_signup')
def storage_management(request):
    user = request.user
    phone = user.first_name    
    role = user.last_name 
    buyers= Buyier.objects.filter(farmer_name=request.user.username)

    return render(request, 'storage_management.html', {'buyers': buyers,'user': user,'phone':phone,'role':role})

@login_required(login_url='login_signup')
def profit_loss(request):
    user = request.user
    phone = user.first_name    
    role = user.last_name 
    buyers= Buyier.objects.filter(farmer_name=request.user.username)

    return render(request, 'profit_loss.html', {'buyers': buyers,'user': user,'phone':phone,'role':role})



@login_required(login_url='login_signup')
def to_do_list(request):
    user = request.user
    phone = user.first_name    
    role = user.last_name 
    buyers= Buyier.objects.filter(farmer_name=request.user.username)

    return render(request, 'to_do_list.html', {'buyers': buyers,'user': user,'phone':phone,'role':role})



@login_required(login_url='login_signup')
def quantity_tracker(request):
    user = request.user
    phone = user.first_name    
    role = user.last_name 
    buyers= Buyier.objects.filter(farmer_name=request.user.username)

    return render(request, 'quantity_tracker.html', {'buyers': buyers,'user': user,'phone':phone,'role':role})










@login_required(login_url='login_signup')
def storage(request):
    if request.method == 'POST':
        delete_id = request.POST.get('delete_id')
        if delete_id:
            try:
                buyer = Buyier.objects.get(id=delete_id)
                buyer.delete()
            except Buyier.DoesNotExist:
                pass  # Optionally log or notify that buyer wasn't found
        return redirect('storage')  # Replace with your URL name

    buyers = Buyier.objects.all().order_by('-id')
    user = request.user
    phone = user.first_name    
    role = user.last_name 
    buyers= Buyier.objects.filter(farmer_name=request.user.username)

    return render(request, 'storage.html', {'buyers': buyers,'user': user,'phone':phone,'role':role})







camera_instance = VideoCamera()
camera_lock = threading.Lock()  # 🚨 Add lock

def gen(camera):
    while True:
        with camera_lock:
            frame, _ = camera.get_frame_and_objects()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            time.sleep(0.1)

def video_feed(request):
    return StreamingHttpResponse(gen(camera_instance),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def object_names_stream(request):
    def event_stream():
        while True:
            with camera_lock:
                _, objects = camera_instance.get_frame_and_objects()
            
            print("DEBUG >>> Objects detected:", objects)  # 👈 Add this
            if set(objects) & {'PERSON', 'COW'}:
                send_test_email()
                print("Alert Sent:", objects)

            yield f"data: {','.join(objects)}\n\n"
            time.sleep(1)

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


from django.core.mail import send_mail
from django.conf import settings

def send_test_email():
    subject = "🚨⚠️🔔 Security Warning: Unusual Activity (Animal/Theaf) Spotted on Your Farm 🚜🐾"
    message = "⚠️ Immediate attention required! 🚨 Visit your farm or check the camera feed now. 🔍👀"

    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['skilldevelopnment@gmail.com']  # Change to your target email

    send_mail(subject, message, from_email, recipient_list)





# # import cv2

# # video = cv2.VideoCapture("http://192.168.114.60:8080/video")

# # while video.isOpened():
# #     r, frame = video.read()
# #     frame = cv2.resize(frame,(500,500 ))
# #     if r==True:
# #         cv2.imshow("frame",frame)
# #         if cv2.waitKey(1) & 0xFF == ord("a"):
# #             break
# #     else:
# #         break
# # video.release()
# # cv2.destroyAllWindows()




# from .a import FaceRecognitionSystem

# frs = FaceRecognitionSystem()
# frs.capture_faces("aryan", "http://192.168.6.199:8080/video")  # Capture faces from a video
# frs.train_model()                     # Train the model
# frs.recognize_and_mark_attendance("http://192.168.6.199:8080/video")  # Run recognition





frs = FaceRecognitionSystem()
frs.train_model()  # Make sure model is trained

@login_required
def home(request):
    user = request.user
    phone = user.first_name    
    role = user.last_name 

    if request.method == "POST":
        # Handle delete
        if 'delete_id' in request.POST:
            chat_id = request.POST.get('delete_id')
            chat_obj = get_object_or_404(Chat, id=chat_id)
            if chat_obj.user == request.user:
                chat_obj.delete()
            return redirect('home')

        # Handle chat creation
        chat_text = request.POST.get('chat')
        if chat_text:
            Chat.objects.create(user=request.user, chat=chat_text)
            return redirect('home')  # ✅ Redirect after saving

    # GET request (or after redirect)
    chats = Chat.objects.all().order_by('-created_at')
    return render(request, "home.html", {
        'user': user,
        'phone': phone,
        'role': role,
        'chats': chats
    })


@login_required
def index(request):
    user = request.user
    phone = user.first_name    
    role = user.last_name 

    return render(request, "index.html", {
        'user': user,
        'phone': phone,
        'role': role
    })



@login_required
def workers(request):
    # Handle form submission to capture new user's face
    if request.GET.get('start') == 'true':
        new = request.GET.get('new')
        if(new!=''):

      
            
            video_url = "http://192.168.58.164:8080/video"
            frs.capture_faces(new, video_url)  # Capture images for new person
            frs.train_model()  # Retrain face recognizer with all data
        return redirect('workers')
    # Render page whether form is submitted or not
  
    if request.method == "POST" and 'delete_id' in request.POST:
        worker_id = request.POST.get('delete_id')
        crop = get_object_or_404(Worker, id=worker_id, user=request.user)
        crop.delete()
        return redirect('workers')  # refresh the page after deletion

    user = request.user
    phone = user.first_name    
    role = user.last_name 
    

    worker_name=''
    worker_age=''
    working_job=''
    working_duration=''
    worker_phone=''
    worker_payment=''
    worker_address=''
    worker_image=''

    data = {}
    try:
        if request.method=="POST":
            worker_name = request.POST.get('worker_name')
            worker_age = request.POST.get('worker_age')
            working_job = request.POST.get('working_job')
            working_duration = request.POST.get('working_duration')
            worker_phone = request.POST.get('worker_phone')
            worker_payment = request.POST.get('worker_payment')
            worker_address = request.POST.get('worker_address')
            worker_image = request.FILES.get('worker_image')

            worker_data =Worker(user=request.user,worker_name=worker_name,worker_age=worker_age,working_job=working_job,working_duration=working_duration,worker_phone=worker_phone,worker_payment=worker_payment,worker_address=worker_address,worker_image=worker_image)
            worker_data.save()
            return redirect('workers')
        data ={"worker_name":worker_name,"worker_age":worker_age,"working_job":working_job,"working_duration":working_duration,"worker_phone":worker_phone,"worker_payment":worker_payment,"worker_address":worker_address,"worker_image":worker_image}
    except:
        pass

    data = Worker.objects.all()
    data = Worker.objects.filter(user=request.user)
    return render(request,"workers.html",{'data':data,'user': user,'phone':phone,'role':role})







def gen_frames():  # Generator to stream video frame by frame
    import cv2
    cap = cv2.VideoCapture("http://192.168.58.164:8080/video")

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Convert to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = frs.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                roi_resized = cv2.resize(roi, frs.face_size)

                label, confidence = frs.recognizer.predict(roi_resized)
                name = frs.label_map.get(label, "Unknown")

                if confidence < 65:
                    frs.mark_attendance(name)
                else:
                    name = "Unknown"

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame, f"{name} {int(confidence)}", (x, y-10),
                            cv2.FONT_HERSHEY_COMPLEX, 3, (0,0, 255), 2)

            # Encode to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')



