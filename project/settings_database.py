from .settings import DEBUG
MongoUri = {
    "DEBUG":None,
    "Production":'mongodb://140.120.13.243:27017'
}

if DEBUG:
    uri = MongoUri['DEBUG']
else:
    uri = MongoUri['Production']