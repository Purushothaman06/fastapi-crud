# FastAPI CRUD Application

This is a FastAPI application that performs CRUD operations for Items and User Clock-In Records.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/Purushothaman06/fastapi-crud-app.git
   cd fastapi-crud-app
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root.
   - Add your MongoDB URI to the `.env` file:
     ```
     MONGODB_URI=mongodb+srv://your-username:<your-password>@your-cluster-url/your-database?retryWrites=true&w=majority
     DEBUG=True
     ```

## Running the Application

To run the application locally:

```
fastapi run
```

The application will be available at `http://localhost:8000`.

## API Endpoints

### Items API

- `POST /items`: Create a new item
- `GET /items/{id}`: Retrieve an item by ID
- `GET /items/filter`: Filter items based on email, expiry date, insert date, and quantity
- `GET /items/aggregate`: Aggregate data to return the count of items for each email
- `DELETE /items/{id}`: Delete an item based on its ID
- `PUT /items/{id}`: Update an item's details by ID

### Clock-In Records API

- `POST /clock-in`: Create a new clock-in entry
- `GET /clock-in/{id}`: Retrieve a clock-in record by ID
- `GET /clock-in/filter`: Filter clock-in records based on email, location, and insert datetime
- `DELETE /clock-in/{id}`: Delete a clock-in record based on its ID
- `PUT /clock-in/{id}`: Update a clock-in record by ID

## API Documentation

You can access the Swagger UI documentation at `http://localhost:8000/docs` when running the application locally.

## Deployment

This application can be deployed to a free hosting service like Koyeb. Follow their documentation to deploy your FastAPI application.

## GitHub Repository

The source code for this project is available at: [https://github.com/Purushothaman06/fastapi-crud-app](https://github.com/Purushothaman06/fastapi-crud-app)

## Hosted Swagger Documentation

The Swagger documentation for the deployed application is available at: [https://your-app-name.koyeb.app/docs](https://your-app-name.koyeb.app/docs)
