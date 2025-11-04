# Project & Repository Description

ExpenseTracker is a web app that helps users manage their personal finances. 
Users can track expenses, categorize them, and manage payment methods. 
The app includes authentication, a clean UI, and full CRUD for expenses, categories, and payment methods.

# Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker

# Frontend Repository Link

https://github.com/HamasAlsharari/capstoneFrontend

# Backend Site

http://localhost:8000/

# Installation Instructions

## Using Docker
1. Make sure Docker is installed and running on your machine.
2. Navigate to the backend project directory:
   ```bash
   cd capstoneBackend
3. Build and start the container:
   docker compose up --build
4. Access the backend API at: http://localhost:8000

Without Docker (Optional)
1. Navigate to the backend project directory:
   cd capstoneBackend
2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
3. Install dependencies:
    pip install -r requirements.txt
4. Apply migrations and start the server:
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
5. Access the backend API at: http://localhost:8000

# ERD Diagram
<img src="ERD.png" alt="ERD Diagram">

## Routing Table / API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/signup/ | User signup |
| POST | /api/auth/login/ | User login |
| POST | /api/auth/logout/ | User logout |

### Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/expenses/ | List all expenses |
| POST | /api/expenses/ | Create expense |
| GET | /api/expenses/:id/ | Get expense details |
| PUT | /api/expenses/:id/ | Update expense |
| DELETE | /api/expenses/:id/ | Delete expense |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/categories/ | List all categories |
| POST | /api/categories/ | Create category |
| GET | /api/categories/:id/ | Get category |
| PUT | /api/categories/:id/ | Update category |
| DELETE | /api/categories/:id/ | Delete category |

### Payment Methods
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/payment-methods/ | List all payment methods |
| POST | /api/payment-methods/ | Create payment method |
| GET | /api/payment-methods/:id/ | Get payment method |
| PUT | /api/payment-methods/:id/ | Update payment method |
| DELETE | /api/payment-methods/:id/ | Delete payment method |

### Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/profile/ | Get user profile |
| POST | /api/profile/ | Create profile |
| PUT | /api/profile/ | Update profile |


# IceBox Features / Future Features
- Add email notifications for account activity.
- Implement analytics dashboard for expenses.
- Integrate third-party payment gateways.
- Add role-based access control for admin users.