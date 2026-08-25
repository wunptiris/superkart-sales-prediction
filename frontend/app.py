
import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

st.title("🛒🛒 Superkart Sales Prediction 🛒🛒")

# Section for online prediction
st.subheader("Online Prediction")

# Input fields for product and store data
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=10.0)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.01)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=100.0)
Store_Size = st.selectbox("Store Size", ["High", "Medium", "Small"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Departmental Store", "Food Mart", "Supermarket Type1", "Supermarket Type2"])
Product_Id_char = st.selectbox("Product ID Category", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store_Age_Years", min=0, max=50.00)
Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

# convert user input into a Dataframe
product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

# make prediction when the "Predict" button is clicked
if st.button("Predict", type='primary'):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data)
    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Sales"]
        st.write(f"Predicted Product Store Sales Total: ₹{predicted_sales:.2f}")
    else:
        st.error("Error in API request")

# Section for batch prediction
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload a CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the CSV file into a pandas DataFrame
        batch_data_df = pd.read_csv(uploaded_file)
        st.write("Uploaded data preview:")
        st.dataframe(batch_data_df.head())

        if st.button("Run Batch Prediction"):
            # Convert DataFrame to list of dictionaries for JSON payload
            batch_data_json = batch_data_df.to_dict(orient="records")

            # Make POST request to the batch prediction endpoint
            batch_response = requests.post(f"{BACKEND_URL}/v1/batch_predict", json=batch_data_json)

            if batch_response.status_code == 200:
                batch_results = batch_response.json()
                st.write("Batch Prediction Results:")
                # Create a DataFrame for better display
                results_df = pd.DataFrame({"Predicted Sales": batch_results["Sales_Predictions"]})
                st.dataframe(results_df)
            else:
                st.error(f"Error in batch API request: {batch_response.status_code} - {batch_response.text}")
    except Exception as e:
        st.error(f"Error processing file: {e}")
