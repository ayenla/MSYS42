from django.shortcuts import render

# Create your views here.
def create_child_profile(request):
    return render(request,'msys42app/create_cp.html')