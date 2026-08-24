import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="ระบบออกใบเสร็จรับเงิน", page_icon="🧾", layout="wide")

def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return ""

LOGO_BASE64 = get_image_base64("logo.png")
if not LOGO_BASE64:
    LOGO_SRC = "https://via.placeholder.com/220x80.png?text=A%26K+Transport+Logo"
else:
    LOGO_SRC = LOGO_BASE64

# --- ฐานข้อมูลลูกค้า ---
CUSTOMER_DB = {
    "-- กรอกข้อมูลเอง / เลือกบริษัท --": {
        "code": "",
        "name": "",
        "address": "",
        "taxid": ""
    },
    "CUST-001 | บริษัท ตัวอย่าง จำกัด": {
        "code": "CUST-001",
        "name": "บริษัท ตัวอย่าง จำกัด",
        "address": "123/45 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพฯ 10110",
        "taxid": "0105551234567"
    },
    "CUST-002 | บริษัท โลจิสติกส์ ไทย จำกัด": {
        "code": "CUST-002",
        "name": "บริษัท โลจิสติกส์ ไทย จำกัด",
        "address": "88/9 หมู่ 2 ต.บางกรวด อ.เมือง จ.ปทุมธานี 12000",
        "taxid": "0135599887766"
    }
}

# Callback ฟังก์ชันสำหรับอัปเดตข้อมูลอัตโนมัติเมื่อเลือกฐานข้อมูล
def update_customer_info():
    selected = st.session_state.selected_cust_key
    if selected in CUSTOMER_DB and selected != "-- กรอกข้อมูลเอง / เลือกบริษัท --":
        st.session_state.customer_code = CUSTOMER_DB[selected]["code"]
        st.session_state.cust_name = CUSTOMER_DB[selected]["name"]
        st.session_state.cust_address = CUSTOMER_DB[selected]["address"]
        st.session_state.cust_taxid = CUSTOMER_DB[selected]["taxid"]

# กำหนด Default Session State
if "customer_code" not in st.session_state:
    st.session_state.customer_code = "CUST-001"
if "cust_name" not in st.session_state:
    st.session_state.cust_name = "บริษัท ตัวอย่าง จำกัด"
if "cust_address" not in st.session_state:
    st.session_state.cust_address = "123/45 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพฯ 10110"
if "cust_taxid" not in st.session_state:
    st.session_state.cust_taxid = "0105551234567"

col_form, col_preview = st.columns([1, 1.2])

with col_form:
    st.header("📝 กรอกข้อมูลใบเสร็จ")
    
    doc_type = st.selectbox("ชนิดเอกสาร", ["ต้นฉบับใบเสร็จรับเงิน", "สำเนาใบเสร็จรับเงิน", "ใบเสร็จรับเงิน/ใบกำกับภาษี"])
    receipt_date = st.text_input("วันที่", "12/03/2026")
    receipt_no = st.text_input("เลขที่ใบเสร็จ", "REC2026/03-001")
    
    st.subheader("👤 ฐานข้อมูลลูกค้า")
    st.selectbox(
        "📂 เลือกรายชื่อลูกค้าจากฐานข้อมูล",
        options=list(CUSTOMER_DB.keys()),
        key="selected_cust_key",
        on_change=update_customer_info
    )
    
    customer_code = st.text_input("รหัสลูกค้า", key="customer_code")
    cust_name = st.text_input("ชื่อลูกค้า", key="cust_name")
    cust_address = st.text_area("ที่อยู่ลูกค้า", key="cust_address")
    cust_taxid = st.text_input("เลขผู้เสียภาษี", key="cust_taxid")
    
    st.subheader("🚛 ข้อมูลการขนส่ง / รายการ")
    payment_term = st.text_input("เงื่อนไขการชำระเงิน", "เงินสด / โอน")
    driver_name = st.text_input("พนักงานขนส่ง", "นายสมชาย ใจดี")
    
    item_desc = st.text_input("รายการสินค้า/บริการ", "ค่าบริการขนส่งสินค้าตามเที่ยววิ่ง")
    item_qty = st.number_input("จำนวน", min_value=1, value=1)
    item_unit = st.text_input("หน่วย", "เที่ยว")
    item_price = st.number_input("ราคาต่อหน่วย", min_value=0.0, value=5000.0, step=100.0)
    
    st.subheader("💳 วิธีการชำระเงิน")
    pay_method = st.radio("เลือกวิธีชำระเงิน", ["เงินสด", "เงินโอน", "เช็ค"])
    
    total_amount = item_qty * item_price
    formatted_price = f"{item_price:,.2f}"
    formatted_amount = f"{total_amount:,.2f}"
    
    chk_cash = "[ / ]" if pay_method == "เงินสด" else "[ &nbsp; ]"
    chk_transfer = "[ / ]" if pay_method == "เงินโอน" else "[ &nbsp; ]"
    chk_cheque = "[ / ]" if pay_method == "เช็ค" else "[ &nbsp; ]"
    
    text_baht = "บาทข้อความ: (ห้าพันบาทถ้วน)"

