# Bicycle Mechanics Courses E-commerce

## Planning

### 1. Application Type

**Type:** E-commerce platform for selling digital products (online courses)  
**Business Model:** Business-to-Consumer (B2C)  
**Payment Model:** Single-payment per course (no subscriptions)  
**Niche:** Courses aimed at bicycle mechanics, from hobbyists to professional technicians

---

### 2. Core Features

#### **User Authentication & Profiles**
- Account creation with name, email, and password  
- Login/Logout functionality  
- Profile page with purchased courses and access history  

#### **Course Catalog**
- Display of all available bicycle mechanic courses with:
  - Title and description  
  - Price  
  - Category (e.g., Basic Maintenance, Advanced Repairs, Electric Bikes)  
  - Difficulty level (Beginner, Intermediate, Advanced)  
  - Estimated course duration (hours or modules)  
  - Preview video or sample lesson (optional)  
- Search and filter functionality by category, level, or price

#### **Shopping Cart and Checkout**
- Add single or multiple courses to the cart  
- Single-payment checkout with credit card, PayPal, or other gateways  
- Instant payment confirmation and order summary

#### **Student Dashboard (Course Access Area)**
- Access to purchased courses immediately after payment  
- Video player or embedded lessons  
- Downloadable resources such as PDFs, checklists, or maintenance guides  
- Progress tracking (optional for a better learning experience)

#### **Course Reviews and Ratings**
- Students can leave feedback after completing a course  
- Display of average ratings to build trust for new buyers

#### **Notifications and Emails**
- Order confirmation email  
- Course access instructions  
- Optional marketing emails for new course launches

---

### 3. Database Structure Overview

#### **Users**
- `user_id`  
- `full_name`  
- `email`  
- `password_hash`  
- `date_joined`  

#### **Courses (Digital Products)**
- `course_id`  
- `title`  
- `description`  
- `price`  
- `thumbnail_image`  
- `category` (Basic, Advanced, Electric Bikes, etc.)  
- `difficulty_level` (Beginner, Intermediate, Advanced)  
- `duration` (in hours or modules)  
- `average_rating`  

#### **Orders**
- `order_id`  
- `user_id`  
- `order_date`  
- `total_amount`  
- `payment_status` (Paid / Pending / Failed)

#### **Order Items**
- `order_item_id`  
- `order_id`  
- `course_id`  
- `quantity` (usually 1 per course)

#### **Course Access**
- `access_id`  
- `user_id`  
- `course_id`  
- `purchase_date`  
- `progress` (optional, % of course completed)

#### **Course Reviews (optional but recommended)**
- `review_id`  
- `course_id`  
- `user_id`  
- `rating` (1-5 stars)  
- `comment`  
- `review_date`  

---

### 4. Additional Considerations
- No stock or shipping information is needed, since these are digital products  
- Focus on user experience and fast checkout, as single-payment B2C platforms rely on smooth purchasing flows  
- Consider SEO and marketing tools to reach individual bicycle mechanics searching for training  
- A responsive design is essential, as many users might access the platform from mobile devices while in workshops  

---

## **User Stories**

This document describes the **User Stories** for the product, organized by **epics**.  
Format:  
**As a** [user type] **I want** [action] **so that** [benefit].

- **Priority (MoSCoW):** Must / Should / Could / Won't  
- **Story Points:** 1, 2, 3, 5, 8, 13 (Fibonacci)  
- **Definition of Done (DoD):**
  - Code committed and passing minimum tests
  - Acceptance criteria met
  - Reviewed through Pull Request
  - Deployed to testing environment
  - Documented in README/Changelog

---

### **EPIC A – Authentication & Profile**

**US-01 – User Registration**  
- **As a** visitor **I want** to create an account with name, email, and password **so that** I can access my purchased courses.  
- **Priority:** Must | **Points:** 3  
- **Acceptance Criteria:**
  - **Given** I am on the registration screen  
    **When** I enter a valid name, email, and strong password  
    **Then** my account is created and I receive a confirmation email.  
- **Tasks:**
  - Registration form + validations
  - API endpoint for user creation + password hashing
  - Confirmation email sending

**US-02 – Login/Logout**  
- **As a** registered user **I want** to log in and log out **so that** I can securely access my student area.  
- **Priority:** Must | **Points:** 3  
- **Acceptance Criteria:**
  - **Given** I have an account  
    **When** I enter the correct email and password  
    **Then** I am authenticated and see my dashboard.  
  - **When** I click logout  
    **Then** my session is ended.  
