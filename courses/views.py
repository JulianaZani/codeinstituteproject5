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
    base_qs = Course.objects.all() if request.user.is_staff else Course.objects.filter(is_active=True)
    qs = base_qs

    q = (request.GET.get("q") or "").strip()
    selected_categories = request.GET.getlist("category")
    selected_levels = request.GET.getlist("level")
    price_min = _to_decimal(request.GET.get("price_min"))
    price_max = _to_decimal(request.GET.get("price_max"))

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    if selected_categories:
        qs = qs.filter(category__in=selected_categories)

    if selected_levels:
        qs = qs.filter(level__in=selected_levels)

    if price_min is not None:
        qs = qs.filter(price__gte=price_min)

    if price_max is not None:
        qs = qs.filter(price__lte=price_max)

    sort = (request.GET.get("sort") or "").strip()
    allowed_sorts = {
        "title": "title",
        "-title": "-title",
        "price": "price",
        "-price": "-price",
        "duration_hours": "duration_hours",
        "-duration_hours": "-duration_hours",
    }
    if sort in allowed_sorts:
        qs = qs.order_by(allowed_sorts[sort])

    context = {
        "courses": qs,
        "category_choices": Course.CATEGORIES,
        "level_choices": Course.LEVELS,
        "selected_categories": selected_categories,
        "selected_levels": selected_levels,
        "q": q,
        "price_min": request.GET.get("price_min", ""),
        "price_max": request.GET.get("price_max", ""),
        "current_sort": sort,
    }
    return render(request, "courses/courses.html", context)


def course_detail(request, slug):
    base_qs = Course.objects.all() if request.user.is_staff else Course.objects.filter(is_active=True)
    course = get_object_or_404(base_qs, slug=slug)

    related_courses = (
        base_qs.filter(category=course.category)
               .exclude(pk=course.pk)[:3]
    )

    return render(
        request,
        "courses/course_detail.html",
        {"course": course, "related_courses": related_courses},
    )
