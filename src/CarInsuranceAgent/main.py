import sys
package = __import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from crew_setup import value_agent, info_agent

st.title("🚗 Car Insurance Assistant")

task = st.radio("Choose a task", ["Estimate Car Value", "Ask Insurance Question"])

if task == "Estimate Car Value":
    car_details = st.text_area("Enter your car details (Make, Model, Year, Condition):")
    if st.button("Estimate Value"):
        if car_details:
            with st.spinner("Estimating..."):
                result = value_agent.run(car_details)
                st.success(result)
        else:
            st.warning("Please enter car details.")

elif task == "Ask Insurance Question":
    user_question = st.text_area("Enter your insurance-related question:")
    if st.button("Get Answer"):
        if user_question:
            with st.spinner("Thinking..."):
                result = info_agent.run(user_question)
                st.success(result)
        else:
            st.warning("Please enter a question.")
