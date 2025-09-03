from decimal import Decimal
from django.conf import settings
from courses.models import Course

CART_SESSION_ID = "cart"

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if cart is None:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, course_id, quantity=1, override=False):
        course_id = str(course_id)
        if course_id not in self.cart:
            self.cart[course_id] = {"quantity": 0}
        if override:
            self.cart[course_id]["quantity"] = quantity
        else:
            self.cart[course_id]["quantity"] += quantity
        self.save()

    def remove(self, course_id):
        course_id = str(course_id)
        if course_id in self.cart:
            del self.cart[course_id]
            self.save()

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.session.modified = True

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def __iter__(self):
        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)
        for course in courses:
            item = self.cart[str(course.id)]
            quantity = item["quantity"]
            price = Decimal(course.price)
            line_total = price * quantity
            yield {
                "course": course,
                "quantity": quantity,
                "price": price,
                "line_total": line_total,
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def total(self):
        total = Decimal("0.00")
        for item in self:
            total += item["line_total"]
        return total
