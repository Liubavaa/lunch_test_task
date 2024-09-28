# Lunch Decision Backend Service

## Description

This project is an internal service for a company that helps employees decide where to go for lunch. Each restaurant admin can upload its menu every day, and employees can vote for their preferred lunch menu (multiple choice). The project includes API functionality for restaurant admin and employee roles, using Django, Django REST Framework, JWT Authentication, and PostgreSQL for the database.

## Features

- **Authentication**: JWT-based user authentication for both restaurant admins and employees.
- **Restaurant Admin Features**: 
  - Create a restaurant
  - Upload a daily menu for restaurant
- **Employee Features**:
  - Vote for the preferred menu
- **Both Users Feature**:
  - View the current day's menu
  - View voting results for the current day

## Tech Stack

- **Backend**: Django + Django REST Framework (DRF)
- **Authentication**: JWT (JSON Web Token)
- **Database**: PostgreSQL
- **Containerization**: Docker with `docker-compose`

## Getting Started

### Prerequisites

- Docker installed on your system.
- Python 3.x and `pip` (if not using Docker).

### Running the Application with Docker

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/lunch-decision-service.git
    cd lunch_decision
    ```

2. Build and run the application using Docker:

    ```bash
    docker-compose up -d
    ```

3. Apply the database migrations:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

4. You can now access the API at `http://localhost:8000/`.

## API Documentation

### Authentication

To authenticate a user (restaurant admin or employee), use the following endpoint:

- `POST /api/register/`: Create new user.

Example request:

```json
{
  "username": "user",
  "password": "password",
  "role": "admin"
}
```

Then

- `POST /api/token/`: Get a JWT token by providing a username and password.

```json
{
  "username": "user",
  "password": "password"
}
```

Now use access token with each next request, or, for example, authorize with it in postman.

### Create restaurant 

- `POST /restaurant/create/`: This restaurant admin user become responsible for created restaurant.

```json
{
  "name": "Ashan"
}
```

### Upload menu 

- `POST /menu/upload/`: Specify menu description and date

```json
{
  "date": "2024-09-28",
  "description": "Fish and beer"
}
```

### Upload menu 

- `POST /menu/upload/`: Specify menu description and date

```json
{
  "date": "2024-09-28",
  "description": "Fish and beer"
}
```

### Get current day menu

- `GET /menu/today/`: Get all available menus for today


### Vote for menu

- `POST /menu/vote/menu_id`: You can cast many votes for each day

### Get result for today

- `GET /menu/results/`

Output example:
```json
[
    {
        "menu": {
            "id": 1,
            "date": "2024-09-28",
            "description": "fish and beer",
            "restaurant": 1
        },
        "votes": 2
    },
    {
        "menu": {
            "id": 2,
            "date": "2024-09-28",
            "description": "fish and no beer",
            "restaurant": 1
        },
        "votes": 1
    }
]
```

## Testing

Run ```docker-compose run web pytest``` to check test cases.

Run ```flake8``` to check code formatting.