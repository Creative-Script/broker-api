from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Broker",
      default_version='v1',
      description=
      ('The Broker is a simple solution that helps users have access'
      'to more sophisticated Real Estate investments'),
      license=openapi.License(name="AGPL-3.0"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    # administration link
    path('admin/', admin.site.urls),
    # swagger documentation link
    path('docs/', schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('api/', include('broker.apps.home.urls')),
]
