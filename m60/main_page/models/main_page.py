from .base import BaseModel
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import sys
from PIL import Image

class WebPField(models.ImageField):
    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)
        if file and not file.name.lower().endswith('.webp'):
            img = Image.open(file)

            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            output = BytesIO()
            
            img.save(output, format='WEBP', quality=85)
            output.seek(0)
            
            webp_name = f"{file.name.split('.')[0]}.webp"
            
            file.save(
                webp_name,
                InMemoryUploadedFile(
                    output,
                    'ImageField',
                    webp_name,
                    'image/webp',
                    sys.getsizeof(output),
                    None
                ),
                save=False
            )
        return file
    
class PageInfo(BaseModel):    

    class Meta:
        verbose_name = "Информация главной страницы"
        verbose_name_plural = "Информация главной страницы"

    #Контакты
    telephone = models.CharField(max_length=13, verbose_name="Телефон компании")
    watsapp_link = models.URLField(verbose_name="Ссылка на WhatsApp", blank=True, null=True)
    telegram_link = models.URLField(verbose_name="Ссылка на Telegram", blank=True, null=True)

    address = models.TextField(verbose_name="Адрес компании")
    hotline_telephone = models.CharField(max_length=13, verbose_name="Горячая линия")

    #Данные первой страницы
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=100, verbose_name="Подзаголовок")
    description = models.TextField(verbose_name="Описание")
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена заявки")
    price_button = models.CharField(max_length=100, verbose_name="Текст кнопки цены заявки")
    price_description = models.CharField(max_length=100, verbose_name="Описание цены заявки")

    #Данные услуг
    services_title = models.CharField(max_length=100, verbose_name="Заголовок услуг")
    services_subtitle = models.CharField(max_length=100, verbose_name="Подзаголовок услуг")

    #Данные доп услуг
    additional_services_title = models.CharField(max_length=100, verbose_name="Заголовок доп услуг")
    additional_services_subtitle = models.CharField(max_length=100, verbose_name="Подзаголовок доп услуг")

    #Данные преимущества
    advantage_title = models.CharField(max_length=100, verbose_name="Заголовок преимущество")
    advantage_subtitle = models.CharField(max_length=100, verbose_name="Подзаголовок преимущество")

    #Данные о нас
    about_us_title = models.CharField(max_length=100, verbose_name="Заголовок о нас")
    about_us_subtitle = models.CharField(max_length=100, verbose_name="Подзаголовок о нас")
    about_us_description = models.TextField(verbose_name="Описание о нас")
    about_us_button = models.TextField(verbose_name="Текст кнопки о нас")

    #Инструкторы
    instructor_title = models.CharField(max_length=100, verbose_name="Заголовок о нас")
    instructor_subtitle = models.CharField(max_length=100, verbose_name="Подзаголовок о нас")

    #Этапы
    stage_title = models.CharField(max_length=100, verbose_name="Заголовок этапы")
    stage_subtitle = models.CharField(max_length=100, verbose_name="Подзаголовок этапы")

    #Отзывы
    reviews_title = models.CharField(max_length=100, verbose_name="Заголовок отзывы")
    reviews_subtitle = models.CharField(max_length=100, verbose_name="Подзаголовок отзывы")
    reviews_google_rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="Оценка Google")
    reviews_yandex_rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="Оценка Yandex")
    reviews_2gis_rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="Оценка 2GIS")

    #Начало обучения заявка
    start_education_title = models.CharField(max_length=100, verbose_name="Заголовок начать обучение")
    start_education_description = models.CharField(max_length=100, verbose_name="Описание начать обучение")
    start_education_image = WebPField(blank=True, null=True, upload_to='main_page/', verbose_name="Изображение начать обучение")

    #FAQ
    faq_title = models.CharField(max_length=100, verbose_name="Заголовок FAQ")

class Statistic(BaseModel):
    page = models.ForeignKey(PageInfo, on_delete=models.CASCADE, related_name="statistic_items")

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.CharField(max_length=100, verbose_name="Содержание")

