import streamlit as st
import pandas as pd
from datetime import datetime

# ตั้งค่าหน้าตา Web App ให้กว้างแบบมืออาชีพ
st.set_page_config(page_title="ระบบบริหารจัดการบันทึกข้อความ", page_icon="📑", layout="wide")

# CSS ตกแต่งอินเทอร์เฟซให้สวยงาม
st.markdown("""
<style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E293B; margin-bottom: 0px; }
    .sub-header { font-size: 15px; color: #64748B; margin-bottom: 20px; }
    .card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; }
    .stButton>button { background-color: #2563EB; color: white; border-radius: 6px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📑 บริหารจัดการบันทึกข้อความ</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">สร้าง ค้นหา และพิมพ์เอกสาร MEMORANDUM ได้อย่างมืออาชีพ</p>', unsafe_allow_html=True)

# สร้าง Session State สำหรับเก็บประวัติเอกสาร
if 'doc_history' not in st.session_state:
    st.session_state.doc_history = [
        {"Document ID": "DOC-2026/001", "Department": "Purchasing", "Subject": "ขออนุมัติจัดซื้ออุปกรณ์สำนักงาน", "Date": "2026-08-24", "Status": "Finalized"},
        {"Document ID": "DOC-2026/002", "Department": "IT", "Subject": "ขอต่ออายุซอฟต์แวร์ประมวลผล", "Date": "2026-08-24", "Status": "Draft"}
    ]

# แบ่งเลย์เอาต์หน้าจอเป็น 2 ฝั่ง (ฝั่งกรอกข้อมูล 65% / ฝั่ง Preview เอกสาร 35%)
col_form, col_preview = st.columns([1.8, 1.2], gap="large")

with col_form:
    st.markdown("### 📝 CREATE NEW DOCUMENT")
    with st.form("doc_create_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            doc_no = st.text_input("เลขที่เอกสาร", "DOC-2026/003")
        with c2:
            dept = st.selectbox("หน่วยงาน/ผู้จัดทำ", ["Purchasing", "IT Department", "HR", "Finance", "General Admin"])
        with c3:
            doc_date = st.date_input("วันที่เอกสาร", datetime.now())
            
        title = st.text_input("เรื่อง", "ขออนุมัติจัดซื้ออุปกรณ์ประจำสำนักงาน")
        
        c4, c5 = st.columns(2)
        with c4:
            receiver = st.text_input("เรียน (ผู้รับ)", "ผู้จัดการฝ่ายบริหาร")
        with c5:
            priority = st.selectbox("ความเร่งด่วน", ["ปกติ (Normal)", "ด่วน (Urgent)", "ด่วนที่สุด (Top Secret)"])

        content = st.text_area("เนื้อหาเอกสาร", "เนื่องด้วยมีความจำเป็นต้องจัดซื้ออุปกรณ์เพิ่มเติม เพื่อรองรับการทำงานของทีมงานในไตรมาสนี้ จึงขออนุมัติจัดซื้อตามรายการแนบ...", height=140)
        sign_name = st.text_input("ชื่อ-นามสกุล ผู้ลงนาม", "สมชาย ใจดี")

        btn_submit = st.form_submit_button("💾 บันทึกเอกสารและสร้างพรีวิว", use_container_width=True)

    if btn_submit:
        new_doc = {
            "Document ID": doc_no,
            "Department": dept,
            "Subject": title,
            "Date": str(doc_date),
            "Status": "Finalized"
        }
        st.session_state.doc_history.insert(0, new_doc)
        st.success("บันทึกข้อมูลและอัปเดตเอกสารเรียบร้อยแล้ว!")

    st.markdown("---")
    st.markdown("### 📋 RECENTLY CREATED DOCUMENTS")
    df = pd.DataFrame(st.session_state.doc_history)
    st.dataframe(df, use_container_width=True, hide_index=True)

with col_preview:
    st.markdown("### 👁️ DOCUMENT VIEWER")
    st.caption("ตัวอย่างเอกสารที่จะพิมพ์จริง (HTML Formatted)")
    
    # พรีวิวเอกสารจัดหน้าตาเรียบหรู พร้อมรองรับภาษาไทย 100%
    preview_html = f"""
    <div style="background-color: white; border: 1px solid #CBD5E1; padding: 30px; border-radius: 8px; font-family: 'Sarabun', sans-serif; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; margin-bottom: 20px; letter-spacing: 2px; color: #0F172A;">บันทึกข้อความ</h2>
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 14px;">
            <tr>
                <td style="padding: 4px 0;"><b>หน่วยงาน:</b> {dept}</td>
                <td style="padding: 4px 0; text-align: right;"><b>วันที่:</b> {doc_date.strftime('%d/%m/%Y')}</td>
            </tr>
            <tr>
                <td style="padding: 4px 0;" colspan="2"><b>เลขที่:</b> {doc_no}</td>
            </tr>
            <tr>
                <td style="padding: 4px 0;" colspan="2"><b>เรื่อง:</b> {title}</td>
            </tr>
            <tr>
                <td style="padding: 4px 0;" colspan="2"><b>เรียน:</b> {receiver}</td>
            </tr>
        </table>
        <hr style="border: 0.5px solid #E2E8F0; margin: 15px 0;">
        <div style="min-height: 150px; font-size: 14px; line-height: 1.6; color: #334155; white-space: pre-wrap;">
{content}
        </div>
        <div style="margin-top: 40px; text-align: right; font-size: 14px;">
            <p>ลงชื่อ .....................................................</p>
            <p style="margin-right: 20px;">( {sign_name} )</p>
        </div>
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # HTML สั่งพิมพ์ตรงผ่านเบราว์เซอร์ หน้าเป๊ะ ไม่เบี้ยว ภาษาไทยไม่เป็นต่างดาว
    print_script = f"""
    <script>
    function printDoc() {{
        var printContents = `{preview_html}`;
        var originalContents = document.body.innerHTML;
        var win = window.open('', '', 'height=700,width=900');
        win.document.write('<html><head><title>Print Document</title>');
        win.document.write('<link href="https://fonts.googleapis.com/css2?family=Sarabun&display=swap" rel="stylesheet">');
        win.document.write('<style>body {{ font-family: "Sarabun", sans-serif; padding: 40px; }}</style>');
        win.document.write('</head><body>');
        win.document.write(printContents);
        win.document.write('</body></html>');
        win.document.close();
        win.print();
    }}
    </script>
    <button onclick="printDoc()" style="width: 100%; background-color: #059669; color: white; border: none; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px;">
        🖨️ สั่งพิมพ์เอกสารทันที (Direct Print)
    </button>
    """
    st.components.v1.html(print_script, height=60)
