import streamlit as st
import base64

def show_logo_and_centered_title(period_label=None):
    logo_path = "assets/logo.png"
    with open(logo_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
        <style>
            .custom-header {{
                background-color: #17193b;
                padding: 30px 40px 30px 40px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .logo-left {{
                display: flex;
                justify-content: flex-start;
                margin-bottom: 10px;
            }}
            .logo-left img {{
                width: 130px;
            }}
            .title-center {{
                text-align: center;
                margin: 0;
                color: white !important;
                font-size: 28px;
                font-weight: bold;
            }}
            .period-subtitle {{
                text-align: center;
                font-size: 18px;
                color: white;
                margin-top: 6px;
                font-weight: 500;
            }}
        </style>

        <div class="custom-header">
            <div class="logo-left">
                <img src="data:image/png;base64,{encoded_image}" alt="ValOre Logo">
            </div>
            <h1 class="title-center">ValOre Trading Insights</h1>
            {f'<div class="period-subtitle">Reference Period: {period_label}</div>' if period_label else ''}
        </div>
    """, unsafe_allow_html=True)
