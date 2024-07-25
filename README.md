
<img src="./Login/static/logo1.png" align='right' width=100 hight=100>

# DocWise

## Description

**DocWise** is a Django-based web application designed to manage medical consultations and reports. It includes features for uploading and processing medical reports, registering doctors, booking appointments, and engaging with a medical chatbot. The application also supports video calling for virtual consultations using WebRTC.

## Features

- **User Authentication**: Sign up, log in, and manage user sessions.
- **Doctor Management**: Register doctors and manage their details.
- **Medical Report Handling**: Upload and analyze medical reports using AI for summaries.
- **Appointment Booking**: Book appointments with doctors and receive confirmation emails.
- **Chatbot**: Interact with a medical chatbot for health-related advice.
- **Video Calling**: Conduct video calls with doctors using WebRTC.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/docwise.git
    cd docwise
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Install Node.js dependencies for Tailwind CSS:**

    ```bash
    npm install
    ```

6. **Set up environment variables:**

    Create a `.env` file in the project root and add the following:

    ```
    GEMINI_API_KEY=your_gemini_api_key
    ```

7. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

8. **Create a superuser (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

9. **Start the Django development server:**

    ```bash
    python manage.py runserver
    ```

10. **For WebSocket support, start Daphne (ASGI server):**

    ```bash
    daphne -p 8001 DocWise.asgi:application
    ```

    Note: Ensure Daphne is installed via `pip install daphne`.

11. **Build Tailwind CSS:**

    To build CSS:

    ```bash
    npm run build:css
    ```

    To watch for changes:

    ```bash
    npm run watch:css
    ```

## File Structure

```
docwise/
├── manage.py
├── docwise/
│   ├── __init__.py
│   ├── asgi.py
│   ├── consumers.py
│   ├── routing.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── ChatbotAndClass/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── consumers.py
├── Login/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── consumers.py
├── templates/
│   ├── chatbot.html
│   ├── upload_report.html
│   ├── search_doctors.html
│   ├── VideoCall.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   └── doctor_registration.html
├── static/
│   ├── styles.css
│   └── output.css
└── .env
```

## Tech Stack

- **Backend**: Django, Node.js , Daphne (for WebSocket support)
- **Frontend**: HTML, CSS, JavaScript, jQuery, Toastr.js, Tailwind CSS
- **Database**: SQLite (default), can be configured to use other databases
- **APIs**: Google Gemini API for generating content
- **WebRTC**: For video calling
- **Email**: SimpleGmail for sending appointment emails[refer SimpleGmail github]

## Additional Information

- **Daphne** is used as an ASGI server to support WebSockets. Ensure you have Daphne installed and running alongside your Django development server for WebRTC features to work.
- **Tailwind CSS** is used for styling. You need to build or watch the CSS files using npm commands.
- For WebRTC video calling, make sure you test it in a secure environment (e.g., using HTTPS). Localhost connections might require additional configuration for secure contexts.