class Service(BaseModel):
    page = models.ForeignKey(PageInfo, on_delete=models.CASCADE, related_name="service_items")

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    duration = models.CharField(max_length=50, verbose_name="Продолжительность")
    description = models.TextField(verbose_name="Описание услуги")
    group_start = models.CharField(max_length=100, verbose_name="Набор в группу")

    service_description_title = models.CharField(max_length=100, verbose_name="Заголовок описания услуги")
    service_desctiption_subtitle_1 = models.CharField(max_length=100, verbose_name="Подзаголовок описание услуги 1")
    service_desctiption_subtitle_2 = models.CharField(max_length=100, verbose_name="Подзаголовок описание услуги 2")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена")
    price_description = models.CharField(max_length=100,verbose_name="Описание для цены")

    confirm_button = models.CharField(max_length=100, verbose_name="Текст кнопки подтверждения")
    installment_button = models.CharField(max_length=100, verbose_name="Текст кнопки рассрочки")

    class Meta:
        verbose_name = "Курс для начинающих водителей"
        verbose_name_plural = "Курсы для начинающих водителей"

    def __str__(self):
        return self.title

class ServiceSubtitle1(BaseModel):
    course = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE,
        related_name='service_subtitle_items_1'
    )
    point = models.CharField(max_length=200, verbose_name="Пункт")

    class Meta:
        verbose_name = "Пункты под подзаголовком услуг 1"
        verbose_name_plural = "Пункты под подзаголовком услуг 1"

class ServiceSubtitle2(BaseModel):
    course = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE,
        related_name='service_subtitle_items_2'
    )
    point = models.CharField(max_length=200, verbose_name="Пункт")

    class Meta:
        verbose_name = "Пункты под подзаголовком услуг 2"
        verbose_name_plural = "Пункты под подзаголовком услуг 2"

class IncludedService(BaseModel):
    course = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='included_services'
    )
    point = models.CharField(max_length=200, verbose_name="Пункт")

    class Meta:
        verbose_name = "Включенная услуга"
        verbose_name_plural = "Включенные услуги"

class AdditionalServices(BaseModel):
    page = models.ForeignKey(PageInfo, on_delete=models.CASCADE, related_name="additional_service_items")

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена")
    price_description = models.CharField(max_length=100,verbose_name="Описание для цены")

    button = models.CharField(max_length=100,verbose_name="Текст кнопки")

class Advantage(BaseModel):
    page = models.ForeignKey(PageInfo, on_delete=models.CASCADE, related_name="advantage_items")

    TYPE_CHOICES = [
        ('small', 'Небольшая информация'),
        ('big', 'Большая информация'),
        ('image', 'Картинка'),
        ('video', 'Приведи друга'),
    ]

    advantage_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        verbose_name="Тип преимущества"
    )

    title = models.CharField(blank=True, null=True, max_length=100, verbose_name="Заголовок")
    subtitle = models.CharField(blank=True, null=True, max_length=100, verbose_name="Подзаголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = WebPField(blank=True, null=True, upload_to='advantages/',  verbose_name="Изображение")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")

    button_text = models.CharField(blank=True, null=True, max_length=100, verbose_name="Текст левой кнопки")
    detailed_button_text = models.CharField(blank=True, null=True, max_length=100, verbose_name="Текст правой кнопки")

class Instructors(BaseModel):
    page = models.ForeignKey(PageInfo, on_delete=models.CASCADE, related_name="instructors_items")

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=100, verbose_name="Подзаголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    image = WebPField(blank=True, null=True,upload_to='instructors/',  verbose_name="Изображение")

    experience = models.CharField(max_length=100,verbose_name="Стаж")

class Stages(BaseModel):
    page = models.ForeignKey(PageInfo, on_delete=models.CASCADE, related_name="stages_items")

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

class Reviews(BaseModel):
    page = models.ForeignKey(PageInfo, on_delete=models.CASCADE, related_name="reviews_items")

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="Оценка")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    date = models.DateField(verbose_name='Дата')

    TYPE_CHOICES = [
        ('2gis', '2GIS'),
        ('google', 'Google'),
        ('yandex', 'Yandex')
    ]

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        verbose_name="Место отзыва"
    )

class ReviewsVideo(BaseModel):
    page = models.ForeignKey(PageInfo, on_delete=models.CASCADE, related_name="reviews_video_items")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")

class FAQ(BaseModel):
    page = models.ForeignKey(PageInfo, on_delete=models.CASCADE, related_name="faq_items")

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")