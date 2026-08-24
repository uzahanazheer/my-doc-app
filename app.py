import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

st.set_page_config(page_title="ระบบออกใบเสร็จรับเงิน", page_icon="🧾", layout="wide")

# File path สำหรับเก็บฐานข้อมูลลูกค้า
DB_FILE = "customers.csv"

# โหลดหรือสร้างฐานข้อมูลลูกค้า
if os.path.exists(DB_FILE):
    df_customers = pd.read_csv(DB_FILE, dtype=str)
else:
    df_customers = pd.DataFrame([
        {
            "code": "00001",
            "name": "บริษัท บุรีรัมย์พนาสิทธิ์ จำกัด (สาขา 00003)",
            "address": "52/647 หมู่ที่ 7 หมู่บ้าน เมืองเอก โครงการ 4 ตำบล หลักหก อำเภอ เมืองปทุมธานี จังหวัด ปทุมธานี 12000",
            "taxid": "0315561000656"
        }
    ])
    df_customers.to_csv(DB_FILE, index=False)

st.markdown("## 🧾 ระบบออกใบเสร็จรับเงิน (Official Receipt)")

col_input, col_preview = st.columns([0.42, 0.58], gap="large")

with col_input:
    tab1, tab2 = st.tabs(["📝 ออกใบเสร็จ", "👥 จัดการข้อมูลลูกค้า"])

    with tab2:
        st.subheader("➕ เพิ่ม/แก้ไข ข้อมูลลูกค้า")
        new_code = st.text_input("รหัสลูกค้า (Customer Code)", f"CUST-00{len(df_customers)+1}")
        new_name = st.text_input("ชื่อลูกค้า/บริษัท", "")
        new_address = st.text_area("ที่อยู่", "", height=70)
        new_taxid = st.text_input("เลขประจำตัวผู้เสียภาษี", "")
        
        if st.button("💾 บันทึกข้อมูลลูกค้าลงระบบ", type="primary"):
            if new_name and new_code:
                # เช็คว่ามีรหัสเดิมไหม ถ้ามีให้แทนที่
                df_customers = df_customers[df_customers["code"] != new_code]
                new_row = pd.DataFrame([{"code": new_code, "name": new_name, "address": new_address, "taxid": new_taxid}])
                df_customers = pd.concat([df_customers, new_row], ignore_index=True)
                df_customers.to_csv(DB_FILE, index=False)
                st.success(f"บันทึกข้อมูลลูกค้า {new_name} เรียบร้อยแล้ว!")
                st.rerun()
            else:
                st.warning("กรุณากรอกรหัสลูกค้าและชื่อลูกค้าก่อนบันทึก")

        st.markdown("---")
        st.write("📋 **รายชื่อลูกค้าในระบบ:**")
        st.dataframe(df_customers, use_container_width=True, hide_index=True)

    with tab1:
        st.subheader("📝 กรอกรายละเอียดใบเสร็จ")
        
        with st.expander("1. ข้อมูลหัวเอกสารและใบเสร็จ", expanded=True):
            doc_type = st.text_input("ประเภทเอกสาร (มุมขวาบน)", "ต้นฉบับใบเสร็จรับเงิน")
            receipt_no = st.text_input("เลขที่ใบเสร็จรับเงิน (Receipt No.)", "260012")
            receipt_date = st.text_input("วันที่ / Date", "23/7/2569")
            payment_term = st.selectbox("เงื่อนไขการชำระเงิน (Terms of Payment)", ["Cash", "Transfer", "Cheque", "Credit"])
            driver_name = st.text_input("พนักงานขนส่ง", "")

        with st.expander("2. เลือกลูกค้าจากระบบ", expanded=True):
            customer_list = ["-- เลือก หรือ กรอกเอง --"] + [f"{r['code']} | {r['name']}" for _, r in df_customers.iterrows()]
            selected_cust = st.selectbox("ดึงข้อมูลลูกค้าเก่า", customer_list)

            if selected_cust != "-- เลือก หรือ กรอกเอง --":
                cust_code = selected_cust.split(" | ")[0]
                matched = df_customers[df_customers["code"] == cust_code].iloc[0]
                default_code = matched["code"]
                default_name = matched["name"]
                default_address = matched["address"]
                default_taxid = matched["taxid"]
            else:
                default_code = ""
                default_name = "บริษัท บุรีรัมย์พนาสิทธิ์ จำกัด (สาขา 00003)"
                default_address = "52/647 หมู่ที่ 7 หมู่บ้าน เมืองเอก โครงการ 4 ตำบล หลักหก อำเภอ เมืองปทุมธานี จังหวัด ปทุมธานี 12000"
                default_taxid = "0315561000656"

            customer_code = st.text_input("รหัสลูกค้า", default_code)
            cust_name = st.text_input("ชื่อลูกค้า", default_name)
            cust_address = st.text_area("ที่อยู่ลูกค้า", default_address, height=70)
            cust_taxid = st.text_input("เลขประจำตัวผู้เสียภาษีลูกค้า", default_taxid)

        with st.expander("3. รายการสินค้า / บริการ", expanded=True):
            item_desc = st.text_input("รายการ (Description)", "ค่าขนส่งสินค้า")
            c1, c2, c3 = st.columns(3)
            with c1:
                item_qty = st.number_input("จำนวน", min_value=1, value=2)
            with c2:
                item_unit = st.text_input("หน่วย", "เที่ยว")
            with c3:
                item_price = st.number_input("ราคา/หน่วย", min_value=0.0, value=4200.00, step=100.0)
                
            item_amount = item_qty * item_price
            st.info(f"💰 จำนวนเงินรวม: **{item_amount:,.2f}** บาท")
            text_baht = st.text_input("จำนวนเงินตัวอักษร", "แปดพันสี่ร้อยบาทถ้วน")

        with st.expander("4. การชำระเงิน", expanded=False):
            pay_type = st.radio("ชำระโดย", ["เงินสด", "เงินโอน", "เช็ค"], index=0)

chk_cash = "[ ✓ ]" if pay_type == "เงินสด" else "[ &nbsp; ]"
chk_transfer = "[ ✓ ]" if pay_type == "เงินโอน" else "[ &nbsp; ]"
chk_cheque = "[ ✓ ]" if pay_type == "เช็ค" else "[ &nbsp; ]"
formatted_price = f"{item_price:,.2f}"
formatted_amount = f"{item_amount:,.2f}"

# HTML Template บาลานซ์ A4 เป๊ะ 100%
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
    * {{
        box-sizing: border-box;
    }}
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
            <td style="width: 28%; vertical-align: top;">
                <div style="border: 1px solid #000; padding: 6px; text-align: center; font-size: 11px;">
                    <div style="font-weight: bold; font-size: 14px;">A&K</div>
                    <div>บริษัท เอ แอนด์ เค ทรานสปอร์ต จำกัด</div>
                    <div>A & K TRANSPORT CO.,LTD.</div>
                </div>
            </td>
            <td style="width: 72%; padding-left: 15px; vertical-align: top;">
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

<button class="btn-print" onclick="window.print()">🖨️ พิมพ์ใบเสร็จรับเงิน / Save PDF (บาลานซ์ A4)</button>

</body>
</html>
"""

with col_preview:
    st.subheader("👁️ ตัวอย่างใบเสร็จรับเงิน (Receipt Preview)")
    components.html(full_html, height=920, scrolling=True)
