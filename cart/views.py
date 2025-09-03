from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from courses.models import Course
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart": cart})

@require_POST
def add_to_cart(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)

    if not course.is_active and not request.user.is_staff:
        messages.error(request, f'"{course.title}" is not available at the moment.')
        return redirect(request.META.get("HTTP_REFERER", "cart:detail"))

    qty = request.POST.get("quantity", "1")
    try:
        qty = int(qty)
    except ValueError:
        qty = 1
    qty = max(1, qty)

    cart.add(course_id=course.id, quantity=qty)
    messages.success(request, f'"{course.title}" was added to your cart.')
    return redirect(request.META.get("HTTP_REFERER", "cart:detail"))

@require_POST
def remove_from_cart(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.remove(course_id=course.id)
    messages.info(request, f'"{course.title}" was removed from your cart.')
    return redirect("cart:detail")
