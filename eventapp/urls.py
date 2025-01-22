
from django.urls import path
from eventapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add_event/',views.add_event),
    path('card/<int:id>',views.event_card),
    path('cardlist/',views.card_list),
    path('search/',views.serch_home),
    path('update/<int:id>',views.update_events),
    path('delete/<int:id>',views.delete)

]+static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)