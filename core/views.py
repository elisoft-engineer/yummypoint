from django.shortcuts import render, redirect
from feedback.forms import ContactMessageForm
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from accounts.decorators import admin_required

class Index(View):
    template_name = "core/index.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"title" : "Home"})

class About(View):
    template_name = "core/about.html"
    def get(self, request, *args, **kwargs):
        return render(request, "core/about.html", {"title" : "About"})

class Contact(View):
    template_name = "core/contact.html"
    form_class = ContactMessageForm

    def get(self, request, *args, **kwargs):
        form = ContactMessageForm()
        return render(request, "core/contact.html", {
            "title" : "Contact Us",
            "form" : form,
            })
    
    def post(self, request):
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Message sent successfully")
            return redirect('index')
        
class AdminDashboard(View):
    template_name = "core/admin-dashboard.html"
    admin = None

    @method_decorator(admin_required)
    def dispatch(self, request, admin=None, *args, **kwargs):
        self.admin = admin
        return super().dispatch()
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "title" : "Admin Dashboard",
            "admin" : self.admin,
        })
        

def set_theme(request, theme):
    prev_url = request.META.get('HTTP_REFERER')
    if theme in ['light', 'dark']:
        request.session['theme'] = theme
    return redirect(prev_url)
    
def access_denied(request):
    return render(request, "core/403.html", {"title" : "403 | Access Denied"})

def not_found(request):
    return render(request, "core/404.html", {"title" : "404 | Not Found"})