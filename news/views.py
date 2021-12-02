from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView # импортируем необходимые дженерики
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm

class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 2
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateCreation')


    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


# дженерик для получения деталей о товаре
class PostDetailView(DetailView):
    template_name = 'sample_app/post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'sample_app/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    # дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
        template_name = 'sample_app/post_create.html'
        form_class = PostForm
        permission_required = ('news.change_post',)

        # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактирова
        def get_object(self, **kwargs):
            id = self.kwargs.get('pk')
            return Post.objects.get(pk=id)


    # дженерик для удаления товара
class PostDeleteView(DeleteView):
        template_name = 'sample_app/post_delete.html'
        queryset = Post.objects.all()
        success_url = '/news/'


