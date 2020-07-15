from django.shortcuts import render,HttpResponse
from home.models import Contact
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, 'home/home.html')
 

def contact(request):
    
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        
        if len(name)<3 or len(email)<5 or len(phone)<10 or len(content)<5:
            messages.error(request,"please fill the form correctly")

        else:
          contact = Contact(name=name, email=email, phone=phone, description=content)
          contact.save()
          messages.success(request,"your form has been submitted successfully")

       
    return render(request, 'home/contact.html')
  

def about(request):
    messages.success(request,'this is about')
      
    return render(request, 'home/about.html')
     