- **Tasks:** session/token handling, protected route middleware, error feedback UI

**US-03 – User Profile**  
- **As a** user **I want** to view and edit my name and email **so that** I can keep my account information up to date.  
- **Priority:** Should | **Points:** 2  
- **Acceptance Criteria:** name can be edited; email changes require verification flow  
- **Tasks:** profile page, update endpoint, confirmation email when email is changed

---

### **EPIC B – Course Catalog**

**US-04 – Course Listing**  
- **As a** visitor **I want** to see a list of courses with title, price, category, and difficulty **so that** I can choose what to buy.  
- **Priority:** Must | **Points:** 5  
- **Acceptance Criteria:** paginated results; cards display image, price, category, difficulty  
- **Tasks:** `/courses` endpoint, responsive grid layout, pagination

**US-05 – Search and Filters**  
- **As a** visitor **I want** to search by keyword and filter by category/level/price **so that** I can quickly find relevant courses.  
- **Priority:** Must | **Points:** 5  
- **Acceptance Criteria:** filter combinations allowed; clear filters option; state reflected in URL  
- **Tasks:** query params handling, filter UI, combination testing

**US-06 – Course Details**  
- **As a** visitor **I want** to view a course page with description, duration, preview video, and reviews **so that** I can decide on a purchase.  
- **Priority:** Should | **Points:** 3  
- **Acceptance Criteria:**  
  - Course page displays title, price, description, duration, difficulty level, category, and preview video.  
  - Average rating and number of reviews (if available) are shown.  
  - “Add to Cart” button is visible and functional.  
- **Tasks:** `/courses/:id` endpoint, video player, reviews section (read-only)

---

### **EPIC C – Cart & Checkout**

**US-07 – Add to Cart**  
- **As a** user **I want** to add one or more courses to my cart **so that** I can buy them all at once.  
- **Priority:** Must | **Points:** 3  
- **Acceptance Criteria:** no duplicates; remove items; view subtotal  
- **Tasks:** cart store, mini-cart UI, local persistence

**US-08 – One-time Payment Checkout**  
- **As a** user **I want** to pay with credit card or PayPal **so that** I can get immediate access to the course.  
- **Priority:** Must | **Points:** 8  
- **Acceptance Criteria:**
  - Payment confirmation sets order status to “Paid”
  - Failure shows error message and allows retry
  - Receipt/order summary displayed after success  
- **Tasks:** payment gateway integration (sandbox), confirmation webhook, order creation

**US-09 – Confirmation Email & Receipt**  
- **As a** user **I want** to receive a confirmation email **so that** I have proof of purchase and access instructions.  
- **Priority:** Must | **Points:** 2  
- **Acceptance Criteria:** email sent within 5 minutes after payment; includes link to dashboard  
- **Tasks:** transactional email template, sending queue, magic link (optional)

---

### **EPIC D – Course Access (Student Area)**

**US-10 – Student Dashboard**  
- **As a** user **I want** to see my purchased courses **so that** I can quickly access lessons.  
- **Priority:** Must | **Points:** 3  
- **Acceptance Criteria:** list courses with progress; order by most recent  
- **Tasks:** `/me/courses` endpoint, course cards UI, progress state

**US-11 – Player & Materials**  
- **As a** user **I want** to watch video lessons and download PDFs/checklists **so that** I can study effectively.  
- **Priority:** Must | **Points:** 5  
- **Acceptance Criteria:** functional player; downloadable materials; remembers last watched lesson  
- **Tasks:** video player with time tracking, secure asset storage, progress tracking

---

### **EPIC F – Admin**

**US-15 – Course CRUD (Basic)**  
- **As an** admin **I want** to create/edit courses (title, price, category, level, duration, thumbnail) **so that** I can maintain the catalog.  
- **Priority:** Should | **Points:** 8  
- **Acceptance Criteria:** validations; image upload; save as draft or publish  
- **Tasks:** simple admin panel, protected endpoints, media storage

---

### **Non-Functional Requirements (NFRs)**

- **Security:** password hashing, HTTPS, token expiration  
- **Performance:** catalog loads in < 2s on 4G  
- **Responsiveness:** mobile-first layouts  
- **Accessibility:** proper contrast, keyboard navigation  
- **Observability:** minimal backend error logging
errors:

- OperationalError: no such table: django_site - This error occurred because I didn't run all the migrations. After running (python manage.py migrate) I was able to see:  

![register](doc/screenshots/01register.png)