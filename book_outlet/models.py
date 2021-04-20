from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
# from django.utils.text import slugify


# Create your models here.
# python3 manage.py shell
# python3 manage.py makemigrations
# python3 manage.py migrate
# python3 manage.py runserver
# from book_outlet.models import Book, Author

class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name} ({self.code}"

    class Meta:
        verbose_name_plural = 'Countries'


class Address(models.Model):
    street = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.address_text()

    def address_text(self):
        return f"{self.street}  {self.city}, Zip: {self.postal_code}"

    class Meta:
        verbose_name_plural = 'Address Entries'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, related_name='address')
    # .books.all()

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_name}  {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    # author = models.CharField(null=True, max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='books')
    is_bestselling = models.BooleanField(default=False)
    # blank=False editable=False
    slug = models.SlugField(default='', null=False, db_index=True)
    published_countries = models.ManyToManyField(Country, related_name='books')

    def get_absolute_url(self):
        return reverse('book-detail', args=[self.slug])

    # def save(self, *args, **kwargs):
    #    self.slug = slugify(self.title)
    #    super().save(*args, **kwargs)

    # id = models.AutoField()

    def __str__(self):
        return f"{self.title} ({self.rating})"
