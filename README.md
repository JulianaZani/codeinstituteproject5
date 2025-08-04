# Online Course Store for Bicycle Mechanics

## E-Commerce Planning

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
