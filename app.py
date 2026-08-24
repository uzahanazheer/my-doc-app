import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ระบบออกใบเสร็จรับเงิน", page_icon="🧾", layout="wide")

st.markdown("## 🧾 ระบบออกใบเสร็จรับเงิน (Official Receipt)")

col_input, col_preview = st.columns([0.4, 0.6], gap="large")

with col_input:
    st.subheader("📝 กรอกข้อมูลใบเสร็จ")
    
    with st.expander("1. ข้อมูลหัวเอกสารและใบเสร็จ", expanded=True):
        doc_type = st.text_input("ประเภทเอกสาร (มุมขวาบน)", "ต้นฉบับใบเสร็จรับเงิน")
        receipt_no = st.text_input("เลขที่ใบเสร็จรับเงิน (Receipt No.)", "260012")
        receipt_date = st.text_input("วันที่ / Date", "23/7/2569")
        customer_code = st.text_input("รหัสลูกค้า (Customer Code)", "")
        payment_term = st.selectbox("เงื่อนไขการชำระเงิน (Terms of Payment)", ["Cash", "Transfer", "Cheque", "Credit"])
        driver_name = st.text_input("พนักงานขนส่ง", "")

    with st.expander("2. ข้อมูลลูกค้า", expanded=True):
        cust_name = st.text_input("ชื่อลูกค้า", "บริษัท บุรีรัมย์พนาสิทธิ์ จำกัด (สาขา 00003)")
        cust_address = st.text_area("ที่อยู่ลูกค้า", "52/647 หมู่ที่ 7 หมู่บ้าน เมืองเอก โครงการ 4 ตำบล หลักหก อำเภอ เมืองปทุมธานี จังหวัด ปทุมธานี 12000", height=70)
        cust_taxid = st.text_input("เลขประจำตัวผู้เสียภาษีลูกค้า", "0315561000656")

    with st.expander("3. รายการสินค้า / บริการ", expanded=True):
        item_desc = st.text_input("รายการ (Description)", "ค่าขนส่งสินค้า")
        item_qty = st.number_input("จำนวน (Quantity)", min_value=1, value=2)
        item_amount = st.number_input("จำนวนเงิน (Amount)", min_value=0.0, value=8400.00, step=100.0)
        text_baht = st.text_input("จำนวนเงินตัวอักษร", "แปดพันสี่ร้อยบาทถ้วน")

    with st.expander("4. การชำระเงิน", expanded=False):
        pay_type = st.radio("ชำระโดย", ["เงินสด", "เงินโอน", "เช็ค"], index=0)

chk_cash = "[ ✓ ]" if pay_type == "เงินสด" else "[ &nbsp; ]"
chk_transfer = "[ ✓ ]" if pay_type == "เงินโอน" else "[ &nbsp; ]"
chk_cheque = "[ ✓ ]" if pay_type == "เช็ค" else "[ &nbsp; ]"
formatted_amount = f"{item_amount:,.2f}"

# HTML Template สำหรับแสดงผลและสั่งพิมพ์
full_html = f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
<style>
    body {{
        font-family: 'Sarabun', sans-serif;
        color: #000;
        margin: 0;
        padding: 10px;
        background-color: #fff;
    }}
    .receipt-box {{
        border: 1px solid #000;
        padding: 15px;
        font-size: 13px;
        line-height: 1.3;
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
        .btn-print {{ display: none; }}
        body {{ padding: 0; }}
    }}
</style>
</head>
<body>

