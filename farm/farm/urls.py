"""
URL configuration for art project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from farm import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # your url patterns
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])



urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index, name='index'), 
    path('header/',views.header, name='header'), 
    path('home/',views.home, name="home"), 
 path('video_feed/', views.video_feed, name='video_feed'),
    path('sell_crop/',views.sellCrop, name="sell_crop"),
    path('farm_monitiring/',views.farmMonitiring, name="farm_monitiring"),
    path('workers/',views.workers, name="workers"),
    path('storage/',views.storage, name="storage"),
        path('logout/',views.logout_page,name='logout_page'),
      path('', views.login_signup, name="login_signup"),
      path('buyier/',views.buyier,name="buyier"),
      path('video_feed/', views.video_feed, name='video_feed'),
        path('object_names_stream/', views.object_names_stream, name='object_names_stream'),

]