from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout

from studykurs.views import  (CategoryListView, CategoryDetailview,
                              CourseDetailview, CreateCommentView, RegistrationView,
                              LoginView, UserAccountView, AddCourseToFavorites, SearchView)

urlpatterns = [

    url(r'^$', CategoryListView.as_view(), name='base-view'),
    url(r'^user_account/(?P<user>[-\w]+)/$', UserAccountView.as_view(), name='user_account'),
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryDetailview.as_view(), name='category-detail'),

    url(r'^(?P<category>[-\w]+)/(?P<slug>[-\w]+)/$', CourseDetailview.as_view(), name='course-detail'),
    url(r'^add_comment/$', CreateCommentView.as_view(), name='add_comment'),
    url(r'registration/$', RegistrationView.as_view(), name='registration'),
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('base-view')), name='logout_view'),
    url(r'^add_to_favourites/$', AddCourseToFavorites.as_view(), name='add_to_favourites'),
    url(r'^search/$', SearchView.as_view(), name='search_view')









]