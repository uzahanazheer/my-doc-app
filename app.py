import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
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
LOGO_SRC = LOGO_BASE64 if LOGO_BASE64 else "https://via.placeholder.com/300x120.png?text=A%26K+Transport+Logo"

# --- ฐานข้อมูลลูกค้า ---
CUSTOMER_DB = {
    "-- กรอกข้อมูลเอง / เลือกบริษัท --": {"code": "", "name": "", "address": "", "taxid": ""},
    "CUST-001 | บริษัท ตัวอย่าง จำกัด": {
        "code": "CUST-001", "name": "บริษัท ตัวอย่าง จำกัด",
        "address": "123/45 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพฯ 10110", "taxid": "0105551234567"
    },
    "CUST-002 | บริษัท โลจิสติกส์ ไทย จำกัด": {
        "code": "CUST-002", "name": "บริษัท โลจิสติกส์ ไทย จำกัด",
        "address": "88/9 หมู่ 2 ต.บางกรวด อ.เมือง จ.ปทุมธานี 12000", "taxid": "0135599887766"
    }
}

# --- Session State เก็บประวัติใบเสร็จ ---
if "receipt_history" not in st.session_state:
    st.session_state.receipt_history = [
        {"เลขที่ใบเสร็จ": "REC2026/03-001", "วันที่": "12/03/2026", "ชื่อลูกค้า": "บริษัท ตัวอย่าง จำกัด", "รายการ": "ค่าบริการขนส่งสินค้าตามเที่ยววิ่ง", "จำนวนเงิน": 5000.0, "วิธีชำระ": "เงินโอน"},
        {"เลขที่ใบเสร็จ": "REC2026/03-002", "วันที่": "15/03/2026", "ชื่อลูกค้า": "บริษัท โลจิสติกส์ ไทย จำกัด", "รายการ": "ค่าขนส่งสินค้ารายเดือน", "จำนวนเงิน": 12500.0, "วิธีชำระ": "เงินสด"}
    ]

def update_customer_info():
    selected = st.session_state.selected_cust_key
    if selected in CUSTOMER_DB and selected != "-- กรอกข้อมูลเอง / เลือกบริษัท --":
        st.session_state.customer_code = CUSTOMER_DB[selected]["code"]
        st.session_state.cust_name = CUSTOMER_DB[selected]["name"]
        st.session_state.cust_address = CUSTOMER_DB[selected]["address"]
        st.session_state.cust_taxid = CUSTOMER_DB[selected]["taxid"]

if "customer_code" not in st.session_state: st.session_state.customer_code = "CUST-001"
if "cust_name" not in st.session_state: st.session_state.cust_name = "บริษัท ตัวอย่าง จำกัด"
if "cust_address" not in st.session_state: st.session_state.cust_address = "123/45 ถนนสุขุมวิท แขวงคลองเตย เขตคลองเตย กรุงเทพฯ 10110"
if "cust_taxid" not in st.session_state: st.session_state.cust_taxid = "0105551234567"

# --- แบ่ง Tab การใช้งาน ---
tab_form, tab_summary = st.tabs(["🧾 ออกใบเสร็จรับเงิน", "📊 สรุปข้อมูลรวม"])

