# 🧘‍♀️ YOGI FITNESS STUDIO - Booking API

This is a RESTful API built using **Django** and **Django REST Framework** for managing fitness classes and class bookings.

##  Features

-  View all available fitness classes
-  Book a fitness class if slots are available
-  Retrieve all bookings by email
-  Timezone-aware scheduling (IST by default)
-  Input validation and error handling
-  In-memory DB (SQLite)

---

## Tech Stack

- Python (version - Python 3.12.5)
- Django
- Django REST Framework
- SQLite
- Postman / cURL for testing

---

## Setup Instructions

1. **Clone the repository**  
 


link clone
cd yogi_fitness_api



2. Create and activate a virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt


4. Run migrations

python manage.py makemigrations
python manage.py migrate

5. Run the development server
python manage.py runserver




################################### API TESTING ########################################################

1. 🔍 View Available Fitness Classes
GET /classes/

Returns a list of upcoming fitness classes.

Response:


[
  {
    "id": 1,
    "name": "Yoga",
    "date_time": "2025-06-12T07:00:00Z",
    "instructor": "Rina",
    "total_slots": 20,
    "available_slots": 10
  }
]

2. ➕ Add a New Fitness Class
POST /classes/
Creates a new fitness class.

Payload:

{
  "name": "Zumba",
  "date_time": "2025-06-15T18:00:00Z",
  "instructor": "Ravi",
  "total_slots": 30,
  "available_slots": 30
}


Response (201 Created):

{
  "id": 2,
  "name": "Zumba",
  "date_time": "2025-06-15T18:00:00Z",
  "instructor": "Ravi",
  "total_slots": 30,
  "available_slots": 30
}




3. 📝 Book a Fitness Class
POST /book/

Payload:

{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}


Response (201 Created):

{
  "id": 1,
  "fitness_class": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}


4. 📬 View Bookings by Email
GET /bookings/?email=john@example.com

Response:
[
  {
    "id": 1,
    "fitness_class": 1,
    "client_name": "John Doe",
    "client_email": "john@example.com"
  }
]

