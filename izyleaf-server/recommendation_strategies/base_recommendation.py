import os
from tinydb import TinyDB, Query
import tensorflow as tf
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

base_path = os.path.dirname(os.path.abspath(__file__))


def strategy_info():
    return {
        "strategy_name": "Base Recommendation Model"
    }

def recommend(db_ref: TinyDB, session_name: str):
    model = tf.keras.models.load_model(os.path.join(base_path,"./base_model"))
    cars = db_ref.table("cars").all()
    SessionQuery = Query()
    session = db_ref.table("sessions").search(
        SessionQuery.session_name == session_name)[0]
    print(session)
    if len(session["session_vector"]) != 32:
        sessvec = np.array([0]*64)
    else:
        sessvec = np.array(session["session_vector"] + [0]*32)

    # Reshape sessvec to have an extra dimension
    sessvec = sessvec.reshape(1, -1)

    ideal_car = model.predict(sessvec)
    car_vectors = {car["id"]: car["car_vector"] for car in cars if not (
        car["id"] in session["seen_vehicule_ids"])}

    # Convert dict_values to list before passing it to cosine_similarity
    car_vectors_values_no_nan = [np.nan_to_num(car_vec) for car_vec in car_vectors.values()]
    scores = cosine_similarity(car_vectors_values_no_nan, ideal_car)
    i = scores.argmax()
    recommended_car = cars[list(car_vectors.keys())[i]]

    return (ideal_car, recommended_car)