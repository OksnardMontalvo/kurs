from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from studykurs.models import Course, Category, UserAccount
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.http import JsonResponse, HttpResponseRedirect
from studykurs.forms import CommentForm, RegistrationForm, LoginForm
from django.contrib.auth import get_user_model, authenticate, login, logout
User = get_user_model()

# Create your views here.
class CourseListView(ListView):
    model = Course
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)
        context['courses'] = self.model.objects.all()

        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data(*args, **kwargs)
        context['categories'] = self.model.objects.all()
        context['courses'] = Course.objects.all()
        return context


class CategoryDetailview(DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailview, self).get_context_data(*args, **kwargs)
        context['categories'] = self.model.objects.all()
        context['category'] = self.get_object()
        context['courses_from_category'] = self.get_object().course_set.all()
        return context


class CourseDetailview(DetailView):
    model = Course
    template_name = 'course_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailview, self).get_context_data(*args, **kwargs)

        context['categories'] = Category.objects.all()
        context['course'] = self.get_object()
        context['course_comments'] = self.get_object().comments.all().order_by('-timestamp')
        context['form'] = CommentForm()
        context['current_user'] = UserAccount.objects.get(user=self.request.user)

        return context


class CreateCommentView(View):
    template_name = 'course_detail.html'

    def post(self, request, *args, **kwargs):

        course_id = self.request.POST.get('course_id')
        comment = self.request.POST.get('comment')
        course = Course.objects.get(id=course_id)
        new_comment = course.comments.create(author=request.user, comment=comment)
        comment = [{'author': new_comment.author.username, 'comment': new_comment.comment,
                    'timestamp': new_comment.timestamp.strftime('%Y-%m-%d')}]
        return JsonResponse(comment, safe=False)


class RegistrationView(View):
    template_name = 'registration.html'

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form':form
        }
        return render(self.request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            new_user.set_password(password)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            new_user.save()
            UserAccount.objects.create(user=User.objects.get(username=new_user.username), first_name=new_user.first_name, last_name=new_user.last_name,email=new_user.email)
            return HttpResponseRedirect('/')
        context = {
            'form':form
        }
        return render(self.request, self.template_name, context)

class LoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form':form
        }
        return render(self.request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           user = authenticate(username=username, password=password)
           if user:
               login(self.request, user)
               return HttpResponseRedirect('/')
        context = {
            'form':form
        }
        return render(self.request, self.template_name, context)

class UserAccountView(View):
    template_name = 'user_account.html'

    def get(self, request, *args, **kwargs):
        user = self.kwargs.get('user')
        current_user = UserAccount.objects.get(user=User.objects.get(username=user))
        context = {
            'current_user': current_user
        }
        return render(self.request, self.template_name, context)

class AddCourseToFavorites(View):
    template_name = 'course_detail.html'

    def get(self, request, *args, **kwargs):
        course_slug = self.request.GET.get('course_slug')
        course = Course.objects.get(slug=course_slug)
        current_user = UserAccount.objects.get(user=request.user)
        current_user.favourite_courses.add(course)
        current_user.save()
        return JsonResponse({'ok':'ok'})

class SearchView(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        founded_courses = Course.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        context = {
            'founded_courses': founded_courses
        }
        return render(self.request, self.template_name, context)


