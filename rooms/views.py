from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Rooms, RoomImage, Facilities, Booking
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def home(request):
    cars = Rooms.objects.order_by('-id')
    paginator = Paginator(cars, 4)
    page = request.GET.get('page')
    paged_cars = paginator.get_page(page)
    facilities = Facilities.objects.all()

    room_facilities = Rooms.objects.values_list('facilites_no').distinct()
    if request.session.get("start_date") and request.session.get("end_date") and request.session.get("bill") and request.session.get("no_of_days"):
        del request.session['start_date']
        del request.session['end_date']
        del request.session['bill']
        del request.session['no_of_days']
    data = {
        'cars': paged_cars,
        'facilities':facilities,
        'room_facilities':room_facilities
      
    }
    return render(request, 'rooms/rooms.html', data)


def room_detail(request, id):
     if request.session.get("no_of_days",1):
            no_of_days=request.session['no_of_days']
            start_date=request.session['start_date']
            end_date=request.session['end_date']
            single_room = get_object_or_404(Rooms, pk=id)
            bill=single_room.price*int(no_of_days)
            request.session['bill']=bill
            
            context={
                'single_room':single_room,
                "no_of_days":no_of_days,
                "bill":bill,
                "start_date":start_date,
                "end_date":end_date
            }
            return render(request,"rooms/room_detail.html",context)
     else:
            return redirect("home")


def rooms(request):
    cars = Rooms.objects.order_by('-price')
    facilities = Facilities.objects.all()

    # model_search = Car.objects.values_list('model', flat=True).distinct()
    # checkin checkout filteration
    if request.GET.get('checkin') and request.GET.get('checkout'):
          start_date=request.GET.get('checkin')
          end_date=request.GET.get('checkout')
          request.session['start_date']=start_date
          request.session['end_date']=end_date
          # start_date=datetime.strptime(start_date, "%Y-%b-%d").date()
          # end_date=datetime.strptime(end_date, "%Y-%b-%d").date()
          start_date=datetime.strptime(str(start_date), "%Y-%m-%d").date()
          end_date=datetime.strptime(str(end_date), "%Y-%m-%d").date()

          no_of_days=(end_date-start_date).days
          request.session['no_of_days']=no_of_days

          print("day differnt", no_of_days)
          cars=cars.filter(is_available=True,no_of_days_advance__gte=no_of_days,start_date__lte=start_date)

    #search filter, other filter
    search_facilities = request.GET.getlist('facilities')
    sort_by = request.GET.get('sort_by')

    if len(search_facilities):
        cars = cars.filter(facilites_no__id__in = search_facilities).distinct()

    if sort_by:
        if sort_by == 'ASC':
            cars = cars.order_by('price')
        elif sort_by == 'DSC':
            cars = cars.order_by('-price')

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cars = cars.filter(room_type__icontains=keyword)

    if 'model' in request.GET:
        model = request.GET['model']
        if model:
            cars = cars.filter(model__iexact=model)

    if 'min_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']
        if max_price:
            cars = cars.filter(price__gte=min_price, price__lte=max_price)
   
    
    data = {
        'cars': cars,
        'facilities':facilities
    }
    return render(request, 'rooms/search.html', data)


def book_confirm(request):
    if request.method=="POST":
        user_id=request.user.id
        user=User.objects.get(pk=user_id)
        room_id=request.POST.get('room_id')
        room=Rooms.objects.get(pk=room_id)

        start_date=request.session['start_date']
        end_date=request.session['end_date']
        amount=request.session['bill']

        start_date=datetime.strptime(start_date,  "%Y-%m-%d").date()
        end_date=datetime.strptime(end_date,  "%Y-%m-%d").date()
        no_of_days=(end_date-start_date).days
        data=Booking(start_day=start_date, end_day=end_date, price=amount, no_of_days=no_of_days, room_no=room, user_id=user)
        data.save()
        room.is_available=False
        room.save()
        del request.session['start_date']
        del request.session['end_date']
        del request.session['bill']
        if data.is_past_due:
            room.is_available=True
            room.save()
        messages.info(request,"Room has been successfully booked")
        return redirect('dashboard')
    else:
       return redirect('rooms')


def cancel_room(request,id):
    data=Booking.objects.get(id=id)
    room=data.room_no
    room.is_available=True
    room.save()
    data.delete()
    messages.success(request,"Booking Has Been Cencelled successfully")
    return redirect('dashboard')