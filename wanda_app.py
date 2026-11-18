import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sunshine Cattle Feed", layout="wide")

st.title("🐄 Sunshine Cattle Feed")
st.subheader("Feed Formulation & Cost Calculator")

if "df" not in st.session_state:
    data = {
        "Ingredient": [
            "Maize (Makai)",
            "Wheat Bran (Choker)",
            "Cottonseed Cake (Khal Banola)",
            "Canola Meal",
            "Soybean Meal",
            "Corn Gluten 30%",
            "Molasses (Sheera)",
            "DCP (Dicalcium Phosphate)",
            "Limestone / Marble Powder",
            "Salt (Namak)",
            "Mineral Premix & Toxin Binder"
        ],
        "CP (%)": [8.5, 14.5, 22.0, 36.0, 44.0, 28.0, 3.5, 0.0, 0.0, 0.0, 0.0],
        "ME (Mcal/kg)": [3.10, 2.45, 2.30, 2.65, 3.05, 2.75, 2.40, 0.0, 0.0, 0.0, 0.0],
        "TDN (%)": [85.0, 68.0, 65.0, 72.0, 82.0, 75.0, 68.0, 0.0, 0.0, 0.0, 0.0],
        "Fiber (%)": [2.2, 10.5, 22.0, 11.5, 6.5, 8.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Price (Rs/kg)": [75.0, 68.0, 95.0, 115.0, 175.0, 92.0, 45.0, 140.0, 12.0, 18.0, 250.0],
        "Inclusion (%)": [25.0, 25.0, 15.0, 12.0, 5.0, 8.0, 7.0, 1.0, 1.0, 0.5, 0.5]
    }
    st.session_state.df = pd.DataFrame(data)

with st.expander("➕ Naya Ingredient Shamil Karein (Click Here to Add New Item)", expanded=True):
    with st.form("add_ingredient_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        new_name = c1.text_input("Ingredient ka Naam (maslan: Rice Polish)")
        new_cp = c2.number_input("CP (%)", min_value=0.0, max_value=100.0, value=12.0, step=0.5)
        new_me = c3.number_input("ME (Mcal/kg)", min_value=0.0, max_value=10.0, value=2.50, step=0.05)
        new_tdn = c4.number_input("TDN (%)", min_value=0.0, max_value=100.0, value=70.0, step=1.0)
        
        c5, c6, c7, c8 = st.columns(4)
        new_fiber = c5.number_input("Fiber (%)", min_value=0.0, max_value=100.0, value=8.0, step=0.5)
        new_price = c6.number_input("Price (Rs/kg)", min_value=0.0, value=60.0, step=1.0)
        new_inc = c7.number_input("Inclusion (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        
        submitted = st.form_submit_button("✅ Table Mein Add Karein")
        if submitted and new_name.strip() != "":
            new_row = pd.DataFrame([{
                "Ingredient": new_name.strip(),
                "CP (%)": new_cp,
                "ME (Mcal/kg)": new_me,
                "TDN (%)": new_tdn,
                "Fiber (%)": new_fiber,
                "Price (Rs/kg)": new_price,
                "Inclusion (%)": new_inc
            }])
            st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
            st.success(f"'{new_name}' table mein shamil ho gaya hai!")
            st.rerun()

col_batch1, col_batch2 = st.columns([1, 3])
with col_batch1:
    batch_size = st.number_input("Mixing Batch Size (kg):", min_value=40, value=1000, step=40)

st.subheader("1. Ingredients & Formulation Table")

edited_df = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    width="stretch",
    key="editor",
    column_config={
        "Inclusion (%)": st.column_config.NumberColumn(min_value=0.0, max_value=100.0, step=0.5, format="%.2f"),
        "Price (Rs/kg)": st.column_config.NumberColumn(min_value=0.0, step=1.0, format="Rs %.2f"),
        "CP (%)": st.column_config.NumberColumn(min_value=0.0, format="%.2f"),
        "ME (Mcal/kg)": st.column_config.NumberColumn(min_value=0.0, format="%.2f"),
        "TDN (%)": st.column_config.NumberColumn(min_value=0.0, format="%.2f"),
        "Fiber (%)": st.column_config.NumberColumn(min_value=0.0, format="%.2f"),
    }
)

st.session_state.df = edited_df

total_pct = edited_df["Inclusion (%)"].sum()

edited_df["Batch Weight (kg)"] = (edited_df["Inclusion (%)"] / 100.0) * batch_size
edited_df["40kg Bag Weight (kg)"] = (edited_df["Inclusion (%)"] / 100.0) * 40.0
edited_df["Cost Contribution (Rs/kg)"] = (edited_df["Inclusion (%)"] / 100.0) * edited_df["Price (Rs/kg)"]

final_cp = ((edited_df["Inclusion (%)"] * edited_df["CP (%)"]) / 100.0).sum()
final_me = ((edited_df["Inclusion (%)"] * edited_df["ME (Mcal/kg)"]) / 100.0).sum()
final_tdn = ((edited_df["Inclusion (%)"] * edited_df["TDN (%)"]) / 100.0).sum()
final_fiber = ((edited_df["Inclusion (%)"] * edited_df["Fiber (%)"]) / 100.0).sum()

cost_per_kg = edited_df["Cost Contribution (Rs/kg)"].sum()
cost_per_40kg = cost_per_kg * 40.0
cost_per_batch = cost_per_kg * batch_size

st.divider()
if round(total_pct, 2) == 100.0:
    st.success(f"✅ Total Formulation: **{total_pct:.2f}%** (Bilkul Mukammal!)")
elif total_pct < 100.0:
    st.warning(f"⚠️ Total Formulation: **{total_pct:.2f}%** — Abhi **{100.0 - total_pct:.2f}%** mazeed shamil karna baqi hai.")
else:
    st.error(f"❌ Total Formulation: **{total_pct:.2f}%** — **{total_pct - 100.0:.2f}%** zyada ho gaya hai, kam karein.")

st.subheader("2. Final Nutritional & Cost Results")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Crude Protein (CP)", f"{final_cp:.2f} %")
m2.metric("Metabolizable Energy (ME)", f"{final_me:.2f} Mcal/kg")
m3.metric("Total Digestible Nutrients (TDN)", f"{final_tdn:.2f} %")
m4.metric("Crude Fiber (CF)", f"{final_fiber:.2f} %")

c1, c2, c3 = st.columns(3)
c1.metric("1 kg Wanda Qeemat", f"Rs {cost_per_kg:.2f}")
c2.metric("40 kg Bag Qeemat", f"Rs {cost_per_40kg:,.2f}")
c3.metric(f"{batch_size} kg Batch Qeemat", f"Rs {cost_per_batch:,.2f}")

st.divider()
st.subheader("3. Mixing Plant Batch Sheet (Wazan ki Parchi)")

batch_sheet = edited_df[edited_df["Inclusion (%)"] > 0][["Ingredient", "Inclusion (%)", "40kg Bag Weight (kg)", "Batch Weight (kg)", "Price (Rs/kg)", "Cost Contribution (Rs/kg)"]].copy()
batch_sheet["Total Batch Cost (Rs)"] = batch_sheet["Batch Weight (kg)"] * batch_sheet["Price (Rs/kg)"]

st.dataframe(batch_sheet, width="stretch", hide_index=True)

csv = batch_sheet.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Sunshine Cattle Feed Batch Sheet Download Karein (Excel/CSV)",
    data=csv,
    file_name="sunshine_cattle_feed_batch.csv",
    mime="text/csv",
)
