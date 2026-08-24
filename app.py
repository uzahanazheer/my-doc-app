import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="ระบบพิมพ์เอกสารกลาง", page_icon="📄")
st.title("📄 ระบบพิมพ์เอกสารและบันทึกข้อมูล")

with st.form("doc_form"):
    doc_no = st.text_input("เลขที่เอกสาร", "DOC-2026/001")
    sender = st.text_input("หน่วยงาน/ผู้จัดทำ", "แผนกเอกสาร")
    title = st.text_input("เรื่อง", "ขออนุมัติจัดซื้ออุปกรณ์")
    content = st.text_area("เนื้อหาเอกสาร", height=150)
    sign_name = st.text_input("ชื่อผู้ลงนาม", "สมชาย ใจดี")
    submitted = st.form_submit_button("🔨 สร้างเอกสาร PDF")

def generate_pdf(doc_no, sender, title, content, sign_name):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 80, "MEMORANDUM")
    
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 120, f"No: {doc_no}")
    c.drawString(50, height - 140, f"From: {sender}")
    c.drawString(50, height - 170, f"Subject: {title}")
    
    text_obj = c.beginText(50, height - 200)
    text_obj.setFont("Helvetica", 11)
    for line in content.split('\n'):
        text_obj.textLine(line)
    c.drawText(text_obj)
    
    c.drawString(350, 150, "Signature: .......................................")
    c.drawString(380, 130, f"( {sign_name} )")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

if submitted:
    pdf_data = generate_pdf(doc_no, sender, title, content, sign_name)
    st.success("สร้างเอกสารเรียบร้อย!")
    st.download_button("📥 ดาวน์โหลด PDF สั่งปริ้นท์", pdf_data, f"{doc_no}.pdf", "application/pdf")
