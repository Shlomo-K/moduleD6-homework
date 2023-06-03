from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView 

from django.core.paginator import Paginator 
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Category, SubscribedUsersCategory
from .filters import NewsFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


 
class NewsList(LoginRequiredMixin, ListView):
    model = Post  
    template_name = 'news.html'  
    context_object_name = 'news'  
    queryset = Post.objects.order_by('-dateCreat')
    paginate_by = 1 
    form_class = PostForm  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())

       
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST )  

        if form.is_valid():  
            form.save()

        return super().get(request, *args, **kwargs)

class PostDetail(DetailView):
    model = Post 
    template_name = 'post.html' 
    context_object_name = 'post' 

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_category'] = Category.objects.filter(subscribed_users=self.request.user)
        else:
            context['user_category'] = None
        return context


class SearchNews(ListView):
    model = Post  
    template_name = 'search.html'  #
    context_object_name = 'news'  
    queryset = Post.objects.order_by('-dateCreat')
    paginate_by = 1 

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'add.html'
    form_class = PostForm

class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post')
    template_name = 'add.html'
    form_class = PostForm


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

def subscription(request):
    category_id = request.GET.get('category_id')
    print (category_id)
    category = Category.objects.get(id=category_id)
    
    if not category.subscribed_users.filter(email=request.user.email).exists():
        user = request.user
        SubscribedUsersCategory.objects.create(subscribed_users=user, category=category)
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))