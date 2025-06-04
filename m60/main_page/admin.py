from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *
from nested_admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline

admin.site.register(Video)
admin.site.register(Order)

class StatisticInline(NestedStackedInline):
    model = Statistic
    extra = 0
    verbose_name_plural = "Статистические данные"

class ServiceSubtitle1Inline(NestedTabularInline):
    model = ServiceSubtitle1
    extra = 0
    verbose_name_plural = "Пункты под подзаголовком услуг 1"

class ServiceSubtitle2Inline(NestedTabularInline):
    model = ServiceSubtitle2
    extra = 0
    verbose_name_plural = "Пункты под подзаголовком услуг 2"

class IncludedServiceInline(NestedTabularInline):
    model = IncludedService
    extra = 0
    verbose_name_plural = "Включенные услуги"

class ServiceInline(NestedStackedInline):
    model = Service
    extra = 0
    show_change_link = True
    inlines = [ServiceSubtitle1Inline, ServiceSubtitle2Inline, IncludedServiceInline]
    verbose_name_plural = "Основные услуги"

class AdditionalServicesInline(NestedStackedInline):
    model = AdditionalServices
    extra = 0
    verbose_name_plural = "Дополнительные услуги"

class AdvantageInline(NestedStackedInline):
    model = Advantage
    extra = 0
    verbose_name_plural = "Преимущества"

class InstructorsInline(NestedStackedInline):
    model = Instructors
    extra = 0
    verbose_name_plural = "Инструкторы"

class StagesInline(NestedStackedInline):
    model = Stages
    extra = 0
    verbose_name_plural = "Этапы обучения"

class ReviewsInline(NestedStackedInline):
    model = Reviews
    extra = 0
    verbose_name_plural = "Отзывы"

class ReviewsVideoInline(NestedStackedInline):
    model = ReviewsVideo
    extra = 0
    verbose_name_plural = "Видео отзывы"

class FAQInline(NestedStackedInline):
    model = FAQ
    extra = 0
    verbose_name_plural = "Часто задаваемые вопросы"

@admin.register(PageInfo)
class PageInfoAdmin(NestedModelAdmin):
    inlines = [
        StatisticInline,
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
                'additional_services_title',
                'advantage_title',
                'advantage_subtitle',
                'about_us_title',
                'about_us_subtitle',
                'about_us_description',
                'about_us_button',
                'instructor_title',
                'stage_title',
                'reviews_title',
                'reviews_subtitle',
                'reviews_google_rating',
                'reviews_yandex_rating',
                'reviews_2gis_rating',
                'reviews_video_title',
                'start_education_title',
                'start_education_description',
                'start_education_image',
                'faq_title',
            )
        }),
    )
    