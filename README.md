# 🎯 Phishing Simulation Platform (Flask + Mailtrap)

A lightweight phishing simulation tool built with **Flask**, **Flask-Mail**, and **SQLite**.  
It lets security teams send simulated phishing emails to test staff awareness.  
Tracks both **opens** (via 1x1 tracking pixel) and **clicks** (via unique tracking links).

---

## 🚀 Features
- Send simulated phishing campaigns via [Mailtrap](https://mailtrap.io/)
- Tracks:
  - **Email opened** (tracking pixel)
  - **Link clicked**
- SQLite database to store campaign results
- Web interface for campaign history
- Flask-Mail integration with Mailtrap sandbox

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)
- **Database**: SQLite + SQLAlchemy
- **Mail**: Flask-Mail (Mailtrap SMTP)
- **Frontend**: Jinja2 templates

---

## 📂 Project Structure
phishing-sim/
│── app.py # Main Flask app
│── phishing.db # SQLite database (auto-created)
│── templates/ # HTML templates
│ ├── index.html
│ └── tracked.html
│── .env # Secrets (Mailtrap credentials)
│── .gitignore
│── README.md


---

## ⚙️ Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/phishing-sim.git
   cd phishing-sim

Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate # Linux/Mac

Install dependencies

pip install -r requirements.txt

Create .env file
SECRET_KEY=supersecretkey
MAILTRAP_USERNAME=your_mailtrap_username
MAILTRAP_PASSWORD=your_mailtrap_password

SECRET_KEY=supersecretkey
MAILTRAP_USERNAME=your_mailtrap_username
MAILTRAP_PASSWORD=your_mailtrap_password

Run the app
python app.py
Open in browser:
http://127.0.0.1:5000

Usage

Enter recipient email, subject, and body.

Email contains:

Tracking pixel to detect opens

Tracking link to detect clicks

Dashboard shows all campaigns with open/click status.

[![Phishing Simulation Banner](/images/ph1.PNG)]
[![Phishing Simulation Banner](/images/ph2.PNG)]
[![Phishing Simulation Banner](/images/ph3.PNG)]
