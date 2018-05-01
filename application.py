from flask import Flask, request, render_template

import numpy as np
from sklearn.externals import joblib
import pickle

VECTORIZER_PATH = "models/vectorizer.pk"
MODEL_PATH = "models/gradient_boosting.pkl"

application = Flask(__name__)

application.static_folder = 'static'

@application.route("/")
def home():
	load_model()
	return render_template("main.html")

@application.route("/", methods = ["POST"])
def predict():
	input_text = request.form["text"]
	test_features = vectorizer.transform([input_text]).toarray()
	prediction = model.predict(test_features)
	return "prediction:{0}".format(str(prediction[0]))

@application.route("/<words>")
def URL_predict(words):
	input_text = words.split("?")
	test_features = vectorizer.transform([words]).toarray()
	return "prediction:{0}".format(str(model.predict(test_features)[0]))

def load_model():
	global vectorizer
	global model
	vectorizer_file = open(VECTORIZER_PATH,"rb")
	vectorizer = pickle.load(vectorizer_file)
	vectorizer_file.close()

	model = joblib.load(MODEL_PATH)

if __name__ == "__main__":
	application.run(debug = True)
	
