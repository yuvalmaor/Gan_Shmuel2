weight_schema = {

    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
            "direction": {
                "type": "string",
                "enum": ["in", "out", "none"]
            },
        "truck": {
                "type": "string"
            },
        "containers": {
                "type": "string",
                "pattern": "^[a-zA-Z0-9,]*$"
            },
        "weight": {
                "type": "integer",
                "minimum": 1
            },
        "unit": {
                "type": "string",
                "enum": ["kg", "lbs"]
            },
        "force": {
                "type": "boolean"
            },
        "produce": {
                "type": "string"
            }
    },
    "required": ["direction", "weight", "unit"]

}
