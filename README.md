# Personal Portfolio Application

This is a personal portfolio application built using Flask, designed to showcase my skills, projects, blogs, and resume. The website provides an interactive interface where visitors can learn more about me, view my work, and contact me through a form. Additionally, there's an admin interface to upload new projects and updates to the portfolio.

The application includes features such as:

- Displaying blogs and projects.
- A contact form for visitors to send messages.
- Subscription functionality to notify users of new updates and projects.
- An admin panel to upload new projects and updates, with notifications sent to subscribers.
- Blog and project upvote functionality for user engagement.

The portfolio application is deployed using Koyeb and can be accessed [here](https://homeless-margalo-ayushmaan-personal-109aa799.koyeb.app).

## Features

1. **Home Page**: A welcoming page with an introduction to my work and skills.
2. **Projects Page**: A section displaying various projects I’ve worked on, along with their descriptions and images.
3. **Resume Page**: A page displaying my professional background and achievements.
4. **Skills Page**: A breakdown of the skills I possess in various domains such as programming, web development, and more.
5. **Contact Form**: A contact form where visitors can submit their information and messages. The form data is sent to my email.
6. **Blog Page**: A blog section where I post updates, articles, and new projects. The blog is filterable by type and date.
7. **Upvote System**: Visitors can upvote blogs or projects to show appreciation.
8. **Admin Portal**: A restricted area where I can log in and upload new projects and updates. This section is protected by basic authentication.
9. **Email Notifications**: When new projects or updates are added, notifications are sent to subscribed users via email.

## Technologies Used

- **Flask**: A micro web framework for building the application.
- **MongoDB**: NoSQL database used to store the portfolio data, including blogs, subscribers, and contact form submissions.
- **Cloudinary**: Used to upload and store images for projects.
- **Flask-Mail**: Used to handle sending emails for contact form submissions and notifications.
- **Werkzeug**: A comprehensive WSGI web application library, which is used for password hashing.
- **Markdown**: Used to format content in blogs and projects.

## Setup & Installation

To set up this project locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ayushmaanFCB/Personal-Portfolio.git
   cd Personal-Portfolio
   ```

2. **Create a virtual environment** (if you don't have one already):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:

   You'll need to set the following environment variables:

   - `admin_portal_password`: The password for accessing the admin portal (used for basic authentication).
   - `mail_app_key`: The app key for your email service (for sending notifications and contact form responses).
   - `mongodb_uri`: The MongoDB URI connection string.
   - `cloudinary_api_key` and `cloudinary_api_secret`: Your Cloudinary API credentials.

   You can set these variables in your terminal, or use a `.env` file (recommended).

5. **Run the application**:

   ```bash
   python app.py
   ```

   The application will be hosted locally at `http://127.0.0.1:8000/`.

## Submodule for Testing

This repository includes a submodule for testing the application features:

- **[Selenium-TestNG-Portfolio](https://github.com/ayushmaanFCB/Selenium-TestNG-Portfolio.git)**: This repository contains Selenium-based tests using TestNG for end-to-end testing of the portfolio features. These tests ensure that the application is functioning as expected, including form submissions, blog upvotes, and admin panel functionality.

You can initialize and update the submodule by running:

```bash
git submodule update --init --recursive
```

Then, follow the instructions in the submodule repository to run the tests.

## Deployment

This application is deployed on Koyeb, a platform for deploying cloud-native applications. The live version of this portfolio is available [here](https://homeless-margalo-ayushmaan-personal-109aa799.koyeb.app).

## Notes

- The application is designed as a personal portfolio, so it’s not intended for public contributions.
- It includes a basic authentication system for the admin panel to manage and upload projects and updates.

## License

This project is not open for public use or contributions. All rights reserved to the author.

---
