import sys
package = __import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import streamlit as st
from car_value_estimation_setup import CarValueEstimatorCrew
from insurance_info_response_setup import InsuranceInfoResponderCrew
from image_car_analysis_setup import ImageCarAnalysisCrew 



st.title("🚗 Car Insurance Assistant")

task = st.radio("Choose a task", [
    "Estimate Car Value",
    "Ask Insurance Question",
    "Image-Based Car Estimation"  # ⬅️ new task option
])

if task == "Estimate Car Value":
    car_details = st.text_area("Enter your car details (Make, Model, Year, Condition):")
    if st.button("Estimate Value"):
        if car_details:
            with st.spinner("Estimating..."):
                result = CarValueEstimatorCrew().crew().kickoff(inputs={"car_details": car_details})
                st.success(result)
        else:
            st.warning("Please enter car details.")

elif task == "Ask Insurance Question":
    user_question = st.text_area("Enter your insurance-related question:")
    if st.button("Get Answer"):
        if user_question:
            with st.spinner("Thinking..."):
                result = InsuranceInfoResponderCrew().crew().kickoff(inputs={"user_question": user_question})
                st.success(result)
        else:
            st.warning("Please enter a question.")

elif task == "Image-Based Car Estimation":
    image_url = st.text_input("Paste the image URL (from Google, X, Facebook, etc.)")

    if st.button("Analyze Image"):
        if image_url:
            with st.spinner("Analyzing image..."):
                result = ImageCarAnalysisCrew().crew().kickoff(inputs={"image_url": image_url})
                st.success(result)
        else:
            st.warning("Please paste a valid image URL.")

