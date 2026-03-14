# Django Booking System with QR Code and Stripe Integration

## Project Overview
This is a professional **Django-based booking system** where users can browse services, book them, and receive **QR-coded tickets**. The system includes a modern **UI/UX design**, animated booking progress, Stripe payment simulation, and an admin panel to manage services and bookings.

---

## **Features**

### User Features
- Browse available services with images and descriptions.
- Book a service by selecting a date.
- **Stripe payment simulation** with loader animation.
- **Success page** with animated confirmation.
- **QR code** generated automatically for each booking.
- User dashboard to view **booking history**.

### Admin Features
- Add, edit, or delete services.
- View and manage all bookings.
- Preview QR codes for each booking.

### UI/UX
- Professional and responsive design using **Bootstrap 5**.
- Card hover animation and booking progress steps.
- Animated success page and redirect to dashboard.

---

## **Installation & Setup**

### Prerequisites
- Python 3.10+  
- Django 4.x  
- pip package manager  

### Steps
1. Clone the repository:

```bash
git clone <your-repo-url>
cd booking_platform
```

2. Create virtual environment:

```bash
python -m venv venv
```

3. Activate virtual environment:

- Windows:
```bash
venv\Scripts\activate
```
- Mac/Linux:
```bash
source venv/bin/activate
```

4. Install required packages:

```bash
pip install -r requirements.txt
```

5. Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser for admin panel:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

8. Open your browser:
- **Website:** [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- **Admin Panel:** [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## **Folder Structure**

```
booking_platform/
├── bookings/
│   ├── migrations/
│   ├── static/bookings/
│   │   ├── script.js
│   │   └── css/
│   ├── templates/bookings/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── service_detail.html
│   │   ├── success.html
│   │   └── dashboard.html
│   ├── forms.py
│   ├── models.py
│   ├── utils.py
│   ├── views.py
│   └── urls.py
├── booking_platform/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/
│   ├── services/
│   └── qr_codes/
├── manage.py

```

---

## **Media / Static Files**
- **Services Images:** `media/services/`  
- **Generated QR Codes:** `media/qr_codes/`  
- **JS & CSS:** `bookings/static/bookings/`  

---

## **Usage**
1. Users browse services on home page.  
2. Click **Book Now** → fill date → click submit.  
3. QR code generated automatically and displayed on **success page**.  
4. Dashboard shows all bookings for logged-in user.  
5. Admin panel allows management of services and bookings.

---

## **Future Enhancements**
- Real **Stripe payment integration** with webhook.  
- PDF ticket generation with embedded QR code.  
- Email notifications on booking confirmation.  
- Animated booking progress with step highlights.

---

## **License**
This project is for **client purpose** under [MIT LICENSE](https://github.com/BipronathSaha12/Event-ticket-booking-system/blob/main/LICENSE).

---

## **Contact**
- Developer: **Bipronath Saha**  
- Email: `bipronathsaha@gmail.com`  
- LinkedIn: [LinkedIn Profile](https://www.linkedin.com/bipronath-saha)
```}

