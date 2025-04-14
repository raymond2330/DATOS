# DATOS

This project is a full-stack application built with Django as the backend and React as the frontend.

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   python3 -m venv env # For Linux/Mac
   # or
   python -m venv env # For Windows
   ```
2. Activate the virtual environment:
   ```bash
   source env/bin/activate  # For Linux/Mac
   # or
   env\Scripts\activate    # For Windows
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend` directory and add the following:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=*
   ```
5. Run database migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the Django server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the required npm packages:
   ```bash
   npm install
   ```
3. Start the React application:
   ```bash
   npm start
   ```