with tab_form:
    col_form, col_preview = st.columns([1, 1.1])

    with col_form:
        st.header("📝 กรอกข้อมูลใบเสร็จ")
        
        doc_type = st.selectbox("ชนิดเอกสาร", ["ต้นฉบับใบเสร็จรับเงิน", "สำเนาใบเสร็จรับเงิน", "ใบเสร็จรับเงิน/ใบกำกับภาษี"])
        receipt_date = st.text_input("วันที่", "12/03/2026")
        receipt_no = st.text_input("เลขที่ใบเสร็จ", "REC2026/03-003")
        
        st.subheader("👤 ฐานข้อมูลลูกค้า")
        st.selectbox("📂 เลือกรายชื่อลูกค้าจากฐานข้อมูล", options=list(CUSTOMER_DB.keys()), key="selected_cust_key", on_change=update_customer_info)
        
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

        if st.button("💾 บันทึกข้อมูลลงฐานข้อมูลสรุป", type="primary"):
            st.session_state.receipt_history.append({
                "เลขที่ใบเสร็จ": receipt_no, "วันที่": receipt_date, "ชื่อลูกค้า": cust_name,
                "รายการ": item_desc, "จำนวนเงิน": total_amount, "วิธีชำระ": pay_method
            })
            st.success("บันทึกข้อมูลเรียบร้อยแล้ว!")

    with col_preview:with col_preview:
    st.subheader("👁️ ตัวอย่างก่อนพิมพ์ (Fit A4 View)")
    
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4 portrait;
            margin: 0;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Sarabun', sans-serif;
            color: #000;
            margin: 0;
            padding: 0;
            background-color: transparent;
        }}
        .preview-wrapper {{
            transform: scale(0.68);
            transform-origin: top left;
            width: 147%;
            height: 1100px;
        }}
        .receipt-box {{
            border: 1.5px solid #000;
            padding: 28px 32px;
            font-size: 12.5px;
            line-height: 1.35;
            width: 794px;
            height: 1060px;
            background-color: #fff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin: 0 auto;
        }}
        table {{ width: 100%; border-collapse: collapse; }}
        .border-table, .border-table th, .border-table td {{ border: 1px solid #000; }}
        .btn-print {{
            margin-top: 15px;
            width: 794px;
            background-color: #059669;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            font-size: 18px;
            font-family: 'Sarabun', sans-serif;
        }}
        @media print {{
            .preview-wrapper {{ transform: none; width: 100%; height: auto; }}
            body {{ background: none; }}
            .btn-print {{ display: none !important; }}
            .receipt-box {{
                border: 1.5px solid #000;
                width: 100%;
                height: 98vh;
                padding: 25px 30px;
                box-shadow: none;
                page-break-after: avoid;
                page-break-inside: avoid;
            }}
        }}
    </style>
    </head>
    <body>

    <div class="preview-wrapper">
        <div class="receipt-box">
            <div>
                <div style="text-align: right; font-size: 14px; font-weight: bold; margin-bottom: 4px;"><u>{doc_type}</u></div>

                <table style="margin-bottom: 8px;">
                    <tr>
                        <td style="width: 35%; vertical-align: middle; padding-right: 10px;">
                            <img src="{LOGO_SRC}" style="width: 100%; max-height: 110px; object-fit: contain; display: block;">
                        </td>
                        <td style="width: 65%; vertical-align: middle; padding-left: 5px;">
                            <div style="font-size: 22px; font-weight: bold; line-height: 1.2;">บริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div>
                            <div style="font-size: 17px; font-weight: bold; line-height: 1.2;">A & K TRANSPORT CO.,LTD.</div>
                        </td>
                    </tr>
                </table>

                <div style="font-size: 11px; line-height: 1.4; margin-bottom: 8px;">
                    <div>สำนักงานใหญ่ : 48/1 หมู่ที่ 3 ซอยใจเอื้อ ต.บางขะแยง อ.เมืองปทุมธานี จังหวัดปทุมธานี 12000</div>
                    <div>Head Office : 48/1 M00 3, Soi Jaiaoue1 , Bangkayeang, Mangpathumthani, Pathumthani 12000</div>
                    <div>Tel. 0-2975-3103 fax. 0-2975-3103 เลขประจำตัวผู้เสียภาษี 0135566024644</div>
                </div>

                <div style="text-align: right; font-size: 12.5px; margin-bottom: 4px;"><b>วันที่ / Date :</b> {receipt_date}</div>

                <table class="border-table" style="text-align: center;">
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

                <div style="border: 1px solid #000; border-top: none; padding: 6px 10px; font-size: 12px; line-height: 1.5;">
                    <div><b>ชื่อลูกค้า :</b> {cust_name}</div>
                    <div><b>ที่อยู่ :</b> {cust_address}</div>
                    <div><b>เลขประจำตัวผู้เสียภาษี :</b> {cust_taxid}</div>
                </div>

                <table class="border-table" style="border-top: none;">
                    <thead>
                        <tr style="text-align: center; background-color: #fdfdfd;">
                            <th style="width: 8%; padding: 5px;">ลำดับที่</th>
                            <th style="width: 42%; padding: 5px;">รายการ</th>
                            <th style="width: 10%; padding: 5px;">จำนวน</th>
                            <th style="width: 10%; padding: 5px;">หน่วย</th>
                            <th style="width: 15%; padding: 5px;">ราคา/หน่วย</th>
                            <th style="width: 15%; padding: 5px;">จำนวนเงิน</th>
                        </tr>
                    </thead>
                    <!-- แก้ไขเพิ่มจำนวนแถวในส่วนนี้แล้ว -->
                    <tbody>
                        <tr style="height: 30px; text-align: center;">
                            <td>1</td>
                            <td style="padding: 2px 8px; text-align: left;">{item_desc}</td>
                            <td>{item_qty}</td>
                            <td>{item_unit}</td>
                            <td style="padding: 2px 8px; text-align: right;">{formatted_price}</td>
                            <td style="padding: 2px 8px; text-align: right;">{formatted_amount}</td>
                        </tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="height: 30px;"><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr style="font-weight: bold;">
                            <td colspan="3" style="padding: 6px 8px; text-align: left;">{text_baht}</td>
                            <td colspan="2" style="padding: 6px; text-align: center;">ยอดสุทธิ</td>
                            <td style="padding: 6px 8px; text-align: right;">{formatted_amount}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div>
                <div style="margin-top: 10px; font-size: 12px; line-height: 1.8;">
                    <div><b>ชำระโดย :</b></div>
                    <div>{chk_cash} เงินสด ................................................................................................................บาท</div>
                    <div>{chk_transfer} เงินโอน ................................................................................................................บาท</div>
                    <div>{chk_cheque} เช็ค &nbsp; ธนาคาร........................................สาขา...........................................................................................</div>
                </div>

                <table class="border-table" style="margin-top: 12px; text-align: center; font-size: 11.5px;">
                    <tr>
                        <td style="width: 33%; padding: 8px 4px; vertical-align: top;">
                            <div>ผู้รับเงิน</div><br><br>
                            <div>วันที่................................................</div>
                        </td>
                        <td style="width: 33%; padding: 8px 4px; vertical-align: top;">
                            <div>ผู้รับใบเสร็จ</div><br><br>
                            <div>วันที่................................................</div>
                        </td>
                        <td style="width: 34%; padding: 8px 4px; vertical-align: top;">
                            <div>ในนามบริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div><br><br>
                            <div>ประทับตราบริษัท</div>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <button class="btn-print" onclick="window.print()">🖨️ พิมพ์ใบเสร็จรับเงิน / Save PDF (A4)</button>
    </div>

    </body>
    </html>
    """
    components.html(full_html, height=780, scrolling=False)
        st.subheader("👁️ ตัวอย่างก่อนพิมพ์ (Fit A4 View)")
        
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
        <style>
            @page {{
                size: A4 portrait;
                margin: 0;
            }}
            * {{ box-sizing: border-box; }}
            body {{
                font-family: 'Sarabun', sans-serif;
                color: #000;
                margin: 0;
                padding: 0;
                background-color: transparent;
            }}
            /* สเกลภาพพรีวิวลงเพื่อให้เห็นเต็มหน้าโดยไม่ต้องเลื่อน */
            .preview-wrapper {{
                transform: scale(0.68);
                transform-origin: top left;
                width: 147%;
                height: 1100px;
            }}
            .receipt-box {{
                border: 1.5px solid #000;
                padding: 28px 32px;
                font-size: 12.5px;
                line-height: 1.35;
                width: 794px;
                height: 1060px; /* คุมความสูงพอดี 1 หน้า A4 ไม่ให้ล้นแผ่นที่ 2 */
                background-color: #fff;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                margin: 0 auto;
            }}
            table {{ width: 100%; border-collapse: collapse; }}
            .border-table, .border-table th, .border-table td {{ border: 1px solid #000; }}
            .btn-print {{
                margin-top: 15px;
                width: 794px;
                background-color: #059669;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                cursor: pointer;
                font-size: 18px;
                font-family: 'Sarabun', sans-serif;
            }}
            @media print {{
                .preview-wrapper {{ transform: none; width: 100%; height: auto; }}
                body {{ background: none; }}
                .btn-print {{ display: none !important; }}
                .receipt-box {{
                    border: 1.5px solid #000;
                    width: 100%;
                    height: 98vh;
                    padding: 25px 30px;
                    box-shadow: none;
                    page-break-after: avoid;
                    page-break-inside: avoid;
                }}
            }}
        </style>
        </head>
        <body>

        <div class="preview-wrapper">
            <div class="receipt-box">
                <div>
                    <div style="text-align: right; font-size: 14px; font-weight: bold; margin-bottom: 4px;"><u>{doc_type}</u></div>

                    <!-- ขยายโลโก้ให้ใหญ่ขึ้น -->
                    <table style="margin-bottom: 8px;">
                        <tr>
                            <td style="width: 35%; vertical-align: middle; padding-right: 10px;">
                                <img src="{LOGO_SRC}" style="width: 100%; max-height: 110px; object-fit: contain; display: block;">
                            </td>
                            <td style="width: 65%; vertical-align: middle; padding-left: 5px;">
                                <div style="font-size: 22px; font-weight: bold; line-height: 1.2;">บริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div>
                                <div style="font-size: 17px; font-weight: bold; line-height: 1.2;">A & K TRANSPORT CO.,LTD.</div>
                            </td>
                        </tr>
                    </table>

                    <div style="font-size: 11px; line-height: 1.4; margin-bottom: 8px;">
                        <div>สำนักงานใหญ่ : 48/1 หมู่ที่ 3 ซอยใจเอื้อ ต.บางขะแยง อ.เมืองปทุมธานี จังหวัดปทุมธานี 12000</div>
                        <div>Head Office : 48/1 M00 3, Soi Jaiaoue1 , Bangkayeang, Mangpathumthani, Pathumthani 12000</div>
                        <div>Tel. 0-2975-3103 fax. 0-2975-3103 เลขประจำตัวผู้เสียภาษี 0135566024644</div>
                    </div>

                    <div style="text-align: right; font-size: 12.5px; margin-bottom: 4px;"><b>วันที่ / Date :</b> {receipt_date}</div>

                    <table class="border-table" style="text-align: center;">
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

                    <div style="border: 1px solid #000; border-top: none; padding: 6px 10px; font-size: 12px; line-height: 1.5;">
                        <div><b>ชื่อลูกค้า :</b> {cust_name}</div>
                        <div><b>ที่อยู่ :</b> {cust_address}</div>
                        <div><b>เลขประจำตัวผู้เสียภาษี :</b> {cust_taxid}</div>
                    </div>

                    <table class="border-table" style="border-top: none;">
                        <thead>
                            <tr style="text-align: center; background-color: #fdfdfd;">
                                <th style="width: 8%; padding: 5px;">ลำดับที่</th>
                                <th style="width: 42%; padding: 5px;">รายการ</th>
                                <th style="width: 10%; padding: 5px;">จำนวน</th>
                                <th style="width: 10%; padding: 5px;">หน่วย</th>
                                <th style="width: 15%; padding: 5px;">ราคา/หน่วย</th>
                                <th style="width: 15%; padding: 5px;">จำนวนเงิน</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="height: 30px; text-align: center;">
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
                </div>

                <div>
                    <div style="margin-top: 10px; font-size: 12px; line-height: 1.8;">
                        <div><b>ชำระโดย :</b></div>
                        <div>{chk_cash} เงินสด ................................................................................................................บาท</div>
                        <div>{chk_transfer} เงินโอน ................................................................................................................บาท</div>
                        <div>{chk_cheque} เช็ค &nbsp; ธนาคาร........................................สาขา...........................................................................................</div>
                    </div>

                    <table class="border-table" style="margin-top: 12px; text-align: center; font-size: 11.5px;">
                        <tr>
                            <td style="width: 33%; padding: 8px 4px; vertical-align: top;">
                                <div>ผู้รับเงิน</div><br><br>
                                <div>วันที่................................................</div>
                            </td>
                            <td style="width: 33%; padding: 8px 4px; vertical-align: top;">
                                <div>ผู้รับใบเสร็จ</div><br><br>
                                <div>วันที่................................................</div>
                            </td>
                            <td style="width: 34%; padding: 8px 4px; vertical-align: top;">
                                <div>ในนามบริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div><br><br>
                                <div>ประทับตราบริษัท</div>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
            <button class="btn-print" onclick="window.print()">🖨️ พิมพ์ใบเสร็จรับเงิน / Save PDF (A4)</button>
        </div>

        </body>
        </html>
        """
        components.html(full_html, height=780, scrolling=False)

# --- Tab สรุปข้อมูลรวม ---
with tab_summary:
    st.header("📊 สรุปข้อมูลรวมใบเสร็จรับเงิน")
    
    df_history = pd.DataFrame(st.session_state.receipt_history)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("จำนวนใบเสร็จทั้งหมด", f"{len(df_history)} ฉบับ")
    with col2:
        total_sum = df_history["จำนวนเงิน"].sum() if not df_history.empty else 0
        st.metric("ยอดรวมทั้งสิ้น", f"฿{total_sum:,.2f}")
    
    st.subheader("📋 ประวัติการออกใบเสร็จ")
    st.dataframe(df_history, use_container_width=True)
