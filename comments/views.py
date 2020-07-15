from django.shortcuts import render

# Create your views here.
def comment_delete(request,id):
    obj=get_obj_or_404(Comments,id=id)
    context={
        "object":obj
    }

    return render(request,"blog/confirm_delete.html",context)