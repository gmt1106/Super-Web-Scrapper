from flask import Flask, render_template, request, redirect,send_file
from scrapper import extract_so_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

# data base that save the previous search 
data_base = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get("word")
  if word:
    word = word.lower()
    form_data_base = data_base.get(word)
    # if the job is searched previously, find it from data base else call scrapper and save the result to the data base
    if form_data_base:
      jobs = form_data_base
    else:
      jobs = extract_so_jobs(word)
      data_base[word] = jobs
  else:
    # if user didn't search for anything, go back to home page
    return redirect("/")

  # Flask render html and replace the varaibles
  return render_template(
    "report.html", 
    searchingFor = word, 
    resultNumber = len(jobs),
    jobs = jobs
    )

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception();
    word = word.lower()
    jobs = data_base.get(word)
    if not jobs:
      raise Exception();
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

# < and > represent placeholder
# you must use the placeholder in the dunction
@app.route("/<username>")
def contact(username):
  return f"hello, {username}"

app.run(host = "0.0.0.0")