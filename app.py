import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="ระบบออกใบเสร็จรับเงิน", page_icon="🧾", layout="wide")

# ฟังก์ชันอ่านไฟล์รูปภาพแล้วแปลงเป็น Base64 อัตโนมัติ
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

# ดึงรูปจากไฟล์ logo.png (หากไม่มีไฟล์จะแสดงภาพสำรองชั่วคราว)
LOGO_BASE64 = get_image_base64("logo.png")
if not LOGO_BASE64:
    # URL ภาพสำรองกรณีที่ยังไม่ได้ใส่ไฟล์ logo.png ในโฟลเดอร์
    LOGO_SRC = "https://via.placeholder.com/220x80.png?text=A%26K+Transport+Logo"
else:
    LOGO_SRC = LOGO_BASE64

# --- ฝั่งป้อนข้อมูล (UI Controls) ---
col_form, col_preview = st.columns([1, 1.2])

with col_form:
    st.header("📝 กรอกข้อมูลใบเสร็จ")
    
    doc_type = st.selectbox("ชนิดเอกสาร", ["ใบเสร็จรับเงิน (RECEIPT)", "ใบเสร็จรับเงิน/ใบกำกับภาษี"])
    receipt_date = st.text_input("วันที่", "12/03/2026")
    receipt_no = st.text_input("เลขที่ใบเสร็จ", "REC2026/03-001")
    
    st.subheader("ข้อมูลลูกค้า")
    customer_code = st.text_input("รหัสลูกค้า", "CUST-001")
    cust_name = st.text_input("ชื่อลูกค้า", "บริษัท ตัวอย่าง จำกัด")
    cust_address = st.text_area("ที่อยู่ลูกค้า", "123/45 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพฯ 10110")
    cust_taxid = st.text_input("เลขผู้เสียภาษี", "0105551234567")
    
    st.subheader("ข้อมูลการขนส่ง / รายการ")
    payment_term = st.text_input("เงื่อนไขการชำระเงิน", "เงินสด / โอน")
    driver_name = st.text_input("พนักงานขนส่ง", "นายสมชาย ใจดี")
    
    item_desc = st.text_input("รายการสินค้า/บริการ", "ค่าบริการขนส่งสินค้าตามเที่ยววิ่ง")
    item_qty = st.number_input("จำนวน", min_value=1, value=1)
    item_unit = st.text_input("หน่วย", "เที่ยว")
    item_price = st.number_input("ราคาต่อหน่วย", min_value=0.0, value=5000.0, step=100.0)
    
    st.subheader("วิธีการชำระเงิน")
    pay_method = st.radio("เลือกวิธีชำระเงิน", ["เงินสด", "เงินโอน", "เช็ค"])
    
    total_amount = item_qty * item_price
    formatted_price = f"{item_price:,.2f}"
    formatted_amount = f"{total_amount:,.2f}"
    
    chk_cash = "[ / ]" if pay_method == "เงินสด" else "[ &nbsp; ]"
    chk_transfer = "[ / ]" if pay_method == "เงินโอน" else "[ &nbsp; ]"
    chk_cheque = "[ / ]" if pay_method == "เช็ค" else "[ &nbsp; ]"
    
    text_baht = "บาทข้อความ: (ห้าพันบาทถ้วน)"

