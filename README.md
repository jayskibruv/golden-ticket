
### Name of Resources:



>* **tickets.db**

----------

### 'tickets.db' Resource Attributes:




>* entrant name
>* entrant age
>* guest name

----------

### 'tickets.db' Table Schema:


    CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    entrant_name TEXT,
    entrant_age INTEGER,
    guest_name TEXT,
    random_token INTEGER );


----------

### REST API:


>* POST | /tickets | handleTicketCreate
* **Response for submitting a new ticket.**
>* GET | /tickets | handleAllTickets
* **Response for retrieving all submitted tickets.**
