from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
#from django.views.generic.edit import CreateView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Post, Follow, Comment
from django.contrib.auth.models import User
from.forms import NewCommentForm


# Create your views here.
# def home(request):
#    context={
#           'portfolio': Portf.objects.all()
#      }
# return render(request,'index.html',context)


#def detail(request, id):
 #   context = {
  #      'per': get_object_or_404(Portf, pk=id),
   #   }
   #return render(request, 'detail.html', context)



"""
class Portfdetailview(LoginRequiredMixin,DetailView):
        template_name  = 'detail.html'
        model = Portf
        context_object_name = 'per'

"""


@login_required
def searchview(request):
    if request.GET:
        searchterm = request.GET["searchterm"]
        
        search_results = User.objects.filter(
            
         Q(username__icontains= searchterm)

        )  
        
        context = {

            'result': searchterm 
        }
        return redirect('user_posts', username= context['result'])
    else:
        return redirect('home')

"""
class Portfcreateview(LoginRequiredMixin,CreateView):
    template_name = 'create.html'
    model = Portf
    fields = ['name', 'job_dec', 'skills', 'email', 'phoneno',
              'gender', 'image', 'address', 'nationality']
    success_url = '/'

class Signupview(CreateView):
    form_class= UserCreationForm
    template_name='registration/signup.html'
    success_url= reverse_lazy('home')"""
def is_users(post_user, logged_user):
    return post_user == logged_user


class HomePageView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'post'
    ordering = ['-date_posted']

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, f'Account has been updated.')
            return redirect('home')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'create.html', {'uform': uform, 'pform': pform})



class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'person_detail.html'
    context_object_name = 'post'
    

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
       # print(logged_user.username == '', file=sys.stderr)
        post_count = Post.objects.filter(author=visible_user).count()
        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=logged_user,
                                                follow_user=visible_user).count() == 0)
        data = super().get_context_data(**kwargs)

        data['user_profile'] = visible_user
        data['can_follow'] = can_follow
        data['post_count'] = post_count
        return data
    
    def get_queryset(self):
        user = self.visible_user()
        return Post.objects.filter(author=user).order_by('-date_posted')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(user=request.user,
                                                    follow_user=self.visible_user())

            if 'follow' in request.POST:
                    new_relation = Follow(user=request.user, follow_user=self.visible_user())
                    if follows_between.count() == 0:
                        new_relation.save()
            elif 'unfollow' in request.POST:
                    if follows_between.count() > 0:
                        follows_between.delete()

        return self.get(self, request, *args, **kwargs)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        data['count_comment'] = comments_connected.count()
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              author=self.request.user,
                              post_connected=self.get_object())
        new_comment.save()

        return self.get(self, request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

        def post_del(self, request, *args, **kwargs):
            if request.GET:
                return self.get(self, request, *args, **kwargs)
            else:
                return redirect('home')




class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image','content']
    template_name = 'post_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add a new post'
        return data


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['image', 'content']
    template_name = 'post_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Edit a post'
        return data

class FollowsListView(ListView):
    model = Follow
    template_name = 'follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        return data


class FollowersListView(ListView):
    model = Follow
    template_name = 'follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(follow_user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'followers'
        return data