<div class="receipt-box">
    <div style="text-align: right; font-size: 13px; font-weight: bold; margin-bottom: 5px;"><u>{doc_type}</u></div>

    <table style="margin-bottom: 5px;">
        <tr>
            <td style="width: 28%; vertical-align: top;">
                <div style="border: 1px solid #000; padding: 5px; text-align: center; font-size: 11px;">
                    <div style="font-weight: bold; font-size: 13px;">A&K</div>
                    <div>บริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div>
                    <div>A & K TRANSPORT CO.,LTD.</div>
                </div>
            </td>
            <td style="width: 72%; padding-left: 15px; vertical-align: top;">
                <div style="font-size: 16px; font-weight: bold;">บริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div>
                <div style="font-size: 15px; font-weight: bold; margin-bottom: 4px;">A & K TRANSPORT CO.,LTD.</div>
                <div>สำนักงานใหญ่ : 48/1 หมู่ที่ 3 ซอยใจเอื้อ ต.บางขะแยง อ.เมืองปทุมธานี จังหวัดปทุมธานี 12000</div>
                <div>Head Office : 48/1 M00 3, Soi Jaiaoue1 , Bangkayeang, Mangpathumthani, Pathumthani 12000</div>
                <div>Tel. 0-2975-3103 fax. 0-2975-3103 เลขประจำตัวผู้เสียภาษี 0135566024644</div>
            </td>
        </tr>
    </table>

    <div style="text-align: right; font-size: 12px; margin-bottom: 2px;">วันที่ /Date &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {receipt_date}</div>

    <table class="border-table" style="text-align: center; margin-bottom: 0px;">
        <tr>
            <td style="width: 20%; padding: 3px;">รหัสลูกค้า<br><span style="font-size: 11px;">Customer Code</span></td>
            <td style="width: 40%; padding: 3px;">เงื่อนไขการชำระเงิน<br><span style="font-size: 11px;">Terms of Payment</span></td>
            <td style="width: 20%; padding: 3px;">พนักงานขนส่ง</td>
            <td style="width: 20%; padding: 3px;">เลขที่ใบเสร็จรับเงิน<br><span style="font-size: 11px;">Receipt No.</span></td>
        </tr>
        <tr style="height: 25px;">
            <td>{customer_code}</td>
            <td>{payment_term}</td>
            <td>{driver_name}</td>
            <td style="font-weight: bold;">{receipt_no}</td>
        </tr>
    </table>

    <div style="border: 1px solid #000; border-top: none; padding: 5px 8px; margin-bottom: 0px;">
        <div><b>ชื่อลูกค้า :</b> {cust_name}</div>
        <div><b>ที่อยู่ :</b> {cust_address}</div>
        <div><b>เลขประจำตัวผู้เสียภาษี :</b> {cust_taxid}</div>
    </div>

    <table class="border-table" style="border-top: none;">
        <thead>
            <tr style="text-align: center;">
                <th style="width: 12%; padding: 4px;">ลำดับที่<br><span style="font-size: 11px; font-weight: normal;">Item</span></th>
                <th style="width: 53%; padding: 4px;">รายการ<br><span style="font-size: 11px; font-weight: normal;">Description</span></th>
                <th style="width: 15%; padding: 4px;">จำนวน<br><span style="font-size: 11px; font-weight: normal;">Quantity</span></th>
                <th style="width: 20%; padding: 4px;">จำนวนเงิน<br><span style="font-size: 11px; font-weight: normal;">Amount</span></th>
            </tr>
        </thead>
        <tbody>
            <tr style="height: 24px; text-align: center;">
                <td>1</td>
                <td style="padding: 2px 8px; text-align: left;">{item_desc}</td>
                <td>{item_qty}</td>
                <td style="padding: 2px 8px; text-align: right;">{formatted_amount}</td>
            </tr>
            <tr style="height: 22px;"><td></td><td></td><td></td><td></td></tr>
            <tr style="height: 22px;"><td></td><td></td><td></td><td></td></tr>
            <tr style="height: 22px;"><td></td><td></td><td></td><td></td></tr>
            <tr style="height: 22px;"><td></td><td></td><td></td><td></td></tr>
            <tr style="height: 22px;"><td></td><td></td><td></td><td></td></tr>
            <tr style="font-weight: bold;">
                <td colspan="2" style="padding: 4px 8px; text-align: left;">{text_baht}</td>
                <td style="padding: 4px; text-align: center;">ยอดสุทธิ</td>
                <td style="padding: 4px 8px; text-align: right;">{formatted_amount}</td>
            </tr>
        </tbody>
    </table>

    <div style="margin-top: 8px; font-size: 12px; line-height: 1.8;">
        <div><b>ชำระโดย :</b></div>
        <div>{chk_cash} เงินสด ...................................................................บาท</div>
        <div>{chk_transfer} เงินโอน ...................................................................บาท</div>
        <div>{chk_cheque} เช็ค &nbsp; ธนาคาร........................................สาขา...........................................................................................</div>
    </div>

    <table class="border-table" style="margin-top: 15px; text-align: center; font-size: 12px;">
        <tr>
            <td style="width: 33%; padding: 6px; vertical-align: top;">
                <div>ผู้รับเงิน</div><br><br>
                <div>วันที่................................................</div>
            </td>
            <td style="width: 33%; padding: 6px; vertical-align: top;">
                <div>ผู้รับใบเสร็จ</div><br><br>
                <div>วันที่................................................</div>
            </td>
            <td style="width: 34%; padding: 6px; vertical-align: top;">
                <div>ในนามบริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div><br><br>
                <div>ประทับตราบริษัท</div>
            </td>
        </tr>
    </table>
</div>

<button class="btn-print" onclick="window.print()">🖨️ พิมพ์ใบเสร็จรับเงิน / สั่งปริ้นท์</button>

</body>
</html>
"""

with col_preview:
    st.subheader("👁️ ตัวอย่างใบเสร็จรับเงิน (Receipt Preview)")
    components.html(full_html, height=850, scrolling=True)
