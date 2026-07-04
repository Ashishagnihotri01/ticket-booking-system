import qrcode
import io

class QRService:
    @staticmethod
    def generate_booking_qr(booking_ref: str) -> bytes:
        """Generates a QR code for a booking reference and returns image bytes."""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(booking_ref)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()