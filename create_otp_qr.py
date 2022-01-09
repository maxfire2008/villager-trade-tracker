import pyotp
import qrcode
import io

def create_otp_qr(key):
    totp = pyotp.TOTP(key)
    otp_uri = totp.provisioning_uri(issuer_name='villager-trade-tracker')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5,
    )

    qr.add_data(otp_uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io