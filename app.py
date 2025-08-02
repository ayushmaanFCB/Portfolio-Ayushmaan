from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    jsonify,
    url_for,
    Response,
)
from flask_mail import Mail, Message
from pymongo.mongo_client import MongoClient
import os
from bson import ObjectId
from datetime import datetime
import cloudinary
from cloudinary.uploader import upload
from werkzeug.security import generate_password_hash, check_password_hash
from pprint import pprint
import markdown, re
from dotenv import load_dotenv

load_dotenv()
application = Flask(__name__)
application.secret_key = str(os.urandom(24))

ADMIN_USERNAME = "ayushmaanFCB"
ADMIN_PASSWORD_HASH = generate_password_hash(os.environ.get("admin_portal_password"))

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
    notes_collection = db["Notes-and-Materials"]
except Exception as e:
    print("Failed to connect to Mongo DB Database : ", e)

try:
    cloudinary_api_key = os.environ.get("cloudinary_api_key")
    cloudinary_api_secret = os.environ.get("cloudinary_api_secret")
    cloudinary.config(
        api_key=cloudinary_api_key,
        api_secret=cloudinary_api_secret,
        cloud_name="dpviprc3b",
    )
except Exception as e:
    print("Failed to configure Cloudinary services : ", e)


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


@application.template_filter("nl2br")
def nl2br(value):
    # Replace newlines with <br> tags
    return re.sub(r"\n", "<br>", value)


@application.route("/blog", methods=["GET"])
def blog():
    # Get the filter parameters from the request
    sort_by = request.args.get("sort", "date_desc")  # Default to sorting by newest
    blog_type = request.args.get("type", "")  # Default to no filter
    date_range = request.args.get("date_range", "")

    # Build MongoDB filter query
    filter_query = {}
    if blog_type:
        filter_query["type"] = blog_type
    if date_range:
        filter_query["created_at"] = {"$gte": datetime.strptime(date_range, "%Y-%m-%d")}

    # Sort the blogs based on the sort_by parameter
    if sort_by == "date_desc":
        sort_order = [("created_at", -1)]  # Descending order (newest first)
    elif sort_by == "date_asc":
        sort_order = [("created_at", 1)]  # Ascending order (oldest first)
    elif sort_by == "popularity":
        sort_order = [("upvotes", -1)]  # Sort by popularity (upvotes)

    # Query MongoDB for blogs with filters applied
    blogs = list(blogs_collection.find(filter_query).sort(sort_order))

    # Format the date
    for blog in blogs:
        if "created_at" in blog:
            blog["created_at"] = blog["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        # if "content" in blog:
        #     blog["content"] = markdown.markdown(blog['content'])

    # Get the unique date ranges for the dropdown
    date_ranges = sorted(set(blog["created_at"][:10] for blog in blogs))

    # Render the template with the selected filter values
    return render_template(
        "blogs.html",
        blogs=blogs,
        date_ranges=date_ranges,
        sort_by=sort_by,
        blog_type=blog_type,
        date_range=date_range,
    )


@application.route("/upvote/<blog_id>", methods=["POST"])
def toggle_upvote(blog_id):
    blog = blogs_collection.find_one({"_id": ObjectId(blog_id)})
    upvote = blog["upvotes"]

    if blog:
        # Adjust the upvote count
        new_count = blog["upvotes"] + 1
        new_count = max(0, new_count)  # Prevent negative count

        # Update the database
        blogs_collection.update_one(
            {"_id": ObjectId(blog_id)}, {"$set": {"upvotes": new_count}}
        )

        # Respond with the new count and state
        return jsonify({"newCount": new_count, "upvoted": upvote})
    else:
        return jsonify({"error": "Blog not found"}), 404


@application.route("/subscribed", methods=["POST"])
def subscribed():
    name = request.form.get("userName")
    email = request.form.get("userEmail")
    subscribers_collection.insert_one({"name": name, "email": email})
    print(f"New subscription added to Database: {email}")
    return redirect(url_for("blog"))


def send_notifications(subject, template, context):
    subscribers = subscribers_collection.find()
    for subscriber in subscribers:
        name = subscriber["name"]
        email = subscriber["email"]

        html_content = render_template(template, name=name, **context)

        msg = Message(
            subject=subject,
            recipients=[email],
            html=html_content,
        )
        mail.send(msg)


@application.route("/admin")
def admin():
    auth = request.authorization
    if (
        not auth
        or auth.username != ADMIN_USERNAME
        or not check_password_hash(ADMIN_PASSWORD_HASH, auth.password)
    ):
        return Response(
            "Access Denied: Please provide valid credentials.",
            401,
            {"WWW-Authenticate": 'Basic realm="Admin Login"'},
        )
    print("Logged in as Administrator : ", ADMIN_USERNAME, " at", str(datetime.now()))
    return render_template("admin.html")


@application.route("/upload/project", methods=["POST"])
def upload_project():
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form["tags"].split(",")
    images = request.files.getlist("images")

    uploaded_urls = []
    for image in images:
        response = upload(image, folder="Portfolio")
        uploaded_urls.append(response["url"])

    project_data = {
        "title": title,
        "content": content,
        "tags": tags,
        "images": uploaded_urls,
        "created_at": datetime.utcnow(),
        "type": "project",
        "upvotes": 0,
    }
    blogs_collection.insert_one(project_data)

    try:
        send_notifications(
            subject=f"New Project: {title}",
            template="project_notification.html",
            context={"title": title, "content": content, "tags": tags},
        )
        print("Notification sent successfully!!!")
    except Exception as e:
        print("Error sending notification : ", e)

    return jsonify({"message": "Project uploaded successfully!"}), 201


@application.route("/upload/update", methods=["POST"])
def upload_update():
    content = request.form["content"]

    update_data = {
        "content": content,
        "created_at": datetime.utcnow(),
        "type": "updates",
        "upvotes": 0,
    }
    blogs_collection.insert_one(update_data)

    try:
        send_notifications(
            subject="New Update Posted!",
            template="updates_notification.html",
            context={"content": content},
        )
        print("Notification sent successfully!!!")
    except Exception as e:
        print("Error sending notification : ", e)

    return jsonify({"message": "Update uploaded successfully!"}), 201


@application.route("/notes")
def notes_page():
    try:
        notes = list(notes_collection.find().sort("date", -1))  # newest first
        upcoming_notes = []
        for note in notes:
            if note["published"]:
                note["date"] = note.get("date", datetime.utcnow()).strftime("%Y-%m-%d")
            else:
                upcoming_notes.append(note)
        notes = [note for note in notes if note.get("published")]

        return render_template("notes.html", notes=notes, upcoming_notes=upcoming_notes)
    except Exception as e:
        print("Error fetching notes:", e)
        return render_template("notes.html", notes=[], upcoming_notes=[])


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000, debug=True)
