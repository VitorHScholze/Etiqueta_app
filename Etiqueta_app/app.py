import streamlit as st
import pandas as pd
import qrcode
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
 
st.title("Etiquetas 65x25 mm com QR Code")
 
file = st.file_uploader("Envie o Excel", type=["xlsx"])
 
if file:
    df = pd.read_excel(file)
    st.dataframe(df)
 
    if st.button("Gerar PDF"):
 
        buffer = BytesIO()
 
        largura = 6.5 * cm
        altura = 2.5 * cm
 
        c = canvas.Canvas(buffer, pagesize=(largura, altura))
 
        for i, row in df.iterrows():
            texto = str(row[0])
 
            qr = qrcode.make(texto)
            qr_io = BytesIO()
            qr.save(qr_io)
            qr_io.seek(0)
 
            qr_size = altura - 0.2*cm
 
            c.drawImage(
                ImageReader(qr_io),
                0.1*cm,
                0.1*cm,
                qr_size,
                qr_size
            )
 
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
