from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        name = data.get('name', '')
        email = data.get('email', '')
        service = data.get('service', '')
        message = data.get('message', '')

        # Email configuration - set these as environment variables
        smtp_host = os.environ.get('SMTP_HOST', 'smtp.zoho.eu')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_user = os.environ.get('SMTP_USER', 'business@keizhouse.com')
        smtp_pass = os.environ.get('SMTP_PASS', '')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"New Inquiry from {name} — Keiz House Website"
        msg['From'] = smtp_user
        msg['To'] = 'business@keizhouse.com'
        msg['Reply-To'] = email

        html_body = f"""
        <div style="font-family: Georgia, serif; background: #0a0a0a; color: #f5f0e8; padding: 40px; max-width: 600px; margin: 0 auto;">
            <div style="border-left: 3px solid #c9a460; padding-left: 20px; margin-bottom: 30px;">
                <h2 style="color: #c9a460; margin: 0; font-size: 24px; letter-spacing: 2px;">NEW INQUIRY</h2>
                <p style="color: #888; margin: 5px 0 0;">Via keizhouse.com</p>
            </div>
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 12px 0; border-bottom: 1px solid #222; color: #888; width: 120px;">Name</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #222; color: #f5f0e8;">{name}</td></tr>
                <tr><td style="padding: 12px 0; border-bottom: 1px solid #222; color: #888;">Email</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #222; color: #c9a460;">{email}</td></tr>
                <tr><td style="padding: 12px 0; border-bottom: 1px solid #222; color: #888;">Service</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #222; color: #f5f0e8;">{service}</td></tr>
                <tr><td style="padding: 12px 0; color: #888; vertical-align: top;">Message</td>
                    <td style="padding: 12px 0; color: #f5f0e8;">{message}</td></tr>
            </table>
        </div>
        """

        msg.attach(MIMEText(html_body, 'html'))

        if smtp_pass:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
