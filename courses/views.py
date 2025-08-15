from django.shortcuts import render


def course_list(request):
    """Show a list of courses."""
    return render(request, "courses/courses.html")
