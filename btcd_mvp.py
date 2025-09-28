import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

st.title("BTDC – BRICS Trade Digital Corridor MVP")

# Compliance data
compliance_data = pd.DataFrame({
    "Country": ["Brazil", "Russia", "India", "China", "South Africa"],
    "Tariff (%)": [12, 10, 8, 15, 9],
    "Documents Required": [
        "Invoice, Certificate of Origin",
        "Invoice, Import License",
        "Invoice, GST, IEC Code",
        "Invoice, Customs Declaration",
        "Invoice, Import Permit"
    ],
    "Sector": ["Agro", "Pharma", "IT Services", "Textiles", "Automobile"]
})

country_choice = st.selectbox("Select Country", compliance_data["Country"])
sector_choice = st.selectbox("Select Sector", compliance_data["Sector"])
filtered = compliance_data[(compliance_data["Country"]==country_choice) & 
                           (compliance_data["Sector"]==sector_choice)]
st.write(filtered)

# MSME Onboarding
st.header("MSME Exporter Onboarding")
with st.form("onboard_form"):
    name = st.text_input("Company Name")
    email = st.text_input("Email")
    value = st.number_input("Product Value (USD)", 0)
    submit = st.form_submit_button("Register")

if submit:
    st.success(f"Thank you {name}, you are registered for the BTDC pilot!")
    st.info(f"Export Checklist for {sector_choice} to {country_choice}:")
    st.write(filtered["Documents Required"].values[0].split(", "))

# Export cost calculator
st.header("Export Cost Calculator")
tariff = filtered["Tariff (%)"].values[0]
fx_rate = 83.5
total_cost_inr = value * fx_rate * (1 + tariff/100)
st.write(f"Landed Cost (INR) including {tariff}% tariff: ₹{total_cost_inr:,.2f}")

# PDF generation
st.header("Generate Export Document")
def create_pdf(company, country, sector, value, cost):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BTDC – Export Certificate", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Exporter: {company}", ln=True)
    pdf.cell(0, 10, f"Destination Country: {country}", ln=True)
    pdf.cell(0, 10, f"Sector: {sector}", ln=True)
    pdf.cell(0, 10, f"Product Value (USD): {value}", ln=True)
    pdf.cell(0, 10, f"Landed Cost (INR): {cost:,.2f}", ln=True)
    pdf.cell(0, 10, f"Required Documents: {filtered['Documents Required'].values[0]}", ln=True)
    pdf.output("export_certificate.pdf")

if submit:
    create_pdf(name, country_choice, sector_choice, value, total_cost_inr)
    st.success("Export certificate PDF generated! Check Colab Files.")

# Trade Opportunity Dashboard
st.header("Trade Opportunity Dashboard")
trade_data = pd.DataFrame({
    "Sector": ["Pharma", "Agro", "IT Services", "Textiles", "Automobile"],
    "Trade Volume (USD M)": [120, 200, 150, 80, 60],
    "Risk Score": [2, 3, 1, 4, 2]
})
fig = px.bar(trade_data, x="Sector", y="Trade Volume (USD M)",
             color="Risk Score", title="Top Export Opportunities (Mock Data)")
st.plotly_chart(fig)

