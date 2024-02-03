import numpy as np
import os
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import pandas as pd
from tinydb import TinyDB, Query

import importlib
import requests
from bs4 import BeautifulSoup

db = TinyDB("db.json")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


# CONSTANTS :
CAR_CSV_PATH = "./data/car_0.csv"
RECOMMENDATION_STRAT_DIR = "./recommendation_strategies"


@app.post("/new_session")
@cross_origin()
def new_session():
    data = request.json
    session_name = data["session_name"]
    session_table = db.table("sessions")
    session_id = session_table.insert({
        "session_name": session_name,
        "session_vector": [],
        "seen_vehicule_ids": [],
        "response_sequences": []
    })

    return {
        "success": True,
        "error_message": None,
        "session_id": session_name
    }


@app.post("/delete_session")
@cross_origin()
def delete_session():
    data = request.json
    session_name = data["session_name"]
    session_table = db.table("sessions")
    session_table.remove(Query().session_name == session_name)

    return {
        "success": True,
        "error_message": None
    }


@app.post("/get_sessions")
@cross_origin()
def get_sessions():
    session_table = db.table("sessions")

    return {
        "success": True,
        "error_message": None,
        "sessions": session_table.all()
    }



def search_bing_images(query):
    url = "https://www.bing.com/images/search?q=" + query
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    for a in soup.find_all("a", class_="iusc"):
        try:
            img_data = a["m"]
            img_data_dict = eval(img_data)
            high_res_img_url = img_data_dict["murl"]
            print(high_res_img_url)
            return high_res_img_url
        except KeyError:
            print("Failed to get image")
            continue

import simplejson as json

@app.post("/get_recommendation")
@cross_origin()
def get_recommendation():
    data = request.get_json()
    session_id = data["session_id"]
    recommendation_strategy = "recommendation_strategies." + data["recommendation_strategy"]
    module = importlib.import_module(recommendation_strategy)
    recommend = getattr(module, 'recommend', None)
    if callable(recommend):
        result = recommend(db, session_id)
        session_vector = [float(x) for x in result[0]]
        db.table("sessions").update(
            {"session_vector": session_vector}, Query().session_name == session_id)
        result[1]["vehiculeImageURL"] = search_bing_images(f'{result[1]["brand"]} {result[1]["model"]} {result[1]["year"]} {result[1]["color"]}')
        try :
            del result[1]["car_vector"]
            del result[1]["similarity_scores"]
        except KeyError:
            pass
        return {
            "success": True,
            "recommendation": json.dumps(result[1], ignore_nan=True)

        }

    return {
        "success": False
    }

@app.post("/interact_with_rec")
@cross_origin()
def interact_with_rec():
    print("INTERACTED")
    data = request.get_json()
    session_id = data["session_id"]
    vehicule_id = data["vehicule_id"]
    reaction = data["reaction"]
    sv_id = db.table("sessions").search(
        Query().session_name == session_id)[0]["seen_vehicule_ids"]
    sv_id.append({"vehicule_id":vehicule_id,"reaction":reaction})
    db.table("sessions").update(
            {"seen_vehicule_ids": sv_id}, Query().session_name == session_id)
    return {
        "success": True
    }



@app.post("/get_recommendation_strategies")
@cross_origin()
def get_recommendation_strategies():
    rec_strats = db.table("rec_strats")

    return {
        "success": True,
        "recommendation_strategies": rec_strats.all()
    }


@app.post("/get_recommendation_strategies")
@cross_origin()
def reload_recommendation_strategies():
    rec_strats = db.table("rec_strats")
    # Iterate over all Python files in the directory
    for filename in os.listdir(RECOMMENDATION_STRAT_DIR):
        if filename.endswith('.py'):
            # Import the module and call the strategy_info function
            module_name = filename[:-3]  # remove the ".py" extension
            module = __import__(module_name)
            strategy_info = getattr(module, 'strategy_info', None)
            if callable(strategy_info):
                result = strategy_info()
                result["file_name"] = filename

                # Add the result to the TinyDB table
                db.insert(result)
    return {
        "success": True,
        "error": None
    }


parameter_weights = {"brand": 2, "model": 2, "price": 4, "year": 2, "km": 3, "fuel": 5,
                     "gearbox": 4, "color": 3, "doors": 1, "seats": 1, "fiscalPower": 2, "DINPower": 2, "critAir": 1}
textual_data = ["brand", "model", "fuel", "gearbox", "color"]


def map_to_num(dataf, colname):
    mapping = {item: i for i, item in enumerate(dataf[colname].unique())}
    dataf[colname+"_n"] = dataf[colname].apply(lambda x: mapping[x])
    return mapping


@app.post("/reload_vehicule_db")
@cross_origin()
def reload_vehicule_db():
    db.drop_table("cars")
    car_table = db.table("cars")
    car_df = pd.read_csv(CAR_CSV_PATH)
    car_base_df = car_df.copy().to_dict("records")
    mapping_dict = {}
    for param in textual_data:
        mapping_dict[param] = map_to_num(car_df, param)
    car_df["price"] = car_df["price"] / 1000
    car_df["km"] = car_df["km"] / 10000
    car_df["year"] = car_df["year"] - 1900

    car_vectors = {}
    for index, row in car_df.iterrows():
        car_vector = np.ndarray((32,))
        i = 0
        for param, weight in parameter_weights.items():
            if param in textual_data:
                car_vector[i:i+weight] = row[param+"_n"]
            else:
                car_vector[i:i+weight] = row[param]
                i += weight
        car_vectors[row["id"]] = car_vector
        car = car_base_df[index]
        car["car_vector"] = list(car_vector)
        car_table.insert(car)

    return {
        "success": True,
        "error_message": None
    }
