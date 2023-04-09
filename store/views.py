from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .models import Product, ReviewRating
from category.models import Category
from carts.models import Cart, CartItem
from orders.models import OrderProduct
from carts.views import _cart_id
from .forms import ReviewForm
from django.contrib import messages

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('price')
        paginator = Paginator(products, 6, orphans=0, allow_empty_first_page=True)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('price')
        # print("Categoria richiesta = {}".format(category_slug))
        paginator = Paginator(products, 6, orphans=0, allow_empty_first_page=True)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)


    products_count = products.count()

    context = {
        'products': paged_products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,
                                             slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        # return HttpResponse("The product {} is in Cart ? : {}".format(single_product.product_name, in_cart))
        # exit()
    except Exception as e:
        raise e
    # if request.usert.is_authenticated:

    try:
        orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    # except Exception as e:
    except OrderProduct.DoesNotExist:
        orderproduct = None
    except TypeError:
        orderproduct = None
        # raise e
    # else:
    #     orderproduct = None

    # Get the reviews for the product
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    average_rating: float = 0
    reviews_count: int = 0
    for review in reviews:
        reviews_count += 1
        average_rating += review.rating
    average_rating = average_rating / reviews_count




    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct'  : orderproduct,
        'reviews'       : reviews,
        'average_rating': average_rating,
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        prouct_count:int = 0
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(product_name__icontains=keyword))
            product_count = products.count()
        context = {
            'products'  :   products,
            'products_count' : product_count,
            'search_keyword' : keyword,
        }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you bastard! Your fucking review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you bastard! Your fucking review has been submitted')
                return redirect(url)
