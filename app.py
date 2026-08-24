import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="ระบบออกใบเสร็จรับเงิน", page_icon="🧾", layout="wide")

# CSS สำหรับปรับแต่งหน้าตาแอป
st.markdown("""
<style>
    .main-header { font-size: 26px; font-weight: bold; color: #1E293B; margin-bottom: 5px; }
    .sub-header { font-size: 14px; color: #64748B; margin-bottom: 20px; }
    .stButton>button { background-color: #059669; color: white; border-radius: 6px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🧾 ระบบออกใบเสร็จรับเงิน (Official Receipt)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">กรอกข้อมูล ออกใบเสร็จรับเงินตามแบบฟอร์มมาตรฐาน และสั่งพิมพ์ได้ทันที</p>', unsafe_allow_html=True)

# แบ่งหน้าจอเป็น 2 ส่วน (กรอกข้อมูล 45% / Preview ใบเสร็จ 55%)
col_input, col_preview = st.columns([0.45, 0.55], gap="large")

with col_input:
    st.subheader("📝 กรอกข้อมูลใบเสร็จรับเงิน")
    
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
        pay_cash_amount = st.text_input("จำนวนเงินสด/โอน (บาท)", "8,400.00")
        bank_name = st.text_input("ธนาคาร (กรณีเช็ค/โอน)", "")
        bank_branch = st.text_input("สาขา", "")

with col_preview:
    st.subheader("👁️ ตัวอย่างใบเสร็จรับเงิน (Receipt Preview)")
    
    # HTML & CSS ถอดแบบฟอร์มเอกสารจริง 100%
    receipt_html = f"""
    <div style="background-color: white; border: 1px solid #000; padding: 20px; font-family: 'Sarabun', 'TH Sarabun New', sans-serif; color: #000; font-size: 13px; line-height: 1.3; width: 100%; box-sizing: border-box;">
        
        <!-- Header Top Right -->
        <div style="text-align: right; font-size: 13px; font-weight: bold; margin-bottom: 5px;"><u>{doc_type}</u></div>

        <!-- Header Company Info -->
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 5px;">
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

        <!-- Date & Doc Info Table -->
        <div style="text-align: right; font-size: 12px; margin-bottom: 2px;">วันที่ /Date &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {receipt_date}</div>
        
        <table style="width: 100%; border-collapse: collapse; border: 1px solid #000; text-align: center; margin-bottom: 0px;">
            <tr style="border-bottom: 1px solid #000;">
                <td style="width: 20%; border-right: 1px solid #000; padding: 3px;">รหัสลูกค้า<br><span style="font-size: 11px;">Customer Code</span></td>
                <td style="width: 40%; border-right: 1px solid #000; padding: 3px;">เงื่อนไขการชำระเงิน<br><span style="font-size: 11px;">Terms of Payment</span></td>
                <td style="width: 20%; border-right: 1px solid #000; padding: 3px;">พนักงานขนส่ง</td>
                <td style="width: 20%; padding: 3px;">เลขที่ใบเสร็จรับเงิน<br><span style="font-size: 11px;">Receipt No.</span></td>
            </tr>
            <tr style="height: 25px;">
                <td style="border-right: 1px solid #000; padding: 2px;">{customer_code}</td>
                <td style="border-right: 1px solid #000; padding: 2px;">{payment_term}</td>
                <td style="border-right: 1px solid #000; padding: 2px;">{driver_name}</td>
                <td style="padding: 2px; font-weight: bold;">{receipt_no}</td>
            </tr>
        </table>

        <!-- Customer Info Box -->
        <div style="border: 1px solid #000; border-top: none; padding: 5px 8px; margin-bottom: 0px;">
            <div><b>ชื่อลูกค้า :</b> {cust_name}</div>
            <div><b>ที่อยู่ :</b> {cust_address}</div>
            <div><b>เลขประจำตัวผู้เสียภาษี :</b> {cust_taxid}</div>
        </div>

        <!-- Items Table -->
        <table style="width: 100%; border-collapse: collapse; border: 1px solid #000; border-top: none;">
            <thead>
                <tr style="border-bottom: 1px solid #000; text-align: center;">
                    <th style="width: 12%; border-right: 1px solid #000; padding: 4px;">ลำดับที่<br><span style="font-size: 11px; font-weight: normal;">Item</span></th>
                    <th style="width: 53%; border-right: 1px solid #000; padding: 4px;">รายการ<br><span style="font-size: 11px; font-weight: normal;">Description</span></th>
                    <th style="width: 15%; border-right: 1px solid #000; padding: 4px;">จำนวน<br><span style="font-size: 11px; font-weight: normal;">Quantity</span></th>
                    <th style="width: 20%; padding: 4px;">จำนวนเงิน<br><span style="font-size: 11px; font-weight: normal;">Amount</span></th>
                </tr>
            </thead>
            <tbody>
                <tr style="height: 24px; text-align: center;">
                    <td style="border-right: 1px solid #000; padding: 2px;">1</td>
                    <td style="border-right: 1px solid #000; padding: 2px 8px; text-align: left;">{item_desc}</td>
                    <td style="border-right: 1px solid #000; padding: 2px;">{item_qty}</td>
                    <td style="padding: 2px 8px; text-align: right;">{item_amount:,.2f}</td>
                </tr>
                <!-- Empty Rows for Form Balance -->
                <tr style="height: 22px;"><td style="border-right: 1px solid #000;"></td><td style="border-right: 1px solid #000;"></td><td style="border-right: 1px solid #000;"></td><td></td></tr>
                <tr style="height: 22px;"><td style="border-right: 1px solid #000;"></td><td style="border-right: 1px solid #000;"></td><td style="border-right: 1px solid #000;"></td><td></td></tr>
                <tr style="height: 22px;"><td style="border-right: 1px solid #000;"></td><td style="border-right: 1px solid #000;"></td><td style="border-right: 1px solid #000;"></td><td></td></tr>
                <tr style="height: 22px;"><td style="border-right: 1px solid #000;"></td><td style="border-right: 1px solid #000;"></td><td style="border-right: 1px solid #000;"></td><td></td></tr>
                <tr style="height: 22px;"><td style="border-right: 1px solid #000;"></td><td style="border-right: 1px solid #000;"></td><td style="border-right: 1px solid #000;"></td><td></td></tr>
                <!-- Total Row -->
                <tr style="border-top: 1px solid #000; font-weight: bold;">
                    <td colspan="2" style="border-right: 1px solid #000; padding: 4px 8px; text-align: left;">{text_baht}</td>
                    <td style="border-right: 1px solid #000; padding: 4px; text-align: center;">ยอดยอดสุทธิ</td>
                    <td style="padding: 4px 8px; text-align: right;">{item_amount:,.2f}</td>
                </tr>
            </tbody>
        </table>

        <!-- Payment Checkboxes -->
        <div style="margin-top: 8px; font-size: 12px; line-height: 1.8;">
            <div><b>ชำระโดย :</b></div>
            <div>{"[ ✓ ]" if pay_type == "เงินสด" else "[ &nbsp; ]"} เงินสด ...................................................................บาท</div>
            <div>{"[ ✓ ]" if pay_type == "เงินโอน" else "[ &nbsp; ]"} เงินโอน ...................................................................บาท</div>
            <div>{"[ ✓ ]" if pay_type == "เช็ค" else "[ &nbsp; ]"} เช็ค &nbsp; ธนาคาร........................................สาขา...........................................................................................</div>
        </div>

        <!-- Signature Footer Table -->
        <table style="width: 100%; border-collapse: collapse; border: 1px solid #000; margin-top: 15px; text-align: center; font-size: 12px;">
            <tr>
                <td style="width: 33%; border-right: 1px solid #000; padding: 6px; vertical-align: top;">
                    <div>ผู้รับเงิน</div>
                    <br><br>
                    <div>วันที่................................................</div>
                </td>
                <td style="width: 33%; border-right: 1px solid #000; padding: 6px; vertical-align: top;">
                    <div>ผู้รับใบเสร็จ</div>
                    <br><br>
                    <div>วันที่................................................</div>
                </td>
                <td style="width: 34%; padding: 6px; vertical-align: top;">
                    <div>ในนามบริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div>
                    <br><br>
                    <div>ประทับตราบริษัท</div>
                </td>
            </tr>
        </table>

    </div>
    """

    st.markdown(receipt_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ปุ่มสั่งพิมพ์ตรง
    print_script = f"""
    <script>
    function printReceipt() {{
        var printContents = `{receipt_html}`;
        var win = window.open('', '', 'height=850,width=750');
        win.document.write('<html><head><title>Print Receipt</title>');
        win.document.write('<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">');
        win.document.write('<style>body {{ font-family: "Sarabun", sans-serif; margin: 0; padding: 15px; }} @page {{ size: A4 portrait; margin: 10mm; }}</style>');
        win.document.write('</head><body>');
        win.document.write(printContents);
        win.document.write('</body></html>');
        win.document.close();
        setTimeout(function() {{ win.print(); }}, 500);
    }}
    </script>
    <button onclick="printReceipt()" style="width: 100%; background-color: #059669; color: white; border: none; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px;">
        🖨️ พิมพ์ใบเสร็จรับเงิน (Print / Save PDF)
    </button>
    """
    st.components.v1.html(print_script, height=60)
