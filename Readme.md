# Evento - Event Management System

The system allows users to create, manage, and participate in events, with a robust API for interacting with the system programmatically.

### Features
- User Management:
    - User registration, login, and profile management.
    - Authentication using JWT (JSON Web Token).

- Event Management:
  - Event Organizer can 
     - Create, update, delete, and view owned events.
     - create tickets for event.

- Participant Management:
  - Manage participants for events.
  - Participants can purchase tickets for event

- Admin Management:
  - Manage users, events.

### Technologies Used
- fastAPI: Web framework for backend logic.
- JWT Authentication: Secure user authentication.
- PostgreSQL: As the primary database for storing user and event data.


### Routes
```
Authentication

POST /api/auth/register/ - Register a new user. (done)
POST /api/auth/token/ - User login to get JWT token. (done)
POST /api/auth/logout/ - Logout user and invalidate the JWT. 
```

```
Events

GET /api/events/all - List all events. (unauthenticated) (done)
POST /api/events - Create a new event. (For only organizers) (done)
POST /api/events - Create a new event. (done)
GET /api/events/{event_id} - Retrieve details of a specific event. (done)
PUT /api/events/{event_id} - Update an event. (done)
DELETE /api/events/{event_id} - Delete an event. (done)
```

```commandline
Search

GET /api/search?q="hello" (done)
```