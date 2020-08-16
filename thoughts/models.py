from django.db import models 
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User 
from taggit.managers import TaggableManager


# manger that returns the published articles 
class PublishedManger(models.Manager):
    def get_query_set(self):
        return super()\
            .get_query_set()\
            .filter(status='publish')


# Post db 
class Post(models.Model):
    status_choices = (
       ('publish', 'Publish'),
       ('draft', 'Draft')
    )

    title = models.CharField(max_length=50)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='article'
    )

    slug = models.SlugField(
        max_length=25,
        unique_for_date='publish'
    )

    description = models.CharField(blank=True, max_length=100)

    body = models.TextField()

    showcase_image = models.ImageField(upload_to="showcase_images/%Y/%m/%d",
                              blank=True)

    publish = models.DateTimeField(default=timezone.now)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        choices=status_choices,
        default='draft',
        max_length=20,
    )
    
    class Meta:
        ordering = ('-publish', )

    objects = models.Manager()  # The default manager 
    published = PublishedManger() # The custom publish manager
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('thoughts:detail_display', args=[
                                                    self.publish.year,
                                                    self.publish.month,
                                                    self.publish.day,
                                                    self.slug

                                                   ]
        )

    def image(self):
        """
        if post.showcase images is called directly it returns just a path this return the full image 
        """
        
        image_route = f"""<img class="card-img-top" src="{ str(self.showcase_image.url) }" alt="Image">"""
        return mark_safe(image_route)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete = models.CASCADE,
        related_name='comments',        
                            )

    user_name = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments', blank=True, null=True)

    email = models.EmailField(null=True)

    comment = models.TextField()

    publish = models.DateTimeField(default=timezone.now)

    active = models.BooleanField(default=True)

    class Meta: 
        ordering = ('-publish',)
    
    def __str__(self): 
        return f'Comment by {self.user_name} on {self.post}'

    def profile_picture(self):
        """
        if comment.profile_picture is called directly it returns just a path this return the full image 
        """

        image_route = f"""<img  src="{ str(self.user_name.profile.photo.url) }" alt="Image" class="rounded-circle" style="width:40px; height:40px;">"""
        return mark_safe(image_route)


        