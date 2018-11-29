from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from .views import CreateView, DetailsView
from .prstatus_views import PRStatus
from .repository_views import Repository
from .pr_views import PullRequests


urlpatterns = {

    url(r'^auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^accesstokenlists/$', CreateView.as_view(), name="create"),
    url(r'^accesstokenlists/(?P<pk>\d+)/$', DetailsView.as_view(),
        name="details"),
    url(r'^get-token/', obtain_auth_token,name="token"),
    url(r'^prstatus/(?P<pk>\d+)/$',PRStatus.get_pr_status, name="all_prs"),
    url(r'^repository/(?P<pk>\d+)/$',Repository.get_repo_list, name="repo_list_in_org"),
    url(r'^prs/(?P<pk>\d+)/(?P<organization>.+)/(?P<repository>.+)/$',
        PullRequests.get_repo_list, name="pr_list_in_repo"),
    url(r'^prstatus/(?P<pk>\d+)/(?P<organization>.+)/(?P<repository>.+)/$',
        PRStatus.get_pr_status, name="all_prs_in_repo"),
    url(r'^prstatus/(?P<pk>\d+)/(?P<organization>.+)/' +
        '(?P<repository>.+)/(?P<pr>\d+)/$',PRStatus.get_pr_status, name="one_pr_in_repo"),
    url('', include('django_prometheus.urls'), name="metrics"),

}

urlpatterns = format_suffix_patterns(urlpatterns)