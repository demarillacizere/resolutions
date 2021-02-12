from django.conf.urls import url,include
from django.conf import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^accounts/profile/', views.my_profile, name='my_profile'),
    url(r'register/',views.register, name='register'),
    url(r'^post(?P<post_id>\d+)', views.single_post, name='single_post'),
    # url(r'proj/(\d+)',views.view_goal,name='view-goal'),
    # url(r'profile/(\d+)',views.profile,name='profile'),
    url(r'my_profile',views.my_profile,name='my_profile'), 
    url(r'^new/post$', views.new_post, name='new_post'),
    # url(r'^search/', views.search_results, name='search_results'),
    # url(r'^accounts/', include('registration.backends.simple.urls')),

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)