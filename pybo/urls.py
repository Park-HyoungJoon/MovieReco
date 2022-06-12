from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'pybo'

urlpatterns = [
    path('',views.index,name='index'),
    path('<int:question_id>/',views.detail,name='detail'),
    path('<int:question_id>/',views.modal,name='modal'),
    path('main',views.main,name='main'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)