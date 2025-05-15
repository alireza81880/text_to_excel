# app.py
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="تبدیل متن به اکسل", layout="centered")

st.title("🧾 تبدیل متن به فایل اکسل")

with st.expander("📘 راهنمای استفاده"):
    st.markdown("""
    - متن هر ردیف را در یک خط جداگانه وارد کنید.
    - ستون‌ها را با ویرگول `,` جدا کنید.
    - اولین خط باید عنوان ستون‌ها باشد.
    
    **مثال:**
    ```
    نام,سن,شهر
    علی,25,تهران
    مینا,30,اصفهان
    ```
    """)

text_input = st.text_area("متن را وارد کنید:", height=250)

if st.button("تبدیل به اکسل"):
    rows = [r.split(',') for r in text_input.splitlines() if r.strip()]
    if len(rows) < 2:
        st.error("حداقل باید یک عنوان و یک ردیف داده وارد شود.")
    else:
        header = rows[0]
        valid_rows = [r for r in rows[1:] if len(r) == len(header)]
        invalids = [i+2 for i, r in enumerate(rows[1:]) if len(r) != len(header)]

        if invalids:
            st.warning(f"ردیف‌های نامعتبر (تعداد ستون ناهماهنگ): {invalids}")
        else:
            df = pd.DataFrame(valid_rows, columns=header)
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            st.success("فایل آماده است برای دانلود:")
            st.download_button(
                "📥 دانلود فایل اکسل",
                buffer.getvalue(),
                file_name="output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