# --- ฝั่งแสดงผล (Preview) ---
with col_preview:
    st.subheader("👁️ ตัวอย่างใบเสร็จรับเงิน")
    
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4 portrait;
            margin: 10mm;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Sarabun', sans-serif;
            color: #000;
            margin: 0;
            padding: 5px;
            background-color: #fff;
        }}
        .receipt-box {{
            border: 1.5px solid #000;
            padding: 15px;
            font-size: 13px;
            line-height: 1.35;
            width: 100%;
            max-width: 780px;
            margin: 0 auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .border-table, .border-table th, .border-table td {{
            border: 1px solid #000;
        }}
        .btn-print {{
            margin-top: 15px;
            width: 100%;
            max-width: 780px;
            display: block;
            margin-left: auto;
            margin-right: auto;
            background-color: #059669;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            font-size: 16px;
            font-family: 'Sarabun', sans-serif;
        }}
        @media print {{
            .btn-print {{ display: none !important; }}
            body {{ padding: 0; background: none; }}
            .receipt-box {{ border: 1.5px solid #000; max-width: 100%; }}
        }}
    </style>
    </head>
    <body>

    <div class="receipt-box">
        <div style="text-align: right; font-size: 13px; font-weight: bold; margin-bottom: 6px;"><u>{doc_type}</u></div>

        <table style="margin-bottom: 8px;">
            <tr>
                <td style="width: 32%; vertical-align: top;">
                    <img src="{LOGO_SRC}" style="width: 100%; max-width: 220px; height: auto; display: block;">
                </td>
                <td style="width: 68%; padding-left: 15px; vertical-align: top;">
                    <div style="font-size: 16px; font-weight: bold;">บริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div>
                    <div style="font-size: 15px; font-weight: bold; margin-bottom: 4px;">A & K TRANSPORT CO.,LTD.</div>
                    <div style="font-size: 11px;">สำนักงานใหญ่ : 48/1 หมู่ที่ 3 ซอยใจเอื้อ ต.บางขะแยง อ.เมืองปทุมธานี จังหวัดปทุมธานี 12000</div>
                    <div style="font-size: 11px;">Head Office : 48/1 M00 3, Soi Jaiaoue1 , Bangkayeang, Mangpathumthani, Pathumthani 12000</div>
                    <div style="font-size: 11px;">Tel. 0-2975-3103 fax. 0-2975-3103 เลขประจำตัวผู้เสียภาษี 0135566024644</div>
                </td>
            </tr>
        </table>

        <div style="text-align: right; font-size: 12px; margin-bottom: 4px;"><b>วันที่ / Date :</b> {receipt_date}</div>

        <table class="border-table" style="text-align: center; margin-bottom: 0px;">
            <tr>
                <td style="width: 20%; padding: 4px;">รหัสลูกค้า<br><span style="font-size: 10px;">Customer Code</span></td>
                <td style="width: 40%; padding: 4px;">เงื่อนไขการชำระเงิน<br><span style="font-size: 10px;">Terms of Payment</span></td>
                <td style="width: 20%; padding: 4px;">พนักงานขนส่ง</td>
                <td style="width: 20%; padding: 4px;">เลขที่ใบเสร็จรับเงิน<br><span style="font-size: 10px;">Receipt No.</span></td>
            </tr>
            <tr style="height: 28px;">
                <td>{customer_code}</td>
                <td>{payment_term}</td>
                <td>{driver_name}</td>
                <td style="font-weight: bold;">{receipt_no}</td>
            </tr>
        </table>

        <div style="border: 1px solid #000; border-top: none; padding: 6px 10px; margin-bottom: 0px;">
            <div><b>ชื่อลูกค้า :</b> {cust_name}</div>
            <div><b>ที่อยู่ :</b> {cust_address}</div>
            <div><b>เลขประจำตัวผู้เสียภาษี :</b> {cust_taxid}</div>
        </div>

        <table class="border-table" style="border-top: none;">
            <thead>
                <tr style="text-align: center; background-color: #f9f9f9;">
                    <th style="width: 8%; padding: 5px;">ลำดับที่<br><span style="font-size: 10px; font-weight: normal;">Item</span></th>
                    <th style="width: 42%; padding: 5px;">รายการ<br><span style="font-size: 10px; font-weight: normal;">Description</span></th>
                    <th style="width: 10%; padding: 5px;">จำนวน<br><span style="font-size: 10px; font-weight: normal;">Qty</span></th>
                    <th style="width: 10%; padding: 5px;">หน่วย<br><span style="font-size: 10px; font-weight: normal;">Unit</span></th>
                    <th style="width: 15%; padding: 5px;">ราคา/หน่วย<br><span style="font-size: 10px; font-weight: normal;">Price/Unit</span></th>
                    <th style="width: 15%; padding: 5px;">จำนวนเงิน<br><span style="font-size: 10px; font-weight: normal;">Amount</span></th>
                </tr>
            </thead>
            <tbody>
                <tr style="height: 28px; text-align: center;">
                    <td>1</td>
                    <td style="padding: 2px 8px; text-align: left;">{item_desc}</td>
                    <td>{item_qty}</td>
                    <td>{item_unit}</td>
                    <td style="padding: 2px 8px; text-align: right;">{formatted_price}</td>
                    <td style="padding: 2px 8px; text-align: right;">{formatted_amount}</td>
                </tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="height: 26px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr style="font-weight: bold;">
                    <td colspan="3" style="padding: 6px 8px; text-align: left;">{text_baht}</td>
                    <td colspan="2" style="padding: 6px; text-align: center;">ยอดสุทธิ</td>
                    <td style="padding: 6px 8px; text-align: right;">{formatted_amount}</td>
                </tr>
            </tbody>
        </table>

        <div style="margin-top: 10px; font-size: 12px; line-height: 1.8;">
            <div><b>ชำระโดย :</b></div>
            <div>{chk_cash} เงินสด ................................................................................................บาท</div>
            <div>{chk_transfer} เงินโอน ................................................................................................บาท</div>
            <div>{chk_cheque} เช็ค &nbsp; ธนาคาร........................................สาขา...........................................................................................</div>
        </div>

        <table class="border-table" style="margin-top: 15px; text-align: center; font-size: 12px;">
            <tr>
                <td style="width: 33%; padding: 8px; vertical-align: top;">
                    <div>ผู้รับเงิน</div><br><br><br>
                    <div>วันที่................................................</div>
                </td>
                <td style="width: 33%; padding: 8px; vertical-align: top;">
                    <div>ผู้รับใบเสร็จ</div><br><br><br>
                    <div>วันที่................................................</div>
                </td>
                <td style="width: 34%; padding: 8px; vertical-align: top;">
                    <div>ในนามบริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div><br><br><br>
                    <div>ประทับตราบริษัท</div>
                </td>
            </tr>
        </table>
    </div>

    <button class="btn-print" onclick="window.print()">🖨️ พิมพ์ใบเสร็จรับเงิน / Save PDF</button>

    </body>
    </html>
    """
    components.html(full_html, height=920, scrolling=True)
