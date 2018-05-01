MIGRATION_SCHEMA = {
    "$id":"#",
    "type":"object",
    "properties":{
        "content_type":{
            "type":"object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "view_path":{
                        "type": "string"
                    },
                    "schema":{
                        "type": "object",
                        "additionalProperties":{
                            "type":"string"
                        }
                    }
                },
                "required": [
                    "schema"
                ]
            }
        },
        "content_data":{
            "type":"object",
            "properties": {
                "type":{
                    "type":"string"
                },
                "data":{
                }
            },
            "additionalProperties": False,
            "required": [
                "type",
                "data"
            ]
        },
        "content":{
            "type":"object",
            "additionalProperties": {
                "type":"object",
                "properties": {
                    "type":{
                        "type":"string"
                    },
                    "name":{
                        "type": "string"
                    },
                    "data": {
                        "oneOf": [
                            {"type":"integer","minimum":0},
                            {"$ref": "#/properties/content_data/properties/data"}
                        ]
                    },
                    "children":{
                        "type":"object",
                        "additionalProperties":{
                            "$ref":"#/properties/content/additionalProperties"
                        }
                    }
                },
                "required":[
                    "data",
                    "type"
                ]
                
            }

            
        }
    },
    "additionalProperties": False
}