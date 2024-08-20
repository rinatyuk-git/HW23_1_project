from datetime import date

from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    category_name = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории",
    )  # Наименование
    category_info = models.TextField(
        max_length=1255,
        verbose_name="Информация о категории",
        help_text="Введите информацию о категории",
    )  # Описание

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(
        max_length=100,
        verbose_name="Название продукта",
        help_text="Введите название продукта",
        unique=True,
        **NULLABLE,
    )  # Наименование
    product_info = models.TextField(
        max_length=1255,
        verbose_name="Информация о продукте",
        help_text="Введите информацию о продукте",
    )  # Описание
    product_image = models.ImageField(
        upload_to="product/images",
        verbose_name="Изображение продукта",
        help_text="Загрузите изображение продукта",
        **NULLABLE,
    )  # Изображение (превью)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Выберите категорию продукта",
        related_name="products",
        **NULLABLE,
    )  # pass # Категория
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена продукта",
        help_text="Задайте цену продукта",
    )  # Цена за покупку
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата внесения продукта",
        help_text="Задайте дату внесения продукта",
    )  # Дата создания (записи в БД)
    updated_at = models.DateField(
        auto_now=True,
        verbose_name="Дата последнего изменения продукта",
        help_text="Задайте дату последнего изменения продукта",
    )  # Дата последнего изменения (записи в БД)
    manufactured_at = models.DateField(
        default=date.today(),
        verbose_name="Дата производства продукта",
        help_text="Задайте дату производства продукта",
    )  # Дата производства продукта

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Создатель",
        **NULLABLE,
    )  # Создатель продукта

    is_published = models.BooleanField(
        default=False, verbose_name="Признак публикации"
    )  # признак публикации

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["product_name", "category"]
        permissions = [
            ('can_cancel_publication', 'Can cancel publication'),  # is_published
            ('can_edit_description', 'Can edit description'),  # product_info
            ('can_edit_category', 'Can edit category'),  # category
        ]  # отменять публикацию продукта, менять описание любого продукта, категорию любого продукта.

    def __str__(self):
        return self.product_name


class Version(models.Model):
    product_name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Название продукта",
        related_name="versions",
    )  # продукт

    version_number = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name="Номер версии",
        help_text="Задайте номер версии",
    )  # номер версии

    version_name = models.CharField(
        max_length=100,
        verbose_name="Название версии",
        help_text="Введите название версии",
        unique=True,
    )  # Название версии

    is_actual = models.BooleanField(
        default=True, verbose_name="Признак текущей версии"
    )  # признак текущей версии

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ["version_name", "version_number"]

    def __str__(self):
        return self.version_name
