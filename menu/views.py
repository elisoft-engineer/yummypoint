from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MenuCreateForm, MenuUpdateForm, ReviewForm
from .models import Menu, Category, Review
from django.urls import reverse
from django.utils.decorators import method_decorator
from accounts.decorators import customer_required, admin_required
from django.views.generic import View
from PIL import Image
from io import BytesIO
from django.core.files.storage import default_storage

class MenuList(View):
    template_name = "menu/menu.html"
    customer = None

    @method_decorator(customer_required)
    def dispatch(self, request, customer=None, *args, **kwargs):
        self.customer = customer
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "title" : "Menu",
            "items" : Menu.objects.all(),
            "categories" : Category.objects.all(),
            'user' : request.user,
        }
        return render(request, self.template_name, context)

class MenuByCategory(View):
    template_name = "menu/menu.html"
    category = None
    customer = None

    @method_decorator(customer_required)
    def dispatch(self, request, customer=None, *args, **kwargs):
        self.customer = customer
        try:
            self.category = Category.objects.get(id=kwargs.get('id'))
        except Category.DoesNotExist:
            messages.error(request, "Category not found")
            return redirect(reverse("menu"))
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        context = {
            "title" : self.category.name,
            "items" : self.category.items.all(),
            "categories" : Category.objects.all() or None,
            'user' : request.user,
        }
        messages.info(request, self.category.name)
        return render(request, self.template_name, context)

class MenuItem(View):
    template_name = "menu/menu_item.html"
    item = None
    customer = None

    @method_decorator(customer_required)
    def dispatch(self, request, customer=None, *args, **kwargs):
        self.customer = customer
        try:
            self.item = Menu.objects.get(id=kwargs.get('id'))
        except Menu.DoesNotExist:
            messages.error(request, "Menu Item not found")
            return redirect(reverse("menu"))
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title" : self.item.name,
            "item" : self.item,
        })
    
class MenuAdd(View):
    template_name = "menu/add.html"
    form_class = MenuCreateForm
    admin = None

    @method_decorator(admin_required)
    def dispatch(self, request, admin=None, *args, **kwargs):
        self.admin = admin
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title" : "Menu | Add",
            "form" : self.form_class(),
        })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data["image"]
            img = Image.open(image_file)
            size = (300, 300)
            img.thumbnail(size)
            thumb_io = BytesIO()
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(thumb_io, format='JPEG')
            form.instance.thumbnail.save(image_file.name, thumb_io, save=False)
            menu_item = form.save()
            messages.success(request, "Menu Item added successfully")
            return redirect(reverse("admin-dashboard"))
        return render(request, self.template_name, {
            "title" : "Menu | Add",
            "form" : form,
        })

class MenuUpdate(View):
    template_name = "menu/update.html"
    form_class = MenuUpdateForm
    admin = None
    item = None

    @method_decorator(admin_required)
    def dispatch(self, request, admin=None, *args, **kwargs):
        self.admin = admin
        try:
            self.item = Menu.objects.get(id=kwargs.get('id'))
        except Menu.DoesNotExist:
            messages.error("Menu Item not found")
            return redirect(reverse("admin-dashboard"))
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title" : "Menu | Update",
            "form" : self.form_class(instance=self.item),
        })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.item)
        if form.is_valid():
            if 'image' in request.FILES:
                if self.item.image:
                    old_image_path = self.item.image.path
                    default_storage.delete(old_image_path)
                image_file = form.cleaned_data["image"]
                img = Image.open(image_file)
                size = (300, 300)
                img.thumbnail(size)
                thumb_io = BytesIO()
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.save(thumb_io, format='JPEG')
                form.instance.thumbnail.save(image_file.name, thumb_io, save=False)
            menu_item = form.save()
            messages.success(request, "Menu Item added successfully")
            return redirect(reverse("admin-dashboard"))
        return render(request, self.template_name, {
            "title" : "Menu | Update",
            "form" : form,
        })
    
class MenuDelete(View):
    admin = None
    item = None

    @method_decorator(admin_required)
    def dispatch(self, request, admin=None, *args, **kwargs):
        self.admin = admin
        try:
            self.record = Menu.objects.get(id=kwargs.get("id"))
        except Menu.DoesNotExist:
            messages.error(request, "Menu Item not found")
            return redirect(reverse("menu"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.item.delete()
        messages.success(request, 'Menu Item deleted successfully')
        return redirect(reverse('menu'))

class MenuReview(View):
    template_name = "menu/review.html"
    form_class = ReviewForm
    customer = None
    item = None

    @method_decorator(customer_required)
    def dispatch(self, request, customer=None, *args, **kwargs):
        self.customer = customer
        try:
            self.item = Menu.objects.get(id=kwargs.get('id'))
        except Menu.DoesNotExist:
            messages.error(request, "Menu item not Found")
            return redirect(reverse("menu"))
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        try:
            existing_review = Review.objects.get(item=self.item, reviewer=self.customer)
            return redirect(reverse("review_update", args=[existing_review.id]))
        except Review.DoesNotExist:
            messages.info(request, f"Review {self.item.name}")
        return render(request, self.template_name, {
            "title" : "Menu | Review",
            "form" : self.form_class(),
            "item" : self.item,
        })
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = self.item
            review.reviewer = self.customer
            review.save()
            messages.success(request, "Review posted successfully")
            return redirect(reverse("menu-item", args=[self.item.id]))
        return render(request, self.template_name, {
            "title" : "Menu | Review",
            "form" : form,
            "item" : self.item,
        })
    
class ReviewUpdate(View):
    template_name = "menu/review.html"
    form_class = ReviewForm
    customer = None
    review = None

    def dispatch(self, request, customer=None, *args, **kwargs):
        self.customer = customer
        try:
            self.review = Review.objects.get(id=kwargs.get('review_id'))
        except Review.DoesNotExist:
            return redirect(reverse("menu-item", args=[kwargs.get('item_id')]))
        if self.review.item.id != kwargs.get('item_id'):
            messages.error(request, "Bad Request")
            return redirect(reverse("menu"))
        if self.review.reviewer != self.customer:
            messages.error(request, "Access Denied")
            return redirect(reverse("menu"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title" : "Review Update",
            "form" : self.form_class(),
            "item" : self.review,
        })

