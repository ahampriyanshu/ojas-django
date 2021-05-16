from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Post, Comment, Author, Viewer, Admin, Subscriber
from django.utils.text import slugify
import csv
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.admin import AdminSite

max_admin = 1
AdminSite.site_header = "Admin Panel"
AdminSite.site_title = "Admin Panel"
AdminSite.index_title = "Home"


class ExportToCsvMixin:
    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_to_csv.short_description = "Export Data As CSV File"


class AuthorAdmin(admin.ModelAdmin, ExportToCsvMixin):
    list_display = ('author', 'joined')
    date_hierarchy = 'joined'
    readonly_fields = ["author",]
    actions = ["export_to_csv"]


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["author","Image_Preview"]
        else:
            return []

    def Image_Preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=200,
            height=200,
            )
    )


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


admin.site.register(Author, AuthorAdmin)



class ViewerAdmin(admin.ModelAdmin, ExportToCsvMixin):
    list_display = ('post','ip','session','last_visited',)
    actions = ["export_to_csv"]
admin.site.register(Viewer, ViewerAdmin)


class PostAdmin(admin.ModelAdmin, ExportToCsvMixin):
    list_display = ('title', 'views', 'unique_visitor', 'notified', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': (slugify('title'),)}
    date_hierarchy = 'publish'
    ordering = ['status', '-publish']
    actions = ['delete_selected', 'draft_selected', 'publish_selected','export_to_csv']
    readonly_fields = ["author", "Image_Preview"]


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["author", "Image_Preview"]
        else:
            return []


    def Image_Preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=200,
            height=200,
            )
    )

    def publish_selected(self, request, queryset):
        queryset.update(status='published')
    publish_selected.short_description = "Publish the selected posts"


    def draft_selected(self, request, queryset):
        queryset.update(status='draft')
    draft_selected.short_description = "Draft the selected posts"

    
    def save_model(self, request, obj, form, change):
        obj.author = request.user.author
        super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user.author)


    def view_on_site(self, obj):
        return reverse('admin:preview', kwargs={'id': obj.pk})

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')
    actions = ["export_to_csv", 'hide_comment', 'unhide_comment']

    def hide_comment(self, request, queryset):
        queryset.update(active = False)
    hide_comment.short_description = "Hide selected comments"

    def unhide_comment(self, request, queryset):
        queryset.update(active = False)
    unhide_comment.short_description = "Unhide selected comments"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(post__author=request.user.author)
admin.site.register(Comment, CommentAdmin)

class SubscriberAdmin(admin.ModelAdmin, ExportToCsvMixin):
    list_display = ('email','confirmed','created_date',)
    actions = ["export_to_csv"]

admin.site.register(Subscriber, SubscriberAdmin)

class AdminAdmin(admin.ModelAdmin):
    list_display = ('title','owner',)
    readonly_fields = ["Image_Preview"]


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["Image_Preview"]
        else:
            return []


    def Image_Preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=200,
            height=200,
            )
    )


    def has_add_permission(self, request):
        if self.model.objects.count() >= max_admin:
            return False
        return super().has_add_permission(request)

admin.site.register(Admin, AdminAdmin)