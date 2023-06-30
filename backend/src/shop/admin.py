from django.contrib import admin

from src.shop import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	prepopulated_fields = {"slug": ("name", )}
	search_fields = ("name",)
	ordering = ("name",)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ("name",)
	prepopulated_fields = {"slug": ("name", )}
	ordering = ("name",)


class ProductImageInline(admin.StackedInline):
	model = models.ProductImage
	max_num = 10
	extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("pkid", "id", "title", "category", "price", "available")
	list_display_links = ("pkid", "id")
	list_editable = ("available", )
	list_filter = ("available", )
	search_fields = ("title",)
	ordering = ("title",)
	prepopulated_fields = {"slug": ("title",)}
	inlines = [ProductImageInline]
