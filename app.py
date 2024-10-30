from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from pymongo.mongo_client import MongoClient
import os

application = Flask(__name__)


try:
    application.config["MAIL_SERVER"] = "smtp.gmail.com"
    application.config["MAIL_PORT"] = 587
    application.config["MAIL_USE_TLS"] = True
    application.config["MAIL_USERNAME"] = "dasayush5maan@gmail.com"
    application.config["MAIL_PASSWORD"] = os.environ.get("mail_app_key")
    application.config["MAIL_DEFAULT_SENDER"] = "dasayush5maan@gmail.com"
    application.secret_key = str(os.urandom(24))
    mail = Mail(application)
except Exception as e:
    print("Failed to connect Mail Service : ", e)

try:
    cluster = MongoClient(os.environ.get("mongodb_uri"))
    db = cluster["Personal-Portfolio"]
    collection = db["Koyeb-Flask-Application"]
except Exception as e:
    print("Failed to connect to Mongo DB Database : ", e)


@application.route("/")
def home_page_alt():
    return render_template("home.html")


@application.route("/home")
def home_page():
    return render_template("home.html")


@application.route("/projects")
def project_page():
    return render_template("projects2.html")


@application.route("/resume")
def resume_page():
    return render_template("resume.html")


@application.route("/skills")
def skills_page():
    return render_template("skills.html")


@application.route("/contact")
def contact_form():
    return render_template("contact.html")


@application.route("/submit", methods=["POST"])
def submit_form():
    try:
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "organization": request.form["organization"],
            "position": request.form["position"],
            "website": request.form["website"],
            "linkedin": request.form["linkedin"],
            "message": request.form["message"],
        }

        msg = Message(
            subject="Knock Knock, someone wants to contact",
            recipients=[application.config["MAIL_DEFAULT_SENDER"]],
            body=f"""
                You have a new visitor on your portfolio website:

                Full Name: {data["name"]}
                Email Address: {data["email"]}
                Phone Number: {data["phone"]}
                Organization: {data["organization"]}
                Position: {data["position"]}
                Website: {data["website"]}
                LinkedIn: {data["linkedin"]}
                Message: {data["message"]}
                """,
        )

        try:
            mail.send(msg)
        except Exception as e:
            print("Error sending mail : ", e)

        try:
            collection.insert_one(data)
            flash("Your form has been submitted successfully!", "success")
        except Exception as e:
            print("Error inserting data : ", e)

        return redirect("/")
    except Exception as e:
        print(e)
        return redirect("/")


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000, debug=True)
