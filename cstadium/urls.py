from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^leaderboard/', include('leaderboard.urls', namespace='leaderboard')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^contest/', include('contest.urls', namespace='contest')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^checker/', include('checker.urls', namespace='checker'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
