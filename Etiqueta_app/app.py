import streamlit as st
import pandas as pd
import qrcode
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

st.title("Etiquetas 8x2 cm com QR Code")

file = st.file_uploader("Envie o Excel", type=["xlsx"])

if file:
    df = pd.read_excel(file)

    st.dataframe(df)

    if st.button("Gerar PDF"):

        buffer = BytesIO()

        largura = 8 * cm
        altura = 2 * cm

        c = canvas.Canvas(buffer, pagesize=(largura, altura))

        for i, row in df.iterrows():
            texto = str(row[0])

            # QR Code
            qr = qrcode.make(texto)
            qr_io = BytesIO()
            qr.save(qr_io)
            qr_io.seek(0)

            # Desenhar QR
            qr_size = altura - 0.2*cm
            c.drawImage(
                ImageReader(qr_io),
                0.1*cm,
                0.1*cm,
                qr_size,
                qr_size
            )

            # TEXTO EM NEGRITO
            c.setFont("Helvetica-Bold", 10)
            c.drawString(qr_size + 0.3*cm, altura/2, texto[:40])

            c.showPage()

        c.save()
        buffer.seek(0)

        st.download_button(
            "Baixar PDF",
            buffer,
            "etiquetas.pdf",
            "application/pdf"
        )