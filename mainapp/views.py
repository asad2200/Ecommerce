import sys
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Brand, ShippingAddress, Profile, Cart, CartItem, Order, OrderItem
from .forms import ProfileForm
from .task import creating_order

# Create your views here.


# ----------------- Home Page -----------------
class Index(TemplateView):
    template_name = "mainapp/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.order_by("-qty")[:20]
        context["products"] = products
        return context


# ----------------- Shop By Brand -----------------
class BrandCategory(ListView):
    model = Brand

    def get_context_data(self, *args, **kwargs):
        queryset = kwargs.pop("object_list", None)
        if queryset is None:
            self.object_list = self.get_queryset(*args, **kwargs)
        return super().get_context_data(**kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(BrandCategory, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("name")
        context = []
        for q in qs:
            total_brand_items = q.product_set.all().count()
            context.append(
                {
                    "brand": q,
                    "products": total_brand_items,
                }
            )
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)

        brand_id = request.POST.get("brand_id")
        if request.POST.get("sort"):
            sort = request.POST.get("sort")
            context["sort"] = sort
            if sort == "a-z":
                products = Product.objects.filter(
                    brand_id=brand_id).order_by("name")
            elif sort == "z-a":
                products = Product.objects.filter(
                    brand_id=brand_id).order_by("-name")
            elif sort == "price-hl":
                products = Product.objects.filter(
                    brand_id=brand_id).order_by("-price")
            else:
                products = Product.objects.filter(
                    brand_id=brand_id).order_by("price")
        else:
            products = Product.objects.filter(brand_id=brand_id)
        context["products"] = products
        return self.render_to_response(context)

    template_name = "mainapp/brand-category.html"


# ----------------- Shop By Category -----------------
class ItemCategory(ListView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        queryset = kwargs.pop("object_list", None)
        if queryset is None:
            self.object_list = self.get_queryset(*args, **kwargs)
        return super().get_context_data(**kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(ItemCategory, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("name")
        context = []
        for q in qs:
            total_category_items = q.product_set.all().count()
            context.append(
                {
                    "category": q,
                    "products": total_category_items,
                }
            )
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)

        category_id = request.POST.get("category_id")
        if request.POST.get("sort"):
            sort = request.POST.get("sort")
            context["sort"] = sort
            if sort == "a-z":
                products = Product.objects.filter(category_id=category_id).order_by(
                    "name"
                )
            elif sort == "z-a":
                products = Product.objects.filter(category_id=category_id).order_by(
                    "-name"
                )
            elif sort == "price-hl":
                products = Product.objects.filter(category_id=category_id).order_by(
                    "-price"
                )
            else:
                products = Product.objects.filter(category_id=category_id).order_by(
                    "price"
                )
        else:
            products = Product.objects.filter(category_id=category_id)
        context["products"] = products
        return self.render_to_response(context)

    template_name = "mainapp/item-category.html"


# ----------------- Search & All Product -----------------
class AllProducts(ListView):
    model = Product
    context_object_name = "search"

    def get_context_data(self, *args, **kwargs):
        queryset = kwargs.pop("object_list", None)
        if queryset is None:
            self.object_list = self.get_queryset(*args, **kwargs)
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        products = self.get_queryset(*args, **kwargs)

        if request.GET.get("q"):
            search = request.GET.get("q")
            products = Product.objects.filter(name__icontains=search)
            products2 = Product.objects.filter(brand__name__icontains=search)
            products = products | products2
        if request.GET.get("sort"):
            sort = request.GET.get("sort")
            context["sort"] = sort
            if sort == "a-z":
                products = products.order_by("name")
            elif sort == "z-a":
                products = products.order_by("-name")
            elif sort == "price-hl":
                products = products.order_by("-price")
            else:
                products = products.order_by("price")

        context["products"] = products
        return self.render_to_response(context)

    template_name = "mainapp/all-products.html"


# ----------------- Single Product View -----------------
class ProductView(TemplateView):
    template_name = "mainapp/product.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        id = kwargs.get("id")
        product = Product.objects.get(id=id)
        similar_products = Product.objects.filter(brand=product.brand)[:4]
        similar_products2 = Product.objects.filter(
            category=product.category)[:5]
        similar_products = similar_products | similar_products2
        context["product"] = product
        context["similar_product"] = similar_products
        return self.render_to_response(context)


# ----------------- USER REGISTRATION -----------------
def get_user_detail(request, key):
    return request.POST.get(key)


def check_user(request):
    try:
        User.objects.get(username=get_user_detail(request, "username"))
        messages.add_message(
            request,
            messages.ERROR,
            "Username already exists try with different.",
        )
        return False
    except User.DoesNotExist:
        pass
    try:
        User.objects.get(email=get_user_detail(request, "email"))
        messages.add_message(
            request,
            messages.ERROR,
            "email already exists try with different.",
        )
        return False
    except User.DoesNotExist:
        pass

    return True


def register(request):
    if request.method == "POST":
        if not check_user(request):
            return redirect("register")
        try:
            user = User.objects.create_user(
                username=get_user_detail(request, "username"),
                email=get_user_detail(request, "email"),
                password=get_user_detail(request, "password"),
                first_name=get_user_detail(request, "first_name"),
                last_name=get_user_detail(request, "last_name"),
            )
            user.save()
            try:
                shipping_addr = ShippingAddress.objects.create(
                    address_1=get_user_detail(request, "address1"),
                    address_2=get_user_detail(request, "address2"),
                    country=get_user_detail(request, "country"),
                    state=get_user_detail(request, "state"),
                    city=get_user_detail(request, "city"),
                    zipcode=get_user_detail(request, "zipcode"),
                )
                try:
                    profile = Profile.objects.create(
                        user_id=user,
                        mobile_no1=get_user_detail(request, "mobile1"),
                        mobile_no2=get_user_detail(request, "mobile2"),
                    )
                    profile.shipping_address.add(shipping_addr)
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        "User created Succesfully !!",
                    )
                    return redirect("login")
                except:
                    user.delete()
                    shipping_addr.delete()
                    return HttpResponse(
                        "unexpected error occurred in 'Profile'!! try again..."
                    )
            except:
                user.delete()
                return HttpResponse(
                    "unexpected error occurred 'Shipping address'!! try again..."
                )
        except:
            return HttpResponse("unexpected error occurred 'User'!! try again...")
    else:
        return render(request, "mainapp/register.html")


# ----------------- Login -----------------
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("index")
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Credentials are not correct.",
            )
    return render(request, "mainapp/login.html")


# ----------------- Logout -----------------
def logout(request):
    auth_logout(request)
    return redirect("index")


# ----------------- Profile View -----------------
class ProfileView(TemplateView):
    template_name = "mainapp/profile-view.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile = Profile.objects.get(user_id=request.user)
        shipping_addr = profile.shipping_address.all()[0]
        context["profile"] = profile
        context["shipping_addr"] = shipping_addr
        return self.render_to_response(context)


# ----------------- Profile Edit -----------------
class ProfileEdit(FormView):
    template_name = "mainapp/profile-edit.html"
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile = Profile.objects.get(user_id=request.user)
        shipping_addr = profile.shipping_address.all()[0]
        context["profile"] = profile
        context["shipping_addr"] = shipping_addr
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # if not self.form_valid(request.):

        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user_id=user)
        shipping_addr = profile.shipping_address.all()[0]

        # User Update
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()
        # ShippingAddress Update
        shipping_addr.address_1 = request.POST.get("address_1")
        shipping_addr.address_2 = request.POST.get("address_2")
        shipping_addr.country = request.POST.get("country")
        shipping_addr.state = request.POST.get("state")
        shipping_addr.city = request.POST.get("city")
        shipping_addr.zipcode = request.POST.get("zipcode")
        shipping_addr.save()

        # Profile Update
        profile.mobile_no1 = request.POST.get("mobile_no1")
        profile.mobile_no2 = request.POST.get("mobile_no2")
        try:
            profile.save()
        except:
            return HttpResponse("Mobile no. should be unique")

        return redirect("profile-view")


# ----------------- Cart View -----------------
@login_required(login_url="login")
def cart_view(request):
    context = {}
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        context["cart_items"] = cart_items
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        pass
    return render(request, "mainapp/cart.html", context)


# ----------------- Cart View -----------------
class CartAdd(FormView):
    def get(self, request, *args, **kwargs):
        try:
            User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return JsonResponse({'login': "Login is required"}, safe=True)
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart.save()
            product = Product.objects.get(id=kwargs.get("id"))
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product)
            cart_item.qty += 1
            cart_item.save()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return JsonResponse({'error': "Unexpected error occured !! try again.."}, safe=True)
        return JsonResponse({'success': 'Product added in cart succesfully'}, safe=True)


# ----------------- Cart View -----------------
@login_required(login_url="login")
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart)[0]
    except:
        return render(request, "mainapp/cart.html")
    creating_order.delay(request.user.id, request.user.email)
    return HttpResponse("Order confirmation mail sent on youe email. <a href='/'>Home Page</a>")
