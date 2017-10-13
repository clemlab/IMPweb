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
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^dbquery/$', views.job_view, name='db_view_dep'),
    url(r'^job=(?P<uuid>[^/]+)/$', views.batch_view, name='job_view'),
    url(r'^result=(?P<uuid>[^/]+)/$', views.job_view, name='db_view'),
    url(r'^user_results/$', views.user_view, name='user_view'),
    url(r'^recent_results$', views.recent_table, name='recent_results')
    # url(r'^', views.formredirect, name='redirect'),
]
