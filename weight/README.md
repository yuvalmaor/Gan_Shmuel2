# Gan Shmuel Weight Microservice API

The Gan Shmuel Weight Microservice is designed for industrial weight measurement, primarily focusing on weighing trucks to facilitate the payment process to providers. This service allows for the accurate tracking of weights and enables payments based on the net weight of the produce. 

## Key Concepts

- **Bruto Weight**: The total weight, including the net weight of the fruit, the tara (empty weight) of the truck, and the sum of the tara weights of all containers.
- **Neto Weight**: The weight of the produce only .
- **Tara Weight**: The empty weight of the truck and containers.
- **Session ID**: A unique identifier for each weighing session. 

## API Routes

### POST `/weight`

Records the weight data along with server date-time.

#### Parameters:
- `direction`: `in`/`out`/`none` - Direction of weighing.
- `truck`: License plate of the truck, or "na" if not applicable.
- `containers`: Comma-delimited list of container IDs.
- `weight`: Weight measurement (integer).
- `unit`: Unit of weight (`kg`/`lbs`).
- `force`: Boolean flag to force overwrite of previous weigh-ins.
- `produce`: ID of the produce (e.g., "orange", "tomato") or "na" if empty.

#### Returns:
JSON object containing the unique weight session ID, bruto weight, and, for "out" direction, truck tara and neto weight.

### POST `/batch-weight`

Uploads a list of tara weights for containers from a file.

#### Parameters:
- `file`: Filename of the file in the "/in" folder containing tara weights.

### GET `/unknown`

Returns a list of all containers with unknown tara weight.

### GET `/weight`

Retrieves weight records within a specified time frame and filter.

#### Parameters:
- `from`: Start date-time stamp (yyyymmddhhmmss).
- `to`: End date-time stamp (yyyymmddhhmmss).
- `filter`: Comma-delimited list of directions (`in`, `out`, `none`).

### GET `/item/<id>`

Provides details for a specific item (truck or container).

#### Parameters:
- `id`: Item ID.
- `from`: Start date-time stamp (yyyymmddhhmmss).
- `to`: End date-time stamp (yyyymmddhhmmss).

### GET `/session/<id>`

Retrieves details for a specific weighing session.

#### Parameters:
- `id`: Session ID.

### GET `/health`

Checks the health of the system.

## Response Format

Responses are in JSON format. Here are some examples:

### Weight Record:
```json
{
  "id": "string",
  "truck": "license" or "na",
  "bruto": "int",
  "truckTara": "int",
  "neto": "int" or "na"
}
```

### Unknown Containers:
```json
["id1", "id2", ...]
```

### Weighing Records:
```json
[
  {
    "id": "id",
    "direction": "in/out/none",
    "bruto": "int",
    "neto": "int" or "na",
    "produce": "str",
    "containers": ["id1", "id2", ...]
  },
  ...
]
```

## Error Handling

The API provides error messages in cases such as:

- Invalid requests (e.g., "out" without preceding "in").
- Request to overwrite data without the `force` flag set to true.
- System health issues, indicated by a "Failure" message and a 500 Internal Server Error status.

## Implementation Details

- The system assumes server time for all operations unless specified otherwise.
- The precision of weight measurements is around 5kg, thus decimals are not considered.
- The system's functionality and reliability depend on external resources, such as databases, for operation.

This API is integral to the Gan Shmuel industrial operations, facilitating efficient and accurate weight tracking and payment processes for agricultural produce.

