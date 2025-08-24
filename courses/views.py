from decimal import Decimal, InvalidOperation
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Course


def _to_decimal(value):
    if not value:
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError, TypeError):
        return None


def course_list(request):
    qs = Course.objects.all()

    # Read query params
    q = (request.GET.get("q") or "").strip()
    selected_categories = request.GET.getlist("category")  # precompute for template
    selected_levels = request.GET.getlist("level")         # precompute for template
    price_min = _to_decimal(request.GET.get("price_min"))
    price_max = _to_decimal(request.GET.get("price_max"))

    # Keyword search
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    # Filters (combinable)
    if selected_categories:
        qs = qs.filter(category__in=selected_categories)

    if selected_levels:
        qs = qs.filter(level__in=selected_levels)

    if price_min is not None:
        qs = qs.filter(price__gte=price_min)

    if price_max is not None:
        qs = qs.filter(price__lte=price_max)

    context = {
        "courses": qs,
        "category_choices": Course.CATEGORIES,   # your choices
        "level_choices": Course.LEVELS,          # your choices
        # expose selected values so the template can check them (no method calls)
        "selected_categories": selected_categories,
        "selected_levels": selected_levels,
        # also echo raw values to persist inputs
        "q": q,
        "price_min": request.GET.get("price_min", ""),
        "price_max": request.GET.get("price_max", ""),
    }
    return render(request, "courses/courses.html", context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    return render(request, "courses/course_detail.html", {"course": course})
