from flask import Flask, render_template, request, redirect, url_for
import boto3
import random

app = Flask(__name__)

s3 = boto3.client('s3')
bucket_name = 'portolio-contacts'


@app.route("/")
def home_page_alt():
    return render_template("home.html")


@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/projects")
def project_page():
    return render_template("projects.html")


@app.route("/resume")
def resume_page():
    return render_template("resume.html")


@app.route("/skills")
def skills_page():
    return render_template("skills.html")


@app.route("/contact")
def contact_form():
    return render_template("contact.html")


@app.route("/submit", methods=["POST"])
def submit_form():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        org = request.form['organization']
        msg = request.form["message"]

        file_name = f"{name}{random.randint(1000, 9999)}.txt"
        file_content = f"""NAME : {name} \nCONTACT : {phone} \nEMAIL : {email} \nORGANIZATION : {org} \n\n{msg}"""

        s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

        return redirect("/")
    except Exception as e:
        print(e)
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
