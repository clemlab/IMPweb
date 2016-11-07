from django.conf.urls import url

from . import views

"""Form URL documentation

urlpatterns sorts urls based on characters after form in the url

if no characters it goes to form,

thanks will redirect to form unless directed to by form, in which case it
returns the reverse of the string in the your_name entry in the post dictionary

"""

urlpatterns = [

    url(r'^$', views.get_name, name='webform'),
    url(r'^thanks', views.thanks, name='thanks'),
    url(r'^profile/$', views.profile, name='profile')
    # url(r'^', views.formredirect, name='redirect'),
]
