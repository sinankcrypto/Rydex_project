# 🛍️ Rydex — Riding Accessories E-Commerce Platform

Rydex is a full-featured **riding accessories e-commerce web application** built with Django. It provides a complete online shopping experience, from product discovery and cart management to secure payments, order tracking, returns, refunds, and wallet management.

The platform also includes a dedicated **admin dashboard** for managing products, categories, users, orders, offers, coupons, and sales analytics.

The application was developed with a focus on building a realistic e-commerce workflow and implementing core backend concepts such as authentication, authorization, payment processing, order lifecycle management, inventory management, and financial transactions.

---

## ✨ Features

### 👤 User Features

* User registration and authentication
* OTP-based account verification
* Email-based authentication workflows
* Password reset functionality
* User profile management
* Address management
* User account blocking/unblocking support
* Secure session-based authentication

### 🛍️ Product Management

* Browse available products
* Product detail pages
* Category-based product browsing
* Product variants
* Size-based inventory management
* Stock availability tracking
* Product image management
* Product search and filtering
* Category management

### 🛒 Shopping Cart

* Add products to cart
* Update product quantities
* Remove products from cart
* Variant-specific cart management
* Stock validation
* Automatic price calculation
* Offer-aware cart pricing
* Cart total calculation

### ❤️ Wishlist

* Add products to wishlist
* Remove products from wishlist
* View wishlist
* Manage wishlist products

### 🏷️ Offers & Discounts

* Product-level offers
* Category-level offers
* Coupon management
* Coupon application during checkout
* Discount calculation
* Offer validity management
* Expiry date handling
* Discount limits and validation

### 💳 Payments

* Razorpay payment integration
* Cash on Delivery
* Payment status tracking
* Payment verification
* Secure order creation after successful payment
* Payment failure handling

### 📦 Order Management

* Place orders
* View order history
* View individual order details
* Order status tracking
* Order tracking IDs
* Cancel orders
* Order cancellation handling
* Order status management

### ↩️ Returns & Refunds

* Request product returns
* Return request management
* Admin return approval/rejection
* Refund processing
* Wallet-based refunds
* Return status tracking

### 💰 Wallet

* User wallet
* Wallet balance management
* Wallet transactions
* Refunds credited to wallet
* Transaction history

### 🧾 Invoices & Reports

* Generate downloadable PDF invoices
* Sales report generation
* PDF sales reports
* Excel sales reports
* Date-based sales reporting
* Order and revenue statistics

### 👨‍💼 Admin Dashboard

Administrators can manage the entire e-commerce platform through a dedicated admin interface.

* Admin authentication
* Dashboard overview
* User management
* Block/unblock users
* Product management
* Product variant management
* Category management
* Offer management
* Coupon management
* Order management
* Order status updates
* Return request management
* Sales reports
* PDF report generation
* Excel report generation

---

## 🛠️ Tech Stack

### Backend

* **Python**
* **Django 5.1.4**
* **Django Allauth**
* **Django Crispy Forms**

### Database

* **PostgreSQL**

### Frontend

* **HTML5**
* **CSS3**
* **JavaScript**
* **Bootstrap**
* **Django Templates**

### Payments

* **Razorpay**

### Media & Image Processing

* **Pillow**

### Reports & Documents

* **ReportLab**
* **xhtml2pdf**
* **OpenPyXL**

### Communication

* **Twilio**
* Email services

### Production & Deployment

* **AWS EC2**
* **Gunicorn**
* **Nginx**
* **PostgreSQL**

---

## 🏗️ Application Architecture

Rydex follows Django's **MVT (Model-View-Template)** architecture.

The application is organized into dedicated Django apps responsible for different areas of the platform.

```text
Rydex_project/
│
├── Rydex/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── user_auth/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── products/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── cart/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── orders/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── payments/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
└── ...
```

> The exact application structure may vary depending on the current version of the repository.

---

## 🔄 E-Commerce Workflow

The typical customer journey in Rydex is:

```text
User Registration
       │
       ▼
OTP Verification
       │
       ▼
Browse Products
       │
       ▼
Select Product Variant
       │
       ▼
Add to Cart / Wishlist
       │
       ▼
Apply Offer / Coupon
       │
       ▼
Checkout
       │
       ├───────────────┐
       ▼               ▼
Razorpay          Cash on Delivery
       │               │
       └───────┬───────┘
               ▼
        Order Creation
               │
               ▼
        Order Processing
               │
               ▼
          Order Delivery
               │
          ┌────┴────┐
          ▼         ▼
       Cancel     Return
                    │
                    ▼
                Refund
                    │
                    ▼
              User Wallet
```

---

## 💳 Payment Flow

Rydex integrates **Razorpay** for online payments.

The payment workflow follows the general flow:

```text
User Checkout
      │
      ▼
Create Payment Order
      │
      ▼
Redirect / Open Razorpay Checkout
      │
      ▼
User Completes Payment
      │
      ▼
Verify Payment
      │
      ├── Successful ──► Create / Confirm Order
      │
      └── Failed ──────► Handle Payment Failure
```

The application also supports **Cash on Delivery** for eligible orders.

---

## 💰 Wallet & Refund Flow

The wallet system is used to maintain user balances and handle refunds.

