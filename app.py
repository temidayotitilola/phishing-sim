from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import base64

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Flask-Mail configuration (Mailtrap sandbox)
app.config["MAIL_SERVER"] = "sandbox.smtp.mailtrap.io"
app.config["MAIL_PORT"] = 2525
app.config["MAIL_USERNAME"] = os.getenv("MAILTRAP_USERNAME", "your_mailtrap_username")
app.config["MAIL_PASSWORD"] = os.getenv("MAILTRAP_PASSWORD", "your_mailtrap_password")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///phishing.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

mail = Mail(app)
db = SQLAlchemy(app)

# ------------------ Database Models ------------------
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    opened = db.Column(db.Boolean, default=False)
    clicked = db.Column(db.Boolean, default=False)


# ------------------ Routes ------------------
@app.route("/")
def index():
    campaigns = Campaign.query.all()
    return render_template("index.html", campaigns=campaigns)


@app.route("/send", methods=["POST"])
def send():
    recipient = request.form.get("email")
    subject = request.form.get("subject")
    body = request.form.get("body")

    if not recipient or not subject or not body:
        flash("All fields are required!", "danger")
        return redirect(url_for("index"))

    # Save the campaign first so it gets an ID
    campaign = Campaign(recipient=recipient, subject=subject, body=body)
    db.session.add(campaign)
    db.session.commit()

    # Create real tracking links with campaign.id
    tracking_url = url_for("track_click", campaign_id=campaign.id, _external=True)
    open_url = url_for("track_open", campaign_id=campaign.id, _external=True)

    # Inject tracking pixel + link into body
    tracked_body = f"""{body}
    <br><br>
    <img src='{open_url}' width='1' height='1'>
    <br><a href='{tracking_url}'>Verify Account</a>
    """

    # Update campaign with tracked body
    campaign.body = tracked_body
    db.session.commit()

    # Send phishing email
    msg = Message(subject, sender="admin@phishing-sim.com", recipients=[recipient])
    msg.html = tracked_body
    mail.send(msg)

    flash(f"Phishing email sent to {recipient}", "success")
    return redirect(url_for("index"))


@app.route("/track/open/<int:campaign_id>")
def track_open(campaign_id):
    """Mark campaign as opened + return a transparent pixel"""
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.opened = True
    db.session.commit()

    # Tiny transparent GIF (1x1 pixel)
    pixel_gif = base64.b64decode(
        "R0lGODlhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs="
    )
    return Response(pixel_gif, mimetype="image/gif")


@app.route("/track/click/<int:campaign_id>")
def track_click(campaign_id):
    """Mark campaign as clicked + show a landing page"""
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.clicked = True
    db.session.commit()
    return render_template("tracked.html", campaign=campaign)


# ------------------ Run ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
