import os
from tinydb import TinyDB, Query
import tensorflow as tf
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

base_path = os.path.dirname(os.path.abspath(__file__))


def strategy_info():
    return {
        "strategy_name": "Base Recommendation Model"
    }

def recommend(db_ref: TinyDB, session_name: str):
    model = tf.keras.models.load_model(os.path.join(base_path,"./base_model7"))
    cars = db_ref.table("cars").all()
    car_table = pd.DataFrame(cars)
    car_table.reindex(index=car_table["id"])
    SessionQuery = Query()
    session = db_ref.table("sessions").search(
        SessionQuery.session_name == session_name)[0]
    seen_vehicule_ids = [inter["vehicule_id"] for inter in session["seen_vehicule_ids"] ]
    try :
        car_table["id"].drop(seen_vehicule_ids)
    except:
        pass

        

    if len(session["seen_vehicule_ids"]) == 0:
        last_seen_car = [0] * 32
        return (np.array([0.0]*32), car_table.sample(n=1).iloc[0].to_dict())
    else:
        last_seen_car = db_ref.table("cars").search(Query().id == session["seen_vehicule_ids"][-1]["vehicule_id"])[0]["car_vector"]
        
    
    if len(session["session_vector"]) < 1:
        sessvec = np.array([0]*(32+16*2 +32))
    else:
        sessvec = np.array([session["seen_vehicule_ids"][-1]["reaction"]]*16 + session["session_vector"] + [session["seen_vehicule_ids"][-1]["reaction"]]*16 + last_seen_car)

    sessvec = sessvec.reshape(1, -1)

    input1 = np.array([last_seen_car])
    input2 = np.array([session["session_vector"]])
    input3 = np.array([session["seen_vehicule_ids"][-1]["reaction"]])
    print("input1 : \n")
    print(input1)
    print("input2 : \n")
    print(input2)
    print("input3 : \n")
    print(input3)
    ideal_car = model.predict([input1, input2, input3])
    
    print("\n IDEAL CAR : \n")
    print(ideal_car)
    
    def func(row, ideal_car):

        return cosine_similarity(np.nan_to_num(row["car_vector"]).reshape(1,-1), np.nan_to_num(np.array(ideal_car).reshape(1,-1)))
    car_table["similarity_scores"] = car_table.apply((lambda row : func(row,ideal_car)),axis=1)
    recommended_car = car_table.sort_values("similarity_scores",ascending=False).iloc[0].to_dict()
    
    return (ideal_car[0], recommended_car)