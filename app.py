from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import os

application = Flask(__name__)


application.config["MAIL_SERVER"] = "smtp.gmail.com"
application.config["MAIL_PORT"] = 587
application.config["MAIL_USE_TLS"] = True
application.config["MAIL_USERNAME"] = "dasayush5maan@gmail.com"
application.config["MAIL_PASSWORD"] = os.environ.get("mail-app-key")
application.config["MAIL_DEFAULT_SENDER"] = "dasayush5maan@gmail.com"
application.secret_key = str(os.urandom(24))
mail = Mail(application)


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
            "org": request.form["organization"],
            "msg": request.form["message"],
        }

        msg = Message(
            subject="You have a Visitor at your Portfolio website",
            recipients=[application.config["MAIL_DEFAULT_SENDER"]],
            body=f"{str(data)}",
        )
        mail.send(msg)
        flash("Your form has been submitted successfully!", "success")
        return redirect("/")
    except Exception as e:
        print(e)
        return redirect("/")


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=9000, debug=True)
