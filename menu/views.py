from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MenuCreateForm, MenuUpdateForm, ReviewForm
from .models import Menu, Category, Review
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

class Menu(View):
    def get(self, request, *args, **keargs):
        context = {
            "title" : "Menu",
            "items" : Menu.objects.all(),
            "categories" : Category.objects.all(),
            'user' : request.user,
        }
        return render(request, "menu/menu.html", context)

class MenuByCategory(View):
    category = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(id=kwargs.get('id'))
        except Category.DoesNotExist:
            messages.error(request, "Category not found")
            return redirect()
        return super().dispatch(request, *args, **kwargs)

def menu_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if category is not None:
        context = {
            "title" : "Menu",
            "items" : category.items.all(),
            "categories" : Category.objects.all(),
            'user' : request.user,
        }
        messages.info(request, f"{category.name}")
        return render(request, "menu/menu.html", context)
    else:
        return redirect("menu")

def menu_item(request, id):
    item = get_object_or_404(Menu, id=id)
    if item is not None:
        context = {
            "title" : item.name,
            "item" : item,
        }
        return render(request, "menu/menu_item.html", context)
    else:
        return redirect('not_found')

@login_required
def add(request):
    if not request.user.is_staff:
        return redirect("access_denied")
    if request.method == 'POST':
        form = MenuCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Menu Item added successfully")
            return redirect('menu_add')
    else:
        form = MenuCreateForm()
    return render(request, "menu/add.html", { "title" : "Menu | Add", "form" : form})

@login_required
def update(request, id):
    if not request.user.is_staff:
        return redirect("access_denied")
    item = get_object_or_404(Menu, id=id)
    if request.method == 'POST':
        if item is not None:
            form = MenuUpdateForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, f"Menu Item Updated Successfully")
                return redirect('menu')
        else:
            messages.error(request, f"Menu Item with the id {id} does not exist")
            return redirect('menu')
    else:
        form = MenuUpdateForm(instance=item)
    return render(request, "menu/update.html", { "title" : "Menu | Update", "form" : form})

def delete(request, id):
    if not request.user.is_staff:
        return redirect("access_denied")
    item = get_object_or_404(Menu, id=id)
    if item is not None:
        item.delete()
        messages.success(request, f"Menu Item deleted successfully")
        return redirect("menu")
    messages.info(request, f"Menu Item doesnt exist")
    return redirect("menu")

@login_required
def review(request, item_id):
    user = request.user
    try:
        item = Menu.objects.get(id=item_id)
    except Menu.DoesNotExist:
        return redirect("not_found")
    
    try:
        existing_review = Review.objects.get(item=item, reviewer=user)
        return redirect(reverse("review_update", args=[existing_review.id]))
    except Review.DoesNotExist:
        messages.info(request, f"Review {item.name}")

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.reviewer = user
            review.save()
            messages.success(request, f"Review added successfully")
            return redirect(reverse("menu_item", args=[item_id]))
    else:
        form = ReviewForm()
    return render(request, "menu/review.html", {
        "title" : "Menu | Review",
        "form" : form,
        "item" : item,
    })

@login_required
def review_update(request, review_id):
    try:
        review_item = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        messages.error(request, "Review not found")
        return redirect("not_found")
    if review_item.reviewer.username != request.user.username:
        return redirect("access_denied")
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully")
            return redirect(reverse("menu_item", args=[review_item.item.id]))
    else:
        form = ReviewForm(instance=review_item)
    return render(request, "menu/review.html", {
        "title" : "Menu | Review",
        "form" : form,
        "item" : review_item,
    })
        

