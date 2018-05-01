import requests
from bs4 import BeautifulSoup
import json
import csv
import sys

#URL = "http://documentclassifier-env.us-east-2.elasticbeanstalk.com"
URL = sys.argv[1]

def home_page_check():
	page = requests.get(URL)
	soup = BeautifulSoup(page.text,"html.parser")
	assert 1 == len(soup.find_all(id = "submit")),"Error loading the submit button"
	assert 1 == len(soup.find_all(id = "message")),"Error loading the text input"

def load_test_case():
	global test_case_data 
	test_case_data = {"label":[],"document":[]}
	with open("test_case.csv") as test_file:
	    csv_reader = csv.reader(test_file)
	    for line in csv_reader:
	        test_case_data["document"].append(line[0])
	        test_case_data["label"].append(line[1])

def post_json_check():
	#load_test_case()
	json_url = URL+"/jsonify?words={0}".format(test_case_data["document"][0])
	test_case_page = requests.get(json_url)
	prediction_test_page = json.loads(test_case_page.text)
	assert prediction_test_page["prediction"] == test_case_data["label"][0],"Json prediction not working as intended"

def post_text_check():
	#load_test_case()
	text_url = URL+"/predict?words={0}".format(test_case_data["document"][0])
	test_case_page = requests.get(text_url)
	prediction_test_page = test_case_page.text.split(":")[-1]
	assert prediction_test_page == test_case_data["label"][0], "Text prediction not working as intended"

def test_main():
	home_page_check()
	print("Page working good!")
	load_test_case()
	print("Loaded test case")
	post_text_check()
	print("Content header text works fine!")
	post_json_check()
	print("Content header json works fine!")

if __name__ == "__main__":
	test_main()