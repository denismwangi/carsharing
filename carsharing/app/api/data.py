from flask_restful import fields


user_data={"id":fields.Integer,
    "email":fields.String,
    "phone":fields.String,
    "username":fields.String,
    "about":fields.String,
    "joined_on":fields.String,
    "photo":fields.String,
    "rating":fields.Integer
}

car_data={"id":fields.Integer,
    "regno":fields.String,
    "brand":fields.String,
    "added_on":fields.DateTime,
    "charges":fields.Integer,
    "mileage":fields.Integer,
    "approved":fields.Boolean,
    "location":fields.String,
    "description":fields.String,
    "rating":fields.Integer,
    "ownerid":fields.String,
    "photo":fields.String
}

borrowed_data={
    "carid":fields.Integer,
    "borrowed_on":fields.DateTime,
    "expected_on":fields.DateTime,
    "duration":fields.Integer,
    "borrowed_loc":fields.String,
    "expected_loc":fields.String,
}

income_data={
    "id":fields.Integer,
    "date":fields.DateTime,
    "borrowerid":fields.Integer,
    "carid":fields.Integer,
    "amount":fields.Integer
}

spending_data={
    "id":fields.Integer,
    "date":fields.DateTime,
    "ownerid":fields.Integer,
    "carid":fields.Integer,
    "amount":fields.Integer
}
