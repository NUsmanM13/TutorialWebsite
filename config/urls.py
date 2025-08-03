# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # import qiling
from django.conf.urls.static import static # import qiling


from django.conf.urls import handler404
from django.urls import re_path
from django.views.static import serve

handler404 = 'main.views.handler404_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    # CKEditor uchun URL
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('courses/', include('courses.urls', namespace='courses')),
    path('', include('users.urls', namespace='users')), # dashboard va sertifikatlar
    path('', include('main.urls', namespace='main')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]