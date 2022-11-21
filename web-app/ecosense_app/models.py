from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

def default_graph_data():
    return {'title': '', 'labels': [], 'data': []}

class User(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    username = models.CharField(max_length=128, unique=False)
    organization = models.CharField(max_length=128, blank=True, null=True)
    bio = models.TextField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.username is None:
            self.username = (self.first_name[0] + self.last_name.replace(' ', '')).lower()
        super().save(*args, **kwargs)


class TopicManager(models.Manager):
    def create_or_new(self, title):
        title = title.strip()
        qs = self.get_queryset().filter(title__iexact=title)
        if qs.exists():
            return qs.first(), False
        return Topic.objects.create(title=title), True

    def comma_to_qs(self, topics_str):
        final_ids = []
        for topic in topics_str.split(','):
            obj, created = self.create_or_new(topic)
            final_ids.append(obj.id)
        qs = self.get_queryset().filter(id__in=final_ids).distinct()
        return qs


class Topic(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(blank=True, null=True)

    objects = TopicManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class DataSource(models.Model):
    name = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=256, null=False)
    filters = models.CharField(max_length=256, null=True)
    topics = models.ManyToManyField(Topic, blank=False)
    sample_graph_data_available = models.BooleanField(default=False)
    sample_graph_data = models.JSONField(default=default_graph_data)
    aws_endpoint = models.CharField(max_length=128, null=True)
    aws_api_url = models.CharField(max_length=512, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: %s" % (self.name, self.description)


class CustomDataAPI(models.Model):
    name = models.CharField(max_length=128, null=False)
    url = models.CharField(max_length=128, null=False)
    topics = models.CharField(max_length=512, null=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dataset(models.Model):
    name = models.CharField(max_length=128, null=False)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, blank=True)
    data_sources = models.ManyToManyField(DataSource, blank=True)
    how_to_data = models.TextField(blank=True)
    applied_questions = models.TextField(blank=True)
    api_endpoint = models.CharField(max_length=128, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.api_endpoint = "api/" + slugify(self.name)
        super(Dataset, self).save(*args, **kwargs)
    
    def get_public_researchinsights(self):
        return self.researchinsight_set.filter(is_public=True).all()

    def __str__(self):
        return self.name


class ResearchInsight(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=False)
    is_public = models.BooleanField(default=False)
    finding = models.TextField()
    description = models.TextField()
    attribution = models.TextField()
    graph_data_available = models.BooleanField(default=False)
    graph_data = models.JSONField(default=default_graph_data)
    dataset = models.ForeignKey(Dataset, blank=False, on_delete=models.CASCADE)
    data_sources = models.ManyToManyField(DataSource, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s by %s %s" % (self.title, self.user.first_name, self.user.last_name)
