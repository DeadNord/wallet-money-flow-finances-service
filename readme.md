# Finances Service API

## Description

This Finances Service API is designed to manage users' financial transactions and budgets. It allows users to track their income and expenses, categorize transactions, and analyze their financial habits over time.

## Features

- **Budget setting and tracking**: Users can set and view their budget limits.
- **Transaction recording**: Record both income and expense transactions.
- **Categorization of transactions**: Organize transactions by categories.
- **Reporting and analytics**: Provides summaries and analytics by category and time period.

## Installation

To set up the project environment, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/DeadNord/wallet-money-finances-service
```

2. Navigate to the project directory:

```bash
cd finances_service
```

3. Build the Docker containers:

### Development:

To build and run the containers in a development environment, execute the following command:

```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build
```

### Production:

To run the containers in a production environment, use the following command:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

## Usage

To use these endpoints, users will need to be authenticated and provide their unique user ID where required. Transactions can be added or deleted, and budget limits can be set and viewed, all through these endpoints.

## Endpoints

- `/api/finances/budget/`: Retrieve and set the user's budget. This endpoint allows users to view their current budget limit and update it to a new value.

- `/api/finances/transactions/`: List all transactions for the user, record new transactions, and filter transactions by date or category. This endpoint supports GET and POST methods to retrieve and add transactions, respectively.

- `/api/finances/expenses_by_category/`: Retrieve a summary of expenses grouped by category for the current month. This endpoint helps users to track how much they have spent in each category.

- `/api/finances/transactions_by_week/`: Get the total income and expenses for each day of the current week, helping users to understand their weekly financial activity.

- `/api/finances/add-transaction/`: Add a new financial transaction. This endpoint expects POST requests with the transaction data, including the transaction's name, amount, type (income or expense), category, date, and any additional notes.

- `/api/finances/delete-transaction/<int:id>/`: Delete an existing financial transaction by its unique ID. This endpoint expects DELETE requests and will remove the specified transaction from the user's records if it exists.

- `/api/finances/categories/`: List all the transaction categories. This endpoint helps users to get a list of all possible categories for transactions.

- `/api/finances/create-user-profile/`: Create a new user profile. This endpoint allows for the creation of a new user profile with a specific user ID.

- `/api/finances/update-budget/`: Update the budget limit of a user's profile. This endpoint expects new budget limits to update the existing one.

## API Documentation

### Swagger UI

For a more interactive exploration of the API, with the ability to send requests and view responses directly from your web browser, visit the Swagger UI documentation:

- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

This provides a detailed overview of all API endpoints, including request parameters, response structures, and authentication methods. You can also try out API calls directly from the documentation page by clicking on the "Try it out" button for each endpoint.

### Redoc

For an alternative documentation format, you can view the Redoc documentation at:

- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/docs/)

Redoc provides a more structured and readable layout for the API documentation, including clear separation of endpoints, request parameters, and responses. It's particularly useful for understanding the overall structure of the API at a glance.

Both Swagger UI and Redoc are automatically generated from the OpenAPI (formerly Swagger) specification for the Finances Service API. They are updated in real time as changes are made to the API.

## Contributing

Contributions to the Finances Service API are welcome! Please fork the repository and submit pull requests with any enhancements, bug fixes, or new features.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

```

```
