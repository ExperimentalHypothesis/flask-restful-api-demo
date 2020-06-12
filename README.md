# Flask RESTful API Demo

## Instalation via requirements:
```
git clone 
cd flask-restful-api-demo
pip install -r requirements.txt
python app.py
```

## Usage

All responses have the form of JSON:

### List all items:

** definition **

'GET /items'

** response **

- 200 OK on success, 

```
{
    "items": [
        {
            "name": "camera",
            "price": 25.99,
            "store_id": 2
        },
        {
            "name": "walkman",
            "price": 15.99,
            "store_id": 1
        }
    ]
}
``` 

### Create new item:

** definition **

'POST /item'

** arguments **

- `"price":float`
- `"store_id":int` 

** response **

- 201 Created on success

```
    {
        "name": "camera",
        "price": 25.99,
        "store_id": 2
    }
``` 

### Get item details:

** definition **

'GET /item/<name>'

** response **

- 404 Not Found if it does not exist
- 200 OK on success

```
    {
    "name": "camera",
    "price": 25.99,
    "store_id": 2
    }
``` 

### Delete item:

** definition **

'DELETE /item/<name>'

** reponse **
- 404 Not Found if it does not exist




