from flask import Flask, render_template, request, redirect, url_for
import boto3
import random

application = Flask(__name__)

s3 = boto3.client("s3")
bucket_name = "portolio-contacts"


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
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        org = request.form["organization"]
        msg = request.form["message"]

        file_name = f"{name}{random.randint(1000, 9999)}.txt"
        file_content = f"""NAME : {name} \nCONTACT : {phone} \nEMAIL : {email} \nORGANIZATION : {org} \n\n{msg}"""

        s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

        return redirect("/")
    except Exception as e:
        print(e)
        return redirect("/")


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=9000, debug=True)
