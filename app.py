from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_mail import Mail, Message
from pymongo.mongo_client import MongoClient
import os
from bson import ObjectId

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
    blogs_collection = db["Blogs"]
    subscribers_collection = db["Subscribers"]
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


@application.route(
    "/send-notification",
)
def send_notifications():
    subscribers = subscribers_collection.find()
    for subscriber in subscribers:
        name = subscriber["name"]
        email = subscriber["email"]
        msg = Message(
            subject=f"Knock Knock {name}, Ayushmaan just posted an update",
            recipients=[email],
            body=f"""
                new bloggggg...""",
        )

        mail.send(msg)


@application.route("/blog")
def blog():
    blogs = list(blogs_collection.find().sort("created_at", -1))

    for blog in blogs:
        if "created_at" in blog:
            blog["created_at"] = blog["created_at"].strftime("%Y-%m-%d %H:%M:%S")

    date_ranges = sorted(set(blog["created_at"][:10] for blog in blogs))
    return render_template("blogs.html", blogs=blogs, date_ranges=date_ranges)


@application.route("/upvote/<blog_id>", methods=["POST"])
def toggle_upvote(blog_id):

    # Find the blog
    blog = blogs_collection.find_one({"_id": ObjectId(blog_id)})
    upvote = blog["upvotes"]

    print(blog)
    if blog:
        # Adjust the upvote count
        new_count = blog["upvotes"] + (1 if upvote else -1)
        new_count = max(0, new_count)  # Prevent negative count

        # Update the database
        blogs_collection.update_one(
            {"_id": ObjectId(blog_id)}, {"$set": {"upvotes": new_count}}
        )

        # Respond with the new count and state
        return jsonify({"newCount": new_count, "upvoted": upvote})
    else:
        return jsonify({"error": "Blog not found"}), 404


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8080, debug=True)
