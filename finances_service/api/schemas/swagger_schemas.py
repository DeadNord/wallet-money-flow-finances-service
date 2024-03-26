from drf_yasg import openapi

# Define the schema for the transaction creation request
add_transaction_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["name", "date", "amount", "type", "category", "from_account"],
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "date": openapi.Schema(type=openapi.TYPE_STRING, format="date"),
        "amount": openapi.Schema(type=openapi.TYPE_NUMBER),
        "type": openapi.Schema(
            type=openapi.TYPE_STRING,
            enum=["Income", "Expense"],
            description="Type of the transaction",
        ),
        "category_id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "from_account": openapi.Schema(type=openapi.TYPE_STRING),
        "note": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

# Define the schema for the transaction creation request
transaction_query_params = [
    openapi.Parameter(
        "name",
        openapi.IN_QUERY,
        description="Name of the transaction",
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        "start_date",
        openapi.IN_QUERY,
        description="Start date for filtering transactions",
        type=openapi.TYPE_STRING,
        format="date",
        required=False,
    ),
    openapi.Parameter(
        "end_date",
        openapi.IN_QUERY,
        description="End date for filtering transactions",
        type=openapi.TYPE_STRING,
        format="date",
        required=False,
    ),
]

# Define the schema for the transaction creation request
transaction_query_params = [
    openapi.Parameter(
        "name",
        openapi.IN_QUERY,
        description="Name of the transaction",
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        "start_date",
        openapi.IN_QUERY,
        description="Start date for filtering transactions",
        type=openapi.TYPE_STRING,
        format="date",
        required=False,
    ),
    openapi.Parameter(
        "end_date",
        openapi.IN_QUERY,
        description="End date for filtering transactions",
        type=openapi.TYPE_STRING,
        format="date",
        required=False,
    ),
]

delete_transaction_params = [
    openapi.Parameter(
        "id",
        in_=openapi.IN_PATH,
        type=openapi.TYPE_STRING,
        description="Transaction ID",
        required=True,
    ),
]
