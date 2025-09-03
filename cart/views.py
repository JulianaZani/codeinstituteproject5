from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from courses.models import Course
from .cart import Cart


def cart_detail(request):
    """Render the cart page with current session cart contents."""
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart": cart})

@require_POST
def add_to_cart(request, course_id):
    """Add a course to the cart (stored in session)."""
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)

    qty = request.POST.get("quantity", "1")
    try:
        qty = int(qty)
    except ValueError:
        qty = 1
    qty = max(1, qty)

    cart.add(course_id=course.id, quantity=qty)
    messages.success(request, f'"{course.title}" was added to your cart.')
    # Send the user back to where they came from, or to the cart page.
    return redirect(request.META.get("HTTP_REFERER", "cart:detail"))

@require_POST
def remove_from_cart(request, course_id):
    """Remove a course from the cart."""
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.remove(course_id=course.id)
    messages.info(request, f'"{course.title}" was removed from your cart.')
    return redirect("cart:detail")
