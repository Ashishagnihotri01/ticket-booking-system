import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from app.config import settings

class EmailService:
    @staticmethod
    def send_booking_confirmation(to_email: str, booking_ref: str, qr_bytes: bytes):
        """Dispatches real-time transactional reservation notifications incorporating a valid QR verification asset."""
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_FROM
        msg['To'] = to_email
        msg['Subject'] = f"Your Confirmed Ticket Booking - {booking_ref}"

        body = f"Thank you for your booking! Your booking reference code is: {booking_ref}. Find your digital QR entrance code attached."
        msg.attach(MIMEText(body, 'plain'))

        image = MIMEImage(qr_bytes, name=f"{booking_ref}.png")
        msg.attach(image)

        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.SMTP_FROM, to_email, msg.as_string())
        except Exception as e:
            print(f"Failed to send email: {str(e)}")