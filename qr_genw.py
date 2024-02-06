import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import os

def add_logo_with_text_to_qr(qr_img, logo_path, text):
    # Open het QR-code en logo afbeeldingen
    qr = qr_img.copy()  # Maak een kopie van de QR-code afbeelding om te bewerken
    logo = Image.open(logo_path).convert("RGBA")

    # Bereken de grootte van het logo (bijvoorbeeld 1/4 van de QR-code grootte)
    qr_width, qr_height = qr.size
    logo_width, logo_height = logo.size

    # Bereken de positie om het logo in het midden van de QR-code te plaatsen
    position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

    # Voeg het logo toe aan de QR-code
    qr.paste(logo, position, logo)

    # Voeg tekst toe onder het logo
    draw = ImageDraw.Draw(qr)
    font = ImageFont.truetype("fonts/SourceSansPro-Bold.ttf", 30)

    # Bereken de grootte van de tekst met behulp van textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)

    # Bereken de positie om de tekst in het midden onder het logo te plaatsen
    text_width = text_bbox[2] - text_bbox[0]
    text_position = ((qr_width - text_width) // 2, position[1] + logo_height + 10)

    draw.text(text_position, text, fill=(0, 0, 0), font=font)

    return qr

def genereer_qr_en_afbeelding(url, subtekst, afdeling):
    # Maak QR-code
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#009844", back_color="#ffffff")

    # Voeg het logo en tekst toe aan de QR-code afbeelding
    logo_path = "static/images/GB.png"  # Pad naar je logo afbeelding
    text_under_logo = "Wijchmaal"  # Tekst die onder het logo moet worden toegevoegd
    qr_img_with_logo_and_text = add_logo_with_text_to_qr(qr_img, logo_path, text_under_logo)

    # Maak achtergrondafbeelding
    img = Image.new("RGB", (700, 900), (0, 152, 68))
    draw = ImageDraw.Draw(img)

    # Voeg QR-code toe aan achtergrondafbeelding
    qr_pos = (img.width // 2 - qr_img_with_logo_and_text.width // 2, 100)
    img.paste(qr_img_with_logo_and_text, qr_pos)

    # Voeg tekst toe
    font = ImageFont.truetype("fonts/SourceSansPro-Bold.ttf", 40)
    
    # Bereken de positie om de tekst in het midden onder de QR-code te plaatsen
    text_bbox = draw.textbbox((0, 0), text_under_logo, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_pos = ((img.width - text_width) // 2, qr_pos[1] + qr_img_with_logo_and_text.height + 20)

    draw.text((10, 10), f"Gezinsbond {afdeling}", (255, 255, 255), font=font)
    draw.text(text_pos, text_under_logo, (255, 255, 255), font=font)

    # Sla de resulterende afbeelding op in BytesIO object voor Flask response
    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)

    return img_io
