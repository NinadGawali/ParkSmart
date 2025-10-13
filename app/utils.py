# app/utils.py
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from flask import current_app

def format_receipt_email(receipt_data):
    """Format receipt data into a professional HTML email"""
    # Minimal safe HTML template, based on your provided style
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8"/>
      <style>
        body {{ font-family: Arial, sans-serif; color: #333; padding: 18px; }}
        .container {{ max-width:650px; margin:0 auto; border:1px solid #eee; padding:18px; border-radius:8px; }}
        .header {{ text-align:center; margin-bottom:12px; }}
        .company {{ font-weight:700; color:#0ea5e9; font-size:20px; }}
        .section {{ margin-top:12px; }}
        .label {{ font-weight:600; display:inline-block; width:140px; color:#222; }}
        .value {{ color:#444; }}
        .amount {{ margin-top:14px; background:#f7fafc; padding:10px; border-radius:6px; font-weight:700; text-align:center; }}
        .footer {{ margin-top:18px; font-size:12px; color:#777; text-align:center; }}
        a.btn {{ display:inline-block; padding:8px 12px; background:#0369a1; color:#fff; text-decoration:none; border-radius:4px; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="company">ParkSmart</div>
          <div style="margin-top:6px;color:#666;font-size:14px">Booking Receipt</div>
        </div>

        <div class="section">
          <div class="label">Name:</div><div class="value">{receipt_data.get('Name') or receipt_data.get('username') or '-'}</div>
        </div>

        <div class="section">
          <div class="label">Booking ID:</div><div class="value">{receipt_data.get('booking_id') or '-'}</div>
        </div>

        <div class="section">
          <div class="label">Parking:</div><div class="value">{receipt_data.get('parking_title') or receipt_data.get('Parking') or '-'}</div>
        </div>

        <div class="section">
          <div class="label">Location:</div><div class="value">{receipt_data.get('parking_address') or receipt_data.get('Address') or '-'}</div>
        </div>

        <div class="section">
          <div class="label">When:</div>
          <div class="value">{receipt_data.get('time_start','-')} to {receipt_data.get('time_end','-')}</div>
        </div>

        <div class="amount">Amount Paid: ₹{receipt_data.get('total_amount') or receipt_data.get('Amount Paid') or '0'}</div>

        {f'<p style="text-align:center;margin-top:12px"><a class="btn" href="{receipt_data.get("google_map_url")}" target="_blank">Open in Google Maps</a></p>' if receipt_data.get("google_map_url") else ''}

        <div class="footer">
          <div>Thank you for using ParkSmart</div>
          <div style="margin-top:8px">Generated: {receipt_data.get("generated_on", datetime.utcnow().isoformat())}</div>
        </div>
      </div>
    </body>
    </html>
    """
    return html_content

def send_email(to_addr: str, subject: str, receipt_data: dict) -> bool:
    """
    Send an email (HTML + plain text fallback) using SMTP credentials from env variables.
    Returns True on success, False on failure.
    """
    # Prefer env vars; fall back to Flask config if running inside app context
    smtp_host = os.getenv("SMTP_HOST") or os.getenv("EMAIL_HOST") or (current_app.config.get("SMTP_HOST") if current_app else None)
    smtp_port = int(os.getenv("SMTP_PORT") or os.getenv("EMAIL_PORT") or (current_app.config.get("SMTP_PORT") if current_app else 587))
    smtp_user = os.getenv("SMTP_USER") or os.getenv("EMAIL_USER") or (current_app.config.get("SMTP_USER") if current_app else None)
    smtp_pass = os.getenv("SMTP_PASS") or os.getenv("EMAIL_PASS") or (current_app.config.get("SMTP_PASS") if current_app else None)
    from_addr = os.getenv("EMAIL_FROM") or smtp_user or os.getenv("EMAIL_USER")

    if not (smtp_host and smtp_port and smtp_user and smtp_pass and to_addr):
        try:
            current_app.logger.warning("Incomplete SMTP config or missing recipient; cannot send email.")
        except Exception:
            pass
        return False

    # Build email message
    html_body = format_receipt_email(receipt_data)
    text_body = (
        f"Booking Receipt\n\n"
        f"Booking ID: {receipt_data.get('booking_id')}\n"
        f"Parking: {receipt_data.get('parking_title') or receipt_data.get('Parking')}\n"
        f"Location: {receipt_data.get('parking_address') or receipt_data.get('Address')}\n"
        f"When: {receipt_data.get('time_start')} to {receipt_data.get('time_end')}\n"
        f"Amount: ₹{receipt_data.get('total_amount') or receipt_data.get('Amount Paid')}\n\n"
        f"Open in Google Maps: {receipt_data.get('google_map_url','N/A')}\n\n"
        "Thank you,\nParkSmart"
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
                smtp.login(smtp_user, smtp_pass)
                smtp.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(smtp_user, smtp_pass)
                smtp.send_message(msg)
        try:
            current_app.logger.info("Email sent to %s", to_addr)
        except Exception:
            pass
        return True
    except Exception as e:
        try:
            current_app.logger.exception("Failed to send email: %s", e)
        except Exception:
            print("Failed to send email:", e)
        return False
