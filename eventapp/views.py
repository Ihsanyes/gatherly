from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from userapp.models import UserSignup
from .models import CreateEvent, EventImage,Service


# Create your views here.
def add_event(request):
    if 'user_id' in request.session:
        # user_id = request.session['user_id']
        if request.method == 'POST':
            user_id = request.session['user_id']
            user_obj = UserSignup.objects.get(id=user_id)
            obj = CreateEvent()
            obj.create_title = request.POST.get('create_title')
            obj.established_in = request.POST.get('established_in')
            obj.contact = request.POST.get('contact')
            obj.wh_number = request.POST.get('wh_number')
            obj.address = request.POST.get('address')
            selected_services = request.POST.getlist('select_services')  # Get all selected service IDs
            new_service_name = request.POST.get('new_service')  # Get the new service name
            obj.event_photos = request.FILES['event_photos']
            obj.price = request.POST.get('price')
            obj.creator = user_obj
            obj.save()

            # if obj.creator != UserSignup.objects.get(id=user_id):
            #     return render(request, 'eventcard.html', {'message': 'You are not authorized to edit this event.'})

            # CreateEvent.objects.
        
            # Handle selected services
            selected_services = request.POST.getlist('select_services')  # Get selected service IDs
            for service_id in selected_services:
                service = get_object_or_404(Service, id=service_id)
                obj.select_services.add(service)  # Add to ManyToManyField

            # Handle new service
            new_service_name = request.POST.get('new_service')  # Get new service name
            if new_service_name:
                new_service, created = Service.objects.get_or_create(name=new_service_name)
                obj.select_services.add(new_service)  # Add new service to the event

            return redirect('/event/cardlist/',event_id=obj.id)
        services = Service.objects.all()
        return render(request, 'add_event.html',{'service':services})
    else:
        return redirect('/login/')

def update_events(request,id):
    obj = CreateEvent.objects.get(id=id)
    if request.method == 'POST':
        obj = CreateEvent()
        obj.create_title = request.POST.get('create_title')
        obj.established_in = request.POST.get('established_in')
        obj.contact = request.POST.get('contact')
        obj.wh_number = request.POST.get('wh_number')
        obj.address = request.POST.get('address')
        obj.select_services = request.POST.get('services')
        obj.event_photos = request.FILES['event_photos']
        obj.price = request.POST.get('price')
        obj.save()
    return render(request, 'update_events.html',{'obj':obj})




def card_list(request):
    if 'user_id' in request.session:
        # Fetch user details
        user_id = request.session['user_id']
        user_obj = UserSignup.objects.get(id=user_id)

        # Get the sort parameter from the query string
        sort_by = request.GET.get('sort_by', 'newest')  # Default to newest
        selected_category = request.GET.get('category', '')  # Get selected category from the request

        # Apply sorting logic
        if sort_by == 'top_rated':
            events = CreateEvent.objects.prefetch_related('select_services').order_by('-rating')  # Sort by rating
        elif sort_by == 'price_low_high':
            events = CreateEvent.objects.prefetch_related('select_services').order_by('price')  # Sort by price low-high
        elif sort_by == 'price_high_low':
            events = CreateEvent.objects.prefetch_related('select_services').order_by('-price')  # Sort by price high-low
        elif selected_category:
            events = CreateEvent.objects.filter(select_services__name=selected_category)
        else:
            events = CreateEvent.objects.prefetch_related('select_services').order_by('-created_at')  # Default to newest
            events = CreateEvent.objects.all()  # If no category is selected, show all events

        services = Service.objects.all()  # Fetch all services for the dropdown

        # if request.method =="POST":
        #     search = request.get('query')
        #     if search:
        #         data = CreateEvent.objects.filter(create_title=search)

        # Render the template
        return render(request, 'card_list.html', {'eventdata': events, 'userdata': user_obj, 'sort_by': sort_by,'services':services})
    else:
        return redirect('/login/')


def event_card(request,id):
    if 'user_id' in request.session:
        obj = CreateEvent.objects.get(id=id)
        user_id = request.session['user_id']
        user_obj = UserSignup.objects.get(id=user_id)
        

        if obj.creator.id == user_id:
            msg = 'ok'
        else:
            msg = 'error'


        images = request.FILES.getlist('images')
        for image in images:
            EventImage.objects.create(event=obj, image=image)

        events = CreateEvent.objects.prefetch_related('images').all()

        return render(request, 'eventcard.html',{'carddata':obj,'userdata':user_obj,'events':events,'msgg':msg})
    else:
        return redirect('/login/')


# def serch_home(request):
#     if request.method == 'get':
#         query = request.GET.get('q', '')  # Get the query from the GET parameter
#         items = CreateEvent.objects.filter(create_title__icontains=query) #if query else []  # Filter only if query exists
#         return render(request, 'card_list.html', {'items': items, 'query': query})
    
def serch_home(request):
    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        if query:
            print(query)
            results = CreateEvent.objects.filter(create_title__icontains=query)
            return render(request, 'card_list.html', {'results': results, 'query': query})
        else:
            print("no result")
            return render(request, 'card_list.html', {'results': None, 'query': query})
    return render(request, 'card_list.html', {'results': None})


def delete(request,id):
    obj = CreateEvent.objects.get(id=id)
    obj.delete()
    return redirect('/event/cardlist/')