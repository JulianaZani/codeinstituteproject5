from decimal import Decimal
from courses.models import Course

CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if cart is None:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, course_id):
        course_id = str(course_id)
        if course_id not in self.cart:
            course = Course.objects.get(pk=course_id)
            self.cart[course_id] = {
                "price": str(course.price),
            }
            self.save()

    def remove(self, course_id):
        course_id = str(course_id)
        if course_id in self.cart:
            del self.cart[course_id]
            self.save()

    def __iter__(self):
        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)
        for course in courses:
            item = self.cart[str(course.id)]
            price = Decimal(item["price"])
            yield {
                "course": course,
                "price": price,
                "line_total": price,
            }

    def __len__(self):
        return len(self.cart)

    def total(self):
        total = Decimal("0.00")
        for item in self:
            total += item["line_total"]
        return total

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()
