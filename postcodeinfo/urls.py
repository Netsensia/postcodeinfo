from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from postcode_api import views


router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet)


urlpatterns = patterns('',
                       url(r'^postcodes/'
                           '(?P<postcode>[a-zA-Z0-9\s]+)/$',
                           views.PostcodeView.as_view()),

                       url(r'^postcodes/'
                           'partial/(?P<postcode>[a-zA-Z0-9\s]+)/$',
                           views.PartialPostcodeView.as_view()),


                       url(r'^', include(router.urls)),

                       url(r'^admin/', include(admin.site.urls)),
                       )
