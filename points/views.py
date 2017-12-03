import requests

from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from points.forms import SignUpForm, TrashSubmissionForm, NewSuperUserForm
from points.models import Client, Rate, Trash_Submission

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            user.refresh_from_db()
            user.client.phone_number = form.cleaned_data.get('phone_number')
            user.save()

            #logging in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
        
    return render(request, 'points/signup.html', {'form': form})



def home(request):
    submissions = None

    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    if request.user.is_staff:
        return redirect(reverse('admin_users'))

    submissions = Trash_Submission.objects.filter(user=request.user.client)

    return render(request, 'points/home.html', {'submissions': submissions})




def admin_view_users(request):
    if not request.user.is_staff:
        return redirect(reverse('home'))

    users = User.objects.filter(is_staff=False)
    context = {
        'users': users,
    }
    return render(request, "points/admin_users.html", context)


def admin_trash_submission(request):
    client_id = "qkxfhtiy"
    client_secret = "lvllspnq"

    if request.user.is_staff == False:
        #create error message saying user is not allowed
        messages.add_message(request, messages.ERROR, "You are not authorized to access this area", extra_tags="alert alert-danger")

        return redirect(reverse('home'))
    
    if request.method == "POST":
        rate = Rate.objects.get(name="TC rate").value
        form = TrashSubmissionForm(request.POST)
        if form.is_valid():
            trash_submission = form.save(commit=False)
            trash_submission.earning = trash_submission.weight * rate
            trash_submission.user.wallet += trash_submission.earning
            trash_submission.save()
            trash_submission.user.save()
           
           #send sms to user 
            sms_from = 'TrashCash'
            number = str(trash_submission.user.phone_number)
            sms_to = '%2B233'+number 
            content = 'You have GHS{0} in your trashcash wallet. Redeem with a minimum of GHS10'.format(trash_submission.user.wallet)
            print(content)

            url = "https://api.hubtel.com/v1/messages/send?From={0}&To={1}&Content={2}&ClientId={3}&ClientSecret={4}".format(sms_from, sms_to, content, client_id, client_secret)
            response = requests.get(url, auth=(client_id, client_secret))
            print(response.json())
            return redirect(reverse('admin_users'))
    
    form = TrashSubmissionForm()
    return render(request, 'points/trash_submission.html', {'form':form})




def admin_new(request):
    if not request.user.is_superuser:
        messages.add_message(
            request, 
            message.ERROR, 
            "user [{0}] does not have permission to access this section. Only admins allowed.".format(request.user.username), 
            extra_tags="alert alert-danger"
        )
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = NewSuperUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.add_message(
                request, 
                messages.SUCCESS, 
                "Successfully created", 
                extra_tags="alert alert-success"
            )
            return redirect(revers('admin_users'))


    form = NewSuperUserForm()

    return render(request, "points/newsuperuser.html", {'form':form})
    
