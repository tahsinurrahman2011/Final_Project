from joblib import dump, load

MODEL_PATH = "model/model.joblib"

def save_model(model):
    dump(model, MODEL_PATH)

def load_model():
    return load(MODEL_PATH)