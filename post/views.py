from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.utils.text import slugify #slugify methodu stringi araları tire olacak şekilde tekrar oluşturur oluşturur
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
def post_view(request):
    return HttpResponse('POSTS ARE HERE!')


def post_index(request):
    post_list=Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |# modelde bulunan title a göre arama yapar icontains aldığı parametreye göre küçük büyük harf duyarı olmadan çalışır.
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct() #.distinct() aynı kayıtlar birden fazla gözükmeyecek
    paginator = Paginator(post_list, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request,'post/index.html',{'posts':posts})
    #'post'= template de kullandığım kelime.
    #posts=Post.objects.all() veri tabanından postları aldığım değişken


def post_detail(request, slug):
    post = get_object_or_404(Post,slug = slug ) # url de id sini belirttiğim o id ye sahip post gelir
    # get_object_or_404(404 sayfası getirmeyi sağlar)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(
            commit=False)  # .save methodu kayıt işleminden sonra nesneyi geri döndüren bir metoddur.#(commit=False) nesneyi veritabanına eklemez, formdan aldığı bilgilerle nesneyi geri döndürür.
        comment.post = post #hangi posta yorum yapıldığını görmek için yukardaki post nesnesine eşitledik
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())
    context={
        'post': post,
        'form' : form,
    }
    return render(request,'post/detail.html',context)



def post_create(request):

    if not request.user.is_authenticated:#Kullanıcı giriş yapmamışsa 404 sayfasına yönlendir.
        raise Http404() #Hata yakalamak için raise kullanılır.

    # if request.method=="POST":
    #     print(request.POST)
    # title=request.POST.get('title') (BU SEKİLDE KULLANILABİLİR AMA ÖNERİLMEZ)
    # content=request.POST.get('content')
    # Post.objects.create(title=title, content=content)



    # if request.method=="POST":
    #     # Formdan gelen bilgileri kaydet
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    # else:
    #     # Formu kullanıcıya göster
    #     form = PostForm() (ALTTAKIYLE AYNI ANLAMDA)

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit= False)# .save methodu kayıt işleminden sonra nesneyi geri döndüren bir metoddur.#(commit=False) nesneyi veritabanına eklemez, formdan aldığı bilgilerle nesneyi geri döndürür.
        post.user = request.user
        post.save()
        messages.success(request,'MESSAGE IS CREATED SUCCESSFULLY!')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form
    }

    return render(request,'post/form.html',context)


def post_update(request, slug):
    if not request.user.is_authenticated:
        raise Http404()
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None,instance=post) #instance=post posttaki bilgileri forma aktarıyoruz
    if form.is_valid():
        form.save()
        messages.success(request, 'MESSAGE IS updated  SUCCESSFULLY!', extra_tags='Message-is-successful')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form
    }
    return render(request,'post/form.html',context)


def post_delete(request, slug):
    if not request.user.is_authenticated:
        raise Http404()
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post:index')
