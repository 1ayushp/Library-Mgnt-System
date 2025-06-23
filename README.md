# Library Management System API (Django + DRF + JWT)

An API-driven Library Management System built using Django, Django REST Framework, and JWT authentication.  
Supports **admin**, **librarian**, and **member** roles with strict **role-based access control**.

---

## Features

- JWT-based authentication.
- Role-based access:
  - **Admin**: Full control over users and books and access Django admin panel.
  - **Librarian**: Can manage books and update users.
  - **Member**: Can view books and profile only.
- Book management: create, update, delete, list.
- User management: create, update, delete, list with role-based restrictions.
- Ability to update yourself
- Access to admin panel for staff\*

    \* permission only for specific models
- Seed script for initial data setup.
- API test-ready (Postman Collection provided).

---

## Use Case

This system is designed for a digital library where:
- Admins manage everything including roles.
- Librarians handle books and manage member-level users.
- Members can explore the library catalog.

---

## Installation & Setup

1. **Clone the repository**
   ```
   git clone https://github.com/1ayushp/library-management.git
   ```
2. **Create virtual env and activate it**
   ```
   virtualenv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
4. **Go to the file directory**
   ```
   cd library_system
   ```
---
## Seeding the database with sample data
**Run the following command**
    ```
    python manage.py seed
    ```
This will populate the database with 
- **4 admin**(1 super user **admin**) ,**3 libraian** and **3 members** for the **User** model 
  - admin1, admin2, admin3
  - librarian1, librarian2, librarian3
  - member1, member2, member3
    - **Password for all = username**
- **7 books** for the **Books** model 

---
## Running the Server
    ```
    python manage.py runserver
    ```
### Server will be available at:

    ```
    http://127.0.0.1:8000/
    ```
---
## Accessing the api
The api can be access through `http://127.0.0.1:8000/api/`

  \*Currently the only `ALLOWED_HOSTS` is `localhost`

### API Documentation
Use Postman can be used to test the API.
Postman Collection is available in the repo at:


`Postman/LMS Books.postman_collection.json`

`Postman/LMS Users.postman_collection.json`

**Steps**
1. In each collection `{{base_url}}` can be changed to fit with the server URL.
2. Modify the body of the first endpoint `Get Access Token` with the required username and password.
3. The collection is setup in such a way that the access is automatically used for further testing
    - Else use bear token in the authentication section and paste the access value
4.  Test various endpoints the collection consists of some of them to auto run 
    - Many methods are authorized and depends upon the role
    - User can change his/her username and password
    - Admin can access all the database
    - Librarian can only update based on the permission it has been authorized
    - Member can only read the books


### API endpoints
**JWT Authentication**

Login to get authentication token
```
POST: /api/token/
{
  "username": ".....",
  "password": "....."
}
```
```
Output:
{
  "refresh": ".....",
  "access": "....."
}
```
**Refresh the token**

```
POST /api/token/refresh/
{
  "refresh": "refresh_token_value"
}
```
```
Output:
{
    "access": "....."
}

```
\* Currently the refresh token lasts for 1 hour



**Books**
| Action             | Method   | URL                | Role Required     |
| -----------        | -------- | ------------------ | ----------------- |
| List rented books  | GET      | `/api/books/me`    | Any authenticated |
| List books         | GET      | `/api/books/`      | Any authenticated |
| Create book        | POST     | `/api/books/`      | Admin, Librarian  |
| Update book        | PATCH    | `/api/books/{id}/` | Admin, Librarian  |
| Delete book        | DELETE   | `/api/books/{id}/` | Admin, Librarian  |

**Users**
| Action        | Method | URL                | Role Required       |
| ------------- | ------ | ------------------ | ------------------- |
| List yourself | GET    | `/api/users/me`    | Any authenticated   |
| List users    | GET    | `/api/users/`      | Admin, Librarian    |
| Create user   | POST   | `/api/users/`      | Admin, Librarian*   |
| Update user   | PATCH  | `/api/users/{id}/` | Admin, Librarian*   |
| Delete user   | DELETE | `/api/users/{id}/` | Admin, Librarian*   |

\* Librarians can only interact users with role member and cannot make modifications to admin or other librarians

## Summary

| Action               | Admin           | Librarian                           | Member  |
| -------------------- |:---------------:|:-----------------------------------:|:-------:|
| View yourself        |     YES         | YES                                 | YES      |
| View users           |     YES         | YES                                 | NO      |
| Create users         |  YES (any role) | YES (only `member`, `librarian`)    | NO      |
| Update users         |  YES (any user) | YES (only `member`, limited fields) | NO      |
| Change role to admin |      YES        | NO                                  | NO      |
| Delete users         |      YES        | YES (only `member`)                 | NO      |
| View books           |      YES        | YES                                 | YES     |
| Create books         |      YES        | YES                                 | NO      |
| Update books         |      YES        | YES                                 | NO      |
| Delete books         |      YES        | YES                                 | NO      |

**Notes on Librarian Restrictions**
  
  - Librarians cannot assign the admin role.
  - Librarians can only update users with role member, and cannot change roles to admin.
  - Librarians can delete only member users.

---

## Tech Stack Used

```
Python == 3.12.3
Django == 5.2.3
Django REST Framework == 3.16.0
SimpleJWT == 5.5.0
SQLite (can be switched to MySQL/Snowflake/MongoDB/)
```
---
## Limitaions
Currently there are a few limitations in the project
- Lack of Frontend Interface
    - This project only provides API endpoints. There is no web or mobile UI, so tools like Postman or cURL are needed to interact with the system.

- No Rate Limiting or Throttling
    - APIs are open to repeated access and can be abused

- No Pagination or Filtering on List APIs
    - Large datasets may become inefficient to fetch or query as there are no filters or pagination on book or user lists.
- No Book Tracking History
    - Users can get any number of books with no tracking or return system.
---

## Author

**Ayush Parajuli**

*(Task for Backend Developer)*