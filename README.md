# Vuez EMS (Employee Management System)

A robust and flexible Employee Management System built with Django and Django REST Framework. This system allows for dynamic employee profile creation using customizable form templates, supporting various field types and drag-and-drop reordering. It comes with a full-featured REST API secured by JWT authentication.

## 🚀 Key Features

### 🔐 Authentication & Security
- **JWT Authentication**: Secure API access using `simplejwt` with Access and Refresh token rotation.
- **Secure Logout**: Implementation of token blacklisting to invalidate refresh tokens on logout.
- **Role-Based Access**: Standard Django permission system integrated with API views.

### 📝 Dynamic Form Builder
- **Custom Form Templates**: Create unique employee forms (e.g., "Engineering Onboarding", "HR Profile").
- **Drag-and-Drop Reordering**: API to easily reorder form fields.
- **Rich Field Support**: Supports Text, Number, Email, Date, Select (Dropdown), Checkbox, and more.

### 👥 Employee Management
- **Dynamic Profiles**: Employee records are based on the custom templates – not rigid database schemas.
- **Search & Filtering**: Search employees by field values or filter by template type.
- **Pagination**: Efficient handling of large employee lists with paginated API responses.
- **Data Integrity**: Uses `transaction.atomic` to ensure data consistency during complex creation/update operations.

## 🛠️ Tech Stack
- **Backend**: Django 6.0, Django REST Framework
- **Authentication**: simplejwt
- **Database**: SQLite (default) / PostgreSQL (production ready)
- **Utilities**: django-cors-headers, Pillow (for image handling)

## ⚡️ Quick Start

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abbasalitmk/veuz-ems.git
   cd veuz-ems
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**
   ```bash
   python manage.py runserver
   ```

   The API is now available at `http://127.0.0.1:8000/`.

## 📚 API Documentation

### Authentication (`/api/auth/`)
- `POST /register/` - Register a new user
- `POST /login/` - Login and receive JWT tokens
- `GET /profile/` - Get current user profile
- `POST /token/refresh/` - Refresh expired access token
- `POST /logout/` - Logout and blacklist refresh token

### Form Templates (`/api/forms/`)
- `GET /` - List all templates (paginated)
- `POST /` - Create a new template with fields
- `GET /{id}/` - Get template details
- `POST /{id}/reorder/` - Reorder fields (Send `{ "field_order": [ids...] }`)

### Employees (`/api/employees/`)
- `GET /` - List all employees (paginated). Supports `?search=` and `?form_template=`
- `POST /` - Create an employee using a specific template
- `PUT /{id}/` - Update employee data

## 🧪 Testing

A helper script `test_auth_flow.sh` (if available) or the Postman collection can be used to verify the entire flow.

Import the `postman_collection.json` file into Postman for a pre-configured testing environment.

## 📄 License
MIT License
