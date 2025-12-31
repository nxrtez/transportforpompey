from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "siteui"

urlpatterns = [
    path("", views.home, name="home"),

    path("status/", views.status_overview, name="status"),
    path("maps/", views.maps, name="maps"),
    path("fares/", views.fares, name="fares"),

    path("operators/", views.operators, name="operators"),

    path("operators/stagecoach/", views.stagecoach, name="operator_stagecoach"),
    path("operators/first/", views.first, name="operator_first"),

    path("operators/<slug:slug>/", views.operator_detail, name="operator_detail"),

    path("routes/", views.routes, name="routes"),
    path("routes/<uuid:uuid>/", views.route_detail, name="route_detail"),

    path("maps/<slug:slug>/", views.map_detail, name="map_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)