For example:

```text
Order
  │
  ▼
Return Request
  │
  ▼
Admin Approval
  │
  ▼
Refund Processed
  │
  ▼
Amount Added to Wallet
  │
  ▼
Wallet Transaction Recorded
```

This allows refund transactions to be tracked independently through wallet transaction records.

---

## 🏷️ Offer & Coupon System

Rydex supports multiple discount mechanisms, including:

* Product offers
* Category offers
* Coupon discounts

Discounts are validated based on factors such as:

* Offer validity
* Expiration date
* Product/category eligibility
* Coupon availability
* Applicable order conditions

This allows the platform to support flexible promotional campaigns.

---

## 📊 Sales Reporting

The admin dashboard provides sales reporting capabilities.

Administrators can generate reports containing relevant sales and order information and export them in different formats.

Supported formats include:

* PDF
* Excel

This provides administrators with a convenient way to analyze and export sales data.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sinankcrypto/Rydex_project.git
```

```bash
cd Rydex_project
```

---

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file and configure the required environment variables.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DATABASE_NAME=your_database
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret

EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password

TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

> Do not commit your `.env` file or any API credentials to version control.

---

### 5. Configure PostgreSQL

Create a PostgreSQL database and update your environment variables with the appropriate database credentials.

Then run:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrator account.

---

### 7. Collect Static Files

```bash
python manage.py collectstatic
```

---

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

---

## 🔐 Security Considerations

The project uses environment variables for sensitive configuration such as:

* Django secret key
* Database credentials
* Razorpay API credentials
* Email credentials
* Twilio credentials

For production deployment:

* Set `DEBUG=False`
* Configure `ALLOWED_HOSTS`
* Use secure environment variables
* Configure HTTPS
* Protect API credentials
* Use a production-grade database
* Serve static files through a proper web server

---

## 🚀 Production Deployment

Rydex was deployed on an **AWS EC2 instance** using:

```text
Internet
    │
    ▼
  Nginx
    │
    ▼
 Gunicorn
    │
    ▼
 Django Application
    │
    ▼
 PostgreSQL
```

### Production Stack

* AWS EC2
* Nginx
* Gunicorn
* Django
* PostgreSQL

Nginx acts as the reverse proxy and handles incoming HTTP/HTTPS requests before forwarding application requests to Gunicorn.

Gunicorn runs the Django application using multiple worker processes, providing a production-ready WSGI server instead of Django's development server.

---

## 🧠 Key Technical Highlights

Some of the important backend concepts implemented in Rydex include:

### Authentication & Authorization

Implemented user authentication workflows with OTP verification, password reset functionality, and separate administrative capabilities.

### Inventory Management

Product variants maintain their own stock information, allowing inventory to be managed at the variant level rather than only at the product level.

### Payment Processing

Integrated Razorpay to handle online payments and payment verification while also supporting Cash on Delivery.

### Order Lifecycle

The application manages the complete lifecycle of an order:

```text
Pending
   ↓
Confirmed
   ↓
Processing
   ↓
Shipped
   ↓
Delivered
```

Orders can also transition through cancellation and return workflows.

### Refund Management

The wallet system provides a mechanism for processing and tracking refunds after approved returns or eligible cancellations.

### Sales Reporting

The application generates sales reports in both PDF and Excel formats, allowing administrators to export business data.

### Admin Operations

A dedicated administrative interface provides centralized management of the platform's users, products, inventory, orders, offers, coupons, returns, and reports.

---

## 🔮 Future Improvements

Potential future improvements include:

* [ ] REST API using Django REST Framework
* [ ] React-based frontend
* [ ] Advanced product recommendation system
* [ ] Redis caching
* [ ] Celery background tasks
* [ ] Automated email notifications
* [ ] Real-time order notifications
* [ ] Advanced analytics dashboard
* [ ] Elasticsearch-based product search
* [ ] Docker-based deployment
* [ ] Automated CI/CD pipeline
* [ ] Automated unit and integration testing
* [ ] Improved product filtering and sorting

---

## 📸 Screenshots

Add screenshots of the application here to showcase the user interface.

Suggested screenshots:

* Home page
* Product listing
* Product details
* Shopping cart
* Checkout
* Razorpay payment
* Order history
* Wallet
* Admin dashboard
* Sales reports

Example:

```markdown
![Home Page](screenshots/home.png)

![Product Details](screenshots/product-details.png)

![Admin Dashboard](screenshots/admin-dashboard.png)
```

---

## 📌 Project Highlights

Rydex was built as a practical e-commerce application to explore and implement real-world backend development concepts using Django.

The project covers:

* Full e-commerce workflows
* Authentication and authorization
* PostgreSQL database integration
* Payment gateway integration
* Inventory management
* Coupon and offer systems
* Order and return workflows
* Wallet and refund processing
* PDF invoice generation
* Sales report generation
* Excel data export
* Production deployment using AWS EC2
* Gunicorn and Nginx configuration

---

## 👨‍💻 Author

**Sinan Muhammed**

* GitHub: [@sinankcrypto](https://github.com/sinankcrypto)

---

## 📄 License

This project is intended for educational and portfolio purposes.

```
© 2026 Sinan Muhammed. All rights reserved.
```
