"""
Django Admin Sayt Qo'llanmasi
Bu fayl Django Admin interfeysi uchun turli funksiyalar va sozlashlarni namoyish etadi
"""

from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe


# ------ MODEL TA'RIFLARI ------

class Person(models.Model):
    """Asosiy ma'lumotlar bilan Shaxs modeli"""
    first_name = models.CharField(max_length=50)  # Ism
    last_name = models.CharField(max_length=50)  # Familiya
    birthday = models.DateField(blank=True, null=True)  # Tug'ilgan sana
    color_code = models.CharField(max_length=6)  # Rang kodi (namoyish uchun)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_address(self):
        """Manzilni ko'rsatish uchun misol metodi"""
        return [f"{self.first_name} {self.last_name}", "123 Django St", "Admin City"]

    @property
    def full_name(self):
        """To'liq ism xususiyati admin uchun sozlash bilan"""
        return f"{self.first_name} {self.last_name}"

    # Admin ko'rinishi uchun xususiyatni sozlash
    full_name.short_description = "Shaxsning to'liq ismi"
    full_name.admin_order_field = "last_name"
    full_name.boolean = False

    @admin.display(boolean=True)
    def born_in_fifties(self):
        """Admin panelida boolean qiymat ko'rinishi misoli"""
        if self.birthday:
            return 1950 <= self.birthday.year < 1960
        return False

    @admin.display(ordering="first_name", description="Rangli Ism")
    def colored_name(self):
        """Admin ko'rinishida HTML formatlash misoli"""
        return format_html(
            '<span style="color: #{};">{} {}</span>',
            self.color_code,
            self.first_name,
            self.last_name,
        )

    @admin.display(ordering=Concat("first_name", Value(" "), "last_name"))
    def complex_ordering_example(self):
        """Admin ko'rinishida murakkab tartibga solish misoli"""
        return f"{self.first_name} {self.last_name}"

    @admin.display(description="Tug'ilgan o'n yillik")
    def decade_born_in(self):
        """Ko'rinish uchun maxsus tavsif va hisoblash misoli"""
        if self.birthday:
            decade = self.birthday.year // 10 * 10
            return f"{decade}'s"
        return None


class Group(models.Model):
    """Person bilan ko'p-ko'plikka bog'langan Guruh modeli"""
    name = models.CharField(max_length=128)  # Nom
    members = models.ManyToManyField(Person, through="Membership", related_name="groups")  # A'zolar

    def __str__(self):
        return self.name


class Membership(models.Model):
    """Person-Group ko'p-ko'plik bog'lanish modeli"""
    person = models.ForeignKey(Person, on_delete=models.CASCADE)  # Shaxs
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # Guruh
    date_joined = models.DateField()  # Qo'shilgan sana
    invite_reason = models.CharField(max_length=64)  # Taklif sababi

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "group"], name="unique_person_group"
            )  # Har bir shaxs guruhga bir marta qo'shilishi mumkin
        ]


class Author(models.Model):
    """Kitob bilan bog'lanish uchun Muallif modeli"""
    name = models.CharField(max_length=100)  # Ism
    title = models.CharField(max_length=3)  # Unvon (Dr., Mr., Mrs.)
    birth_date = models.DateField(blank=True, null=True)  # Tug'ilgan sana

    def __str__(self):
        return self.name


class Book(models.Model):
    """Muallif bilan bog'langan Kitob modeli"""
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Muallif
    title = models.CharField(max_length=100)  # Sarlavha
    pub_date = models.DateField(blank=True, null=True)  # Nashr sanasi

    def __str__(self):
        return self.title


class Friendship(models.Model):
    """O'ziga bog'langan model (self-reference) misoli"""
    from_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="friends")  # Kimdan
    to_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="from_friends")  # Kimga

    def __str__(self):
        return f"{self.from_person} → {self.to_person}"


class ContentType(models.Model):
    """GenericForeignKey misoli uchun ContentType modeli"""
    name = models.CharField(max_length=100)  # Nom

    def __str__(self):
        return self.name


class Image(models.Model):
    """Umumiy bog'lanish model misoli"""
    image = models.ImageField(upload_to="images")  # Rasm
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Bog'lanish turi
    object_id = models.PositiveIntegerField()  # Bog'langan obyekt ID
    content_object = GenericForeignKey("content_type", "object_id")  # Bog'lanish

    def __str__(self):
        return f"Image for {self.content_object}"


