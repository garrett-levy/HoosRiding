from django.shortcuts import render
from django.contrib.auth.models import User

from user_profile.models import Rider
from find.models import Posting
from django.http import HttpResponseRedirect
from datetime import datetime as dt

from django.core.files.storage import default_storage

#method called
def calculate_rating(current_user): ###
    rating_array = current_user.ratings_list.split(",")  # average of rating_list
    total_rating = 0
    count = 0

    for i in range(0, len(rating_array)):
        if rating_array[i] != '':
            count += 1
            total_rating += int(rating_array[i])
    if count > 0:
        new_rating = round(total_rating / count, 2)
        current_user.rating = new_rating
    else:
        current_user.rating = 0
    current_user.save()

    # user_matches = Posting.objects.filter(driver_id=id)
    # current_user = user_matches[0]
    # current_user.rating = new_rating
    # current_user.save()

    return current_user.rating

def updateRating(request):
    # if posting "ratable by" contains rider's username, then don't update rating
    id = request.user
    user_matches = Rider.objects.filter(username=id)
    current_user = str(user_matches[0])
    posting = Posting.objects.filter(posting_id=request.GET['post_id'])[0]
    ratable = posting.ratable_by
    posting.ratable_by = ratable[:ratable.index(current_user)] + ratable[ratable.index(current_user) + len(current_user):]
    posting.save()


    # id is the driver_id and this fins the rider with the same id and updates rating
    rider_to_rate = Rider.objects.filter(username=request.GET['id'])
    rider_to_rate = rider_to_rate[0]
    rider_to_rate.ratings_list = rider_to_rate.ratings_list + ", " + str(request.GET['rating'])
    rider_to_rate.rating = calculate_rating(rider_to_rate)
    rider_to_rate.save()

    return profile(request)

# performs arithmetic to see if ride has already occurred
def alreadyOccured(Posting):
    return True

# Create your views here.
def profile(request):
    current_user = handleForm(request)  # get and update current user based on form data
    print (current_user.name)
    allRides = {}
    ridesPassengerIds = str(Rider.objects.filter(username=request.user)[0].rides_passenger).split(",")
    for ride in ridesPassengerIds:
        query = Posting.objects.filter(posting_id=ride)
        if query.count() > 0:
            allRides[query[0]] = 'accepted'

    ridesPendingIds = str(Rider.objects.filter(username=request.user)[0].rides_pending).split(",")
    for ride in ridesPendingIds:
        query = Posting.objects.filter(posting_id=ride)
        if query.count() > 0:
            allRides[query[0]] = 'pending'

    ridesDeclinedIds = str(Rider.objects.filter(username=request.user)[0].rides_declined).split(",")
    for ride in ridesDeclinedIds:
        query = Posting.objects.filter(posting_id=ride)
        if query.count() > 0:
            allRides[query[0]] = 'declined'

    # calculates the rating for the current user to be displayed on profile page
    id = request.user
    user_matches = Rider.objects.filter(username=id)
    current_user = user_matches[0]
    rating = calculate_rating(current_user)  ###

    return render(request, 'user_profile/profile.html', {'title': 'Profile', 'id': id, 'current_user': current_user,
                                                         'allRides': allRides, 'viewingPassenger': True, 'rating':rating})

def handleForm(request):
    id = request.user
    user_matches = Rider.objects.filter(username=id)
    current_user = user_matches[0]
    name = request.user.first_name + ' ' + request.user.last_name
    current_user.name = name;
    current_user.save()
    #check if modal form has been filled out yet
    if 'image' in request.FILES:
        current_user.image = request.FILES['image']
        current_user.save()
    if request.POST.get('license_plate') is not None:
        current_user.license_plate = request.POST.get('license_plate')
        current_user.save()
    if request.POST.get('cellphone') is not None:
        current_user.cellphone = request.POST.get('cellphone')
        current_user.save()
    if request.POST.get('car_type') is not None:
        current_user.car_type = request.POST.get('car_type')
        current_user.save()
    return current_user




#method called when driver accepts or declines a new passenger
def respondToDriverRequest(request):

    postingObject = Posting.objects.filter(posting_id=request.GET['id'])[0]
    passenger = Rider.objects.filter(username=request.GET['rider'])[0]

    #if passenger is accepted
    if(request.GET['status'] == "accept"):
        postingObject.riders_riding += passenger.username + "," #add to riders riding
        postingObject.ratable_by += passenger.username + ","
        print('got here yooo')
        postingObject.num_passengers -= 1
        passenger.rides_passenger += request.GET['id'] + "," #update rider's info to save is riding
        passenger.save()
    else:
        passenger.rides_declined += request.GET['id'] + "," # update rider's info, ride declined
        passenger.save()

    #remove from posting
    requested = postingObject.riders_requested
    postingObject.riders_requested = requested[:requested.index(passenger.username)] + requested[requested.index(passenger.username)+len(passenger.username):]
    postingObject.save()

    #remove from passenger
    pending = passenger.rides_pending
    passenger.rides_pending = pending[:pending.index(request.GET['id'])] + pending[pending.index(request.GET['id']) + len(request.GET['id']):]
    # print("passenger pending: " + passenger.rides_pending)
    passenger.save()

    return switchToDriverView(request)

def switchToDriverView(request):
    id = request.user
    current_user = handleForm(request)
    ridesDrivingIds = str(Rider.objects.filter(username=request.user)[0].rides_driven).split(",")
    ridesDriving = []
    for ride in ridesDrivingIds:
        query = Posting.objects.filter(posting_id=ride)
        if query.count() > 0:
            ridesDriving.append(query[0])

    return render(request, 'user_profile/profile.html',
                  {'title': 'Profile', 'id': id, 'ridesDriving': ridesDriving, 'viewingPassenger': False, 'current_user': current_user})
