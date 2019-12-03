from django.db import models
from django.urls import reverse
from django.utils.text import slugify



# Create your models here.

class Post(models.Model):
    user = models.ForeignKey('auth.User', verbose_name='Writer', on_delete=models.CASCADE, related_name='posts')#shellde tüm alakalı postları getirmek için post_get yerine posts kullanılacaktır.
    title = models.CharField(max_length=120, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    publishing_date = models.DateField(verbose_name='Publishing Date', auto_now_add=True)
    image=models.FileField(null=True, blank=True)#null ve blankın True olması boş olabileceği anlamına gelir
    slug=models.SlugField(unique=True, editable=False, max_length=130) #editable=False programatik atanacak slug alanı


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug':self.slug})
        # return "/post/{}".format(self.id)

    def get_create_url(self):
        return reverse('post:create')
    def get_update_url(self):
        return reverse('post:update', kwargs={'slug':self.slug})
    def get_delete_url(self):
        return reverse('post:delete', kwargs={'slug':self.slug})
    def get_unique_slug(self): #eşsiz slug oluşturmak için aynı başlık varsa eğer sonuna autoincrement sayı atıyor algoritma.
        slug = slugify(self.title.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists(): #.exists() aynı slug var mı yok mu diye kontrol eder.
            unique_slug = '{}-{}'.format(slug,counter)
            counter += 1
        return unique_slug
    def save(self,*args,**kwargs):
        # if not self.slug: # başlık güncellendiğinde slug alanı da güncellenmesi için if kosulunu kaldırmak gerek
        self.slug = self.get_unique_slug()
        return super(Post,self).save(*args,**kwargs)
    class Meta:
        ordering = ['-id']

class Comment(models.Model):
    post = models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, verbose_name = 'Name')
    content = models.TextField(verbose_name='Comment')
    created_date = models.DateField(auto_now_add=True)