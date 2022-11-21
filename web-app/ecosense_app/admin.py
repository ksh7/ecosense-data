from django.contrib import admin
from .models import User, Dataset, Category, Topic, DataSource, CustomDataAPI, ResearchInsight

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    pass

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomDataAPI)
class CustomDataAPIAdmin(admin.ModelAdmin):
    pass

@admin.register(ResearchInsight)
class ResearchInsightAdmin(admin.ModelAdmin):
    pass