with col_preview:
    st.subheader("👁️ ตัวอย่างใบเสร็จรับเงิน (A4 Margin Adjusted)")
    
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4 portrait;
            margin: 15mm; /* เว้นขอบกระดาษจริงเมื่อพิมพ์ */
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Sarabun', sans-serif;
            color: #000;
            margin: 0;
            padding: 20px 0;
            background-color: #f3f4f6;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        /* กำหนดระยะขอบ Padding ภายในกล่องให้เว้นเข้ามาด้านในสวยงาม */
        .receipt-box {{
            border: 1.5px solid #000;
            padding: 40px 45px; /* เพิ่มระยะเว้นขอบเข้ามาอีก */
            font-size: 13px;
            line-height: 1.4;
            width: 794px;
            height: 1123px;
            background-color: #fff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .border-table, .border-table th, .border-table td {{
            border: 1px solid #000;
        }}
        .btn-print {{
            margin-top: 20px;
            width: 794px;
            background-color: #059669;
            color: white;
            border: none;
            padding: 14px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            font-size: 16px;
            font-family: 'Sarabun', sans-serif;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }}
        @media print {{
            body {{ padding: 0; background: none; }}
            .btn-print {{ display: none !important; }}
            .receipt-box {{
                border: 1.5px solid #000;
                width: 100%;
                height: 100vh;
                padding: 30px 35px;
                box-shadow: none;
                page-break-after: always;
            }}
        }}
    </style>
    </head>
    <body>

    <div class="receipt-box">
        <div>
            <div style="text-align: right; font-size: 14px; font-weight: bold; margin-bottom: 8px;"><u>{doc_type}</u></div>

            <!-- Header Layout -->
            <table style="margin-bottom: 12px;">
                <tr>
                    <td style="width: 28%; vertical-align: middle; padding-right: 12px;">
                        <img src="{LOGO_SRC}" style="width: 100%; max-height: 75px; object-fit: contain; display: block;">
                    </td>
                    <td style="width: 72%; vertical-align: middle; padding-left: 10px;">
                        <div style="font-size: 21px; font-weight: bold; line-height: 1.2; margin-bottom: 2px;">บริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div>
                        <div style="font-size: 17px; font-weight: bold; line-height: 1.2;">A & K TRANSPORT CO.,LTD.</div>
                    </td>
                </tr>
            </table>

            <!-- ที่อยู่บริษัท -->
            <div style="font-size: 11.5px; line-height: 1.5; margin-bottom: 12px;">
                <div>สำนักงานใหญ่ : 48/1 หมู่ที่ 3 ซอยใจเอื้อ ต.บางขะแยง อ.เมืองปทุมธานี จังหวัดปทุมธานี 12000</div>
                <div>Head Office : 48/1 M00 3, Soi Jaiaoue1 , Bangkayeang, Mangpathumthani, Pathumthani 12000</div>
                <div>Tel. 0-2975-3103 fax. 0-2975-3103 เลขประจำตัวผู้เสียภาษี 0135566024644</div>
            </div>

            <div style="text-align: right; font-size: 13px; margin-bottom: 6px;"><b>วันที่ / Date :</b> {receipt_date}</div>

            <table class="border-table" style="text-align: center; margin-bottom: 0px;">
                <tr>
                    <td style="width: 20%; padding: 5px;">รหัสลูกค้า<br><span style="font-size: 10px;">Customer Code</span></td>
                    <td style="width: 40%; padding: 5px;">เงื่อนไขการชำระเงิน<br><span style="font-size: 10px;">Terms of Payment</span></td>
                    <td style="width: 20%; padding: 5px;">พนักงานขนส่ง</td>
                    <td style="width: 20%; padding: 5px;">เลขที่ใบเสร็จรับเงิน<br><span style="font-size: 10px;">Receipt No.</span></td>
                </tr>
                <tr style="height: 30px;">
                    <td>{customer_code}</td>
                    <td>{payment_term}</td>
                    <td>{driver_name}</td>
                    <td style="font-weight: bold;">{receipt_no}</td>
                </tr>
            </table>

            <div style="border: 1px solid #000; border-top: none; padding: 8px 12px; margin-bottom: 0px; font-size: 12.5px; line-height: 1.6;">
                <div><b>ชื่อลูกค้า :</b> {cust_name}</div>
                <div><b>ที่อยู่ :</b> {cust_address}</div>
                <div><b>เลขประจำตัวผู้เสียภาษี :</b> {cust_taxid}</div>
            </div>

            <table class="border-table" style="border-top: none;">
                <thead>
                    <tr style="text-align: center; background-color: #fdfdfd;">
                        <th style="width: 8%; padding: 6px;">ลำดับที่<br><span style="font-size: 10px; font-weight: normal;">Item</span></th>
                        <th style="width: 42%; padding: 6px;">รายการ<br><span style="font-size: 10px; font-weight: normal;">Description</span></th>
                        <th style="width: 10%; padding: 6px;">จำนวน<br><span style="font-size: 10px; font-weight: normal;">Qty</span></th>
                        <th style="width: 10%; padding: 6px;">หน่วย<br><span style="font-size: 10px; font-weight: normal;">Unit</span></th>
                        <th style="width: 15%; padding: 6px;">ราคา/หน่วย<br><span style="font-size: 10px; font-weight: normal;">Price/Unit</span></th>
                        <th style="width: 15%; padding: 6px;">จำนวนเงิน<br><span style="font-size: 10px; font-weight: normal;">Amount</span></th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="height: 34px; text-align: center;">
                        <td>1</td>
                        <td style="padding: 4px 10px; text-align: left;">{item_desc}</td>
                        <td>{item_qty}</td>
                        <td>{item_unit}</td>
                        <td style="padding: 4px 10px; text-align: right;">{formatted_price}</td>
                        <td style="padding: 4px 10px; text-align: right;">{formatted_amount}</td>
                    </tr>
                    <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                    <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                    <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                    <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                    <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                    <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                    <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                    <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                    <tr style="font-weight: bold;">
                        <td colspan="3" style="padding: 8px 10px; text-align: left;">{text_baht}</td>
                        <td colspan="2" style="padding: 8px; text-align: center;">ยอดสุทธิ</td>
                        <td style="padding: 8px 10px; text-align: right;">{formatted_amount}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div>
            <div style="margin-top: 15px; font-size: 12.5px; line-height: 2.0;">
                <div><b>ชำระโดย :</b></div>
                <div>{chk_cash} เงินสด ................................................................................................................บาท</div>
                <div>{chk_transfer} เงินโอน ................................................................................................................บาท</div>
                <div>{chk_cheque} เช็ค &nbsp; ธนาคาร........................................สาขา...........................................................................................</div>
            </div>

            <table class="border-table" style="margin-top: 15px; text-align: center; font-size: 12px;">
                <tr>
                    <td style="width: 33%; padding: 10px 6px; vertical-align: top;">
                        <div>ผู้รับเงิน</div><br><br><br>
                        <div>วันที่................................................</div>
                    </td>
                    <td style="width: 33%; padding: 10px 6px; vertical-align: top;">
                        <div>ผู้รับใบเสร็จ</div><br><br><br>
                        <div>วันที่................................................</div>
                    </td>
                    <td style="width: 34%; padding: 10px 6px; vertical-align: top;">
                        <div>ในนามบริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div><br><br><br>
                        <div>ประทับตราบริษัท</div>
                    </td>
                </tr>
            </table>
        </div>
    </div>

    <button class="btn-print" onclick="window.print()">🖨️ พิมพ์ใบเสร็จรับเงิน / Save PDF (A4)</button>

    </body>
    </html>
    """
    components.html(full_html, height=1200, scrolling=True)