class Product(models.Model):
    """Umumiy bog'lanish uchun Mahsulot modeli"""
    name = models.CharField(max_length=100)  # Nom

    def __str__(self):
        return self.name


class Article(models.Model):
    """Media misoli uchun Maqola modeli"""
    title = models.CharField(max_length=100)  # Sarlavha
    content = models.TextField()  # Matn
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)  # Foydalanuvchi

    def __str__(self):
        return self.title


class MyModel(models.Model):
    """Maxsus AdminSite uchun model misoli"""
    name = models.CharField(max_length=100)  # Nom

    def __str__(self):
        return self.name


class Blog(models.Model):
    """Bog'langan tartibga solish misoli uchun Blog modeli"""
    title = models.CharField(max_length=255)  # Sarlavha
    author = models.ForeignKey(Person, on_delete=models.CASCADE)  # Muallif

    def __str__(self):
        return self.title


# ------ FORMALAR VA VIDJETLAR ------

class RichTextEditorWidget(forms.Textarea):
    """Forma maydoni uchun maxsus vidjet misoli"""

    def __init__(self, attrs=None):
        default_attrs = {"class": "rich-text-editor"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class PersonForm(forms.ModelForm):
    """Maxsus ModelForm misoli"""

    class Meta:
        model = Person
        exclude = ["name"]  # Misol uchun chiqarib tashlash


class CountryAdminForm(forms.ModelForm):
    """__init__ da so'rov to'plamini sozlash misoli"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'cities'):
            self.fields["capital"].queryset = self.instance.cities.all()


class MyArticleAdminForm(forms.ModelForm):
    """Maxsus tekshirish bilan forma misoli"""

    class Meta:
        model = Article
        fields = '__all__'

    def clean_name(self):
        """Nom maydonini tekshirish"""
        name = self.cleaned_data["name"]
        # Misol tekshirish
        if len(name) < 5:
            raise forms.ValidationError("Nom kamida 5 ta belgidan iborat bo'lishi kerak")
        return name


class MySuperuserForm(forms.ModelForm):
    """Superuser uchun maxsus forma"""

    class Meta:
        model = MyModel
        fields = '__all__'

    # Superuserlar uchun qo'shimcha maydonlar
    is_featured = forms.BooleanField(required=False)


class MyAdminFormSet(forms.BaseModelFormSet):
    """O'zgarishlar ro'yxati uchun maxsus forma to'plami"""

    def clean(self):
        """Butun to'plam uchun tekshirish"""
        super().clean()
        for form in self.forms:
            # Tekshirish logikasi misoli
            pass


# ------ ADMIN INLINE'LAR ------

class BookInline(admin.TabularInline):
    """Muallif adminidagi kitoblar uchun TabularInline"""
    model = Book
    extra = 1  # Ko'rsatiladigan bo'sh formalar soni
    # raw_id_fields = ["pages"]  # raw_id_fields ishlatish misoli


class FriendshipInline(admin.TabularInline):
    """Belgilangan tashqi kalit bilan inline misoli"""
    model = Friendship
    fk_name = "to_person"  # Inline uchun qaysi FK ishlatilishini belgilash
    extra = 1


class MembershipInline(admin.TabularInline):
    """Maxsus orqali model uchun inline"""
    model = Membership
    extra = 1


class ImageInline(GenericTabularInline):
    """GenericTabularInline misoli"""
    model = Image
    extra = 1


class BinaryTreeAdmin(admin.TabularInline):
    """Dinamik qo'shimcha formalar bilan inline misoli"""
    model = Book  # BinaryTree o'rniga Book ishlatilmoqda

    def get_extra(self, request, obj=None, **kwargs):
        """Qo'shimcha formalar sonini dinamik hisoblash"""
        extra = 2
        if obj:
            # Misol: obyekt bog'langan elementlarga ega bo'lsa, kamroq forma qaytarish
            return extra - min(obj.book_set.count(), extra)
        return extra

    def get_max_num(self, request, obj=None, **kwargs):
        """Maksimal formalar sonini dinamik hisoblash"""
        max_num = 10
        if obj and hasattr(obj, 'parent') and obj.parent:
            return max_num - 5
        return max_num


# ------ ADMIN SINFLARI ------

class PersonAdmin(admin.ModelAdmin):
    """Ko'p funksiyali admin misoli"""
    # Ko'rinish sozlamalari
    list_display = ["first_name", "last_name", "colored_name", "born_in_fifties", "decade_born_in", "full_name"]
    search_fields = ["first_name", "last_name"]
    date_hierarchy = "birthday"
    empty_value_display = "noma'lum"

    # Maydonlar sozlamalari
    fields = ["first_name", "last_name", "birthday", "color_code"]
    # exclude = ["color_code"]  # fields ga muqobil

    # Maydon guruhlari misoli
    fieldsets = [
        (
            "Asosiy Ma'lumotlar",
            {
                "fields": ["first_name", "last_name"],
            },
        ),
        (
            "Qo'shimcha Ma'lumotlar",
            {
                "classes": ["collapse"],
                "fields": ["birthday", "color_code"],
            },
        ),
    ]

    # Inline'lar
    inlines = [FriendshipInline, MembershipInline]

    # Maxsus forma
    form = PersonForm

    # Faqat o'qish uchun maydonlar
    readonly_fields = ["address_report"]

    # Site'da ko'rish imkoniyatini o'chirish
    view_on_site = False

    # Media misoli
    class Media:
        css = {
            "all": ["my_styles.css"],
        }
        js = ["my_code.js"]

    @admin.display(description="Manzil")
    def address_report(self, instance):
        """Manzilni HTML formatida ko'rsatish"""
        return format_html_join(
            mark_safe("<br>"),
            "{}",
            ((line,) for line in instance.get_full_address()),
        ) or mark_safe("<span class='errors'>Manzil aniqlanmadi.</span>")

    def get_readonly_fields(self, request, obj=None):
        """Foydalanuvchiga qarab faqat o'qish uchun maydonlarni aniqlash"""
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly.append("color_code")
        return readonly

    def get_ordering(self, request):
        """Foydalanuvchi huquqlariga qarab tartiblash"""
        if request.user.is_superuser:
            return ["first_name", "last_name"]
        else:
            return ["last_name"]

    def get_search_results(self, request, queryset, search_term):
        """Maxsus qidiruv amalga oshirish"""
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        # Qidiruv funksiyasini kengaytirish misoli
        try:
            search_term_as_int = int(search_term)
            # Yosh bo'yicha qidirish (tug'ilgan sanadan hisoblanadi)
            # Bu faqat misol - to'g'ri ishlashi uchun ko'proq kod kerak
        except ValueError:
            pass
        return queryset, may_have_duplicates

    def get_changeform_initial_data(self,request):
        """Provide initial data for new objects"""
        return {"first_name": "New", "last_name": "Person"}

    def get_urls(self):
        """Add custom URLs to the admin"""
        urls = super().get_urls()
        my_urls = [path("my_view/", self.admin_site.admin_view(self.my_view))]
        return my_urls + urls

    def my_view(self, request):
        """Custom view in admin"""
        context = dict(
            self.admin_site.each_context(request),
            title="My Custom View",
        )
        return TemplateResponse(request, "admin/my_custom_view.html", context)

    def get_queryset(self, request):
        """Filter queryset based on user"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Example: non-superusers see only certain records
        return qs.filter(groups__name="Public")


class AuthorAdmin(admin.ModelAdmin):
    """Admin for Author model with simpler configuration"""
    list_display = ["name", "title", "view_birth_date"]
    date_hierarchy = "birth_date"
    inlines = [BookInline]

    @admin.display(empty_value="???")
    def view_birth_date(self, obj):
        """Custom display for birth date with empty value handling"""
        return obj.birth_date


class GroupAdmin(admin.ModelAdmin):
    """Admin for Group model"""
    inlines = [MembershipInline]
    exclude = ["members"]  # Hide the direct M2M field since we're using the through inline


class ProductAdmin(admin.ModelAdmin):
    """Admin with generic inline example"""
    inlines = [ImageInline]


class BlogAdmin(admin.ModelAdmin):
    """Admin with ordering by related field"""
    list_display = ["title", "author", "author_first_name"]

    @admin.display(ordering="author__first_name")
    def author_first_name(self, obj):
        """Display and order by related field"""
        return obj.author.first_name


class ArticleAdmin(admin.ModelAdmin):
    """Admin with save_model example"""
    def save_model(self, request, obj, form, change):
        """Customize object saving"""
        # Example: save current user when saving article
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """Customize formset saving"""
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            # Example: set user for related objects
            instance.user = request.user
            instance.save()
        formset.save_m2m()

