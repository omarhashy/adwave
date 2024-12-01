import pandas as pd
from pymongo import MongoClient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


client = MongoClient("mongodb://localhost:27017/")
db = client["AddWave"]
products_collection = db["products"]
nodes_collection = db["graph"]
sales_collection = db["sales"]


def load_products_data(file, username):
    try:
        data = pd.read_csv(file)
    except:
        return "error"

    data_dict = data.to_dict(orient="records")

    print(data_dict)

    for i in range(len(data_dict)):
        if "product_name" not in data_dict[i]:
            return "The file should contain a 'product_name' attribute!"
        data_dict[i]["username"] = username

    products_collection.insert_many(data_dict)


def feed_the_graph(file, username):
    try:
        data = pd.read_csv(file)

        data_dict = data.to_dict(orient="records")

        for i in range(len(data_dict)):
            if "email" not in data_dict[i]:
                return "The file should contain a 'email' attribute!"
            if "cart" not in data_dict[i]:
                return "The file should contain a 'cart' attribute!"
            data_dict[i]["username"] = username
            data_dict[i]["cart"] = [
                i.strip() for i in list(data_dict[i]["cart"].split(","))
            ]

            for u in range(len(data_dict[i]["cart"])):
                for j in range(u + 1, len(data_dict[i]["cart"])):
                    insert_edge(data_dict[i]["cart"][u], data_dict[i]["cart"][j])
                    insert_edge(data_dict[i]["cart"][j], data_dict[i]["cart"][u])

        sales_collection.insert_many(data_dict)
    except:
        return "error"


def insert_edge(product1, product2):

    filter_query = {"node1": product1, "node2": product2}
    update_operation = {"$inc": {"weight": 1}}
    result = nodes_collection.update_one(filter_query, update_operation)

    if result.matched_count == 0:
        new_document = {
            "node1": product1,
            "node2": product2,
            "weight": 1,
        }
        nodes_collection.insert_one(new_document)


def get_children(product):
    filter_query = {"node1": product}
    documents = [[i["node2"], i["weight"]] for i in nodes_collection.find(filter_query)]
    return documents


def send_email__(subject, body, to_email):
    email = ""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, "")

    message = MIMEMultipart()
    message["From"] = email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    server.sendmail(email, to_email, message.as_string())


import threading

def send_emails(map: dict, products):
    # print(map)
    for email in map:
        recomended_w = dict()
        recomended_li = []
        for u in map[email]:
            ch = get_children(u)
            for j in ch:

                if j[0] in map[email] or j[0] not in products:
                    continue

                if j[0] not in recomended_w:
                    recomended_w[j[0]] = 0
                recomended_li.append(j[0])
                recomended_w[j[0]] += j[1]

        if len(recomended_li) == 0:
            continue
        recomended_li.sort(key=lambda x: -1 * recomended_w[x])
        subject = "Recomindations by AddWave"
        body = f"""
        Hello,
        based on your activity we recommend you to buy {set(recomended_li[0:3])}
        AddWave
        """
        thread = threading.Thread(target=send_email__, args=((subject, body, email)))
        thread.start()


def recomend(username):
    filter_query = {"username": username}
    documents = [i for i in sales_collection.find(filter_query)]
    products = {i["product_name"] for i in products_collection.find(filter_query)}
    frequency = dict()
    for i in documents:
        if i["email"] not in frequency:
            frequency[i["email"]] = set()
        for u in i["cart"]:
            frequency[i["email"]].add(u)
    send_emails(frequency, products)
