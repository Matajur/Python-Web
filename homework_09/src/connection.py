from mongoengine import connect
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

username = config.get("DB", "user")
password = config.get("DB", "pass")
domain = config.get("DB", "domain")
db_name = config.get("DB", "db_name")

url = f"mongodb+srv://{username}:{password}@{domain}.uchiekn.mongodb.net/{db_name}?retryWrites=true&w=majority"
session = connect(host=url, ssl=True)

if __name__ == "__main__":
    print(username, password, db_name, sep="\n")
