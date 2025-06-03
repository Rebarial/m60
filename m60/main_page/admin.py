from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *

class StatisticInline(admin.TabularInline):
    model = Statistic
    extra = 0
    verbose_name_plural = "Статистические данные"

class ServiceSubtitle1Inline(admin.TabularInline):
    model = ServiceSubtitle1
    extra = 0
    verbose_name_plural = "Пункты под подзаголовком услуг 1"

class ServiceSubtitle2Inline(admin.TabularInline):
    model = ServiceSubtitle2
    extra = 0
    verbose_name_plural = "Пункты под подзаголовком услуг 2"

class IncludedServiceInline(admin.TabularInline):
    model = IncludedService
    extra = 0
    verbose_name_plural = "Включенные услуги"

class ServiceInline(admin.StackedInline):
    model = Service
    extra = 0
    show_change_link = True
    inlines = [ServiceSubtitle1Inline, ServiceSubtitle2Inline, IncludedServiceInline]
    verbose_name_plural = "Основные услуги"

class AdditionalServicesInline(admin.TabularInline):
    model = AdditionalServices
    extra = 0
    verbose_name_plural = "Дополнительные услуги"

class AdvantageInline(admin.TabularInline):
    model = Advantage
    extra = 0
    verbose_name_plural = "Преимущества"

class InstructorsInline(admin.TabularInline):
    model = Instructors
    extra = 0
    verbose_name_plural = "Инструкторы"

class StagesInline(admin.TabularInline):
    model = Stages
    extra = 0
    verbose_name_plural = "Этапы обучения"

class ReviewsInline(admin.TabularInline):
    model = Reviews
    extra = 0
    verbose_name_plural = "Отзывы"

class ReviewsVideoInline(admin.TabularInline):
    model = ReviewsVideo
    extra = 0
    verbose_name_plural = "Видео отзывы"

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 0
    verbose_name_plural = "Часто задаваемые вопросы"

@admin.register(PageInfo)
class PageInfoAdmin(ModelAdmin):
    inlines = [
        StatisticInline,  # Включаем сюда нужный нам inline-класс
        ServiceInline,
        AdditionalServicesInline,
        AdvantageInline,
        InstructorsInline,
        StagesInline,
        ReviewsInline,
        ReviewsVideoInline,
        FAQInline,
    ]

    fieldsets = (
        ('Контактная информация', {
            'fields': (
                'telephone', 
                'watsapp_link', 
                'telegram_link',
                'address',
                'hotline_telephone',
            )
        }),
        ('Данные первой страницы', {
            'fields': (
                'title',
                'subtitle',
                'description',
                'price',
                'price_button',
                'price_description',
            ),
        }),
        ('Заголовки разделов', {
            'fields': (
                'services_title',
                'services_subtitle',
                'additional_services_title',
                'additional_services_subtitle',
                'advantage_title',
                'advantage_subtitle',
                'about_us_title',
                'about_us_subtitle',
                'about_us_description',
                'about_us_button',
                'instructor_title',
                'instructor_subtitle',
                'stage_title',
                'stage_subtitle',
                'reviews_title',
                'reviews_subtitle',
                'reviews_google_rating',
                'reviews_yandex_rating',
                'reviews_2gis_rating',
                'start_education_title',
                'start_education_description',
                'start_education_image',
                'faq_title',
            )
        }),
    )
    