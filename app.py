from flask import Flask, url_for, render_template, redirect, request, session, flash
from datetime import timedelta
from portal_bot import PortalBot
from journey_list_generator import JourneyListGenerator
from fare_finder import FareFinderBot
from bs4 import BeautifulSoup
from collections import defaultdict
import json

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes = 5)

# pb = PortalBot(user="", password="")

@app.route("/", methods=["POST", "GET"])
def home():
	if request.method == "POST":
		return redirect(url_for("login"))
	else:
		return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		
		try:
			user = request.form["email"]
			password = request.form["pwd"]
			pb = PortalBot(user = user, password = password)
			pb.login()
			page_source = pb.get_page_source()
		except Exception as e:
			print("Credentials incorrect")
			return redirect(url_for("login", correct = False))
		
		print("login success")
		flash("Login successful")
		
		print("got page source")
		soup = BeautifulSoup(page_source, 'lxml')
		print("soup made")
		flash("Journeys fetched")

		jlg = JourneyListGenerator(soup = soup)
		# journeys = defaultdict(list)
		journeys = jlg.get_journey_list()

		journeys_file = open("journeys.json", "w")
		journeys_file.write(json.dumps(journeys))
		journeys_file.close()
		# journeys_json = json.dumps(journeys)
		# print(journeys_json)
		# journeys_string = json.stringify(journeys_json)

		session["user"] = user
		
		return redirect(url_for("user"))
	else:
		if "user" in session:
			flash("Already logged in")
			return redirect(url_for("user"))
		elif request.args.get("correct") == 'False':
			flash("Credentials incorrect")	

		return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
	
	# print(journeys)

	if request.method == "POST":
		json_file = open("journeys.json")
		data = json.load(json_file)
	# print(type(data))
		journeys = defaultdict(list, data)
		# return "dadad"
		ffb = FareFinderBot(journeys = journeys)
		ffb.begin_fare_search()

		list_length = len(ffb.jrn_list)
		jrn_list = ffb.jrn_list
		fares_list = ffb.fares_list
		# for i in range(jrn_list_length):


		# print(f"You would've paid {ffb.get_grand_total()} to TfL last month if you didn't have a Travelcard")
		return render_template("results.html", jrn_list = jrn_list, fares_list = fares_list, list_length = list_length)

	else:
		if "user" in session:
			user = session["user"]
			return render_template("user.html", user = user)
		else:
			flash("You are not logged in")
			return redirect(url_for("login"))
# journeys = json.load(request.args.get("journeys"))
	# print(type(request.args.get("journeys")))
	# jrns_json = request.args.get("journeys")
	# jrns_dict = json.load(jrns_json)
	# print(jrns_dict)
@app.route("/logout")
def logout():
	if "user" in session:
		user = session["user"]
		flash(f"you have been logged out, {user}", "info")
	session.pop("user", None)
	
	return redirect(url_for("home"))


if __name__ == "__main__":
	app.run(debug=True)