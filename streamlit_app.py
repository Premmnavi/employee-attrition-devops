import streamlit as st
import requests

st.set_page_config(page_title="Employee Attrition Predictor")

st.title("Employee Attrition Prediction System")

# Inputs

age = st.number_input("Age", min_value=18, max_value=65, value=30)

monthly_income = st.number_input(
    "Monthly Income",
    min_value=1000,
    value=5000
)

job_satisfaction = st.selectbox(
    "Job Satisfaction",
    [1, 2, 3, 4]
)

work_life_balance = st.selectbox(
    "Work Life Balance",
    [1, 2, 3, 4]
)

years_at_company = st.number_input(
    "Years At Company",
    min_value=0,
    value=5
)

department = st.selectbox(
    "Department",
    [
        "Research & Development",
        "Sales"
    ]
)

job_role = st.selectbox(
    "Job Role",
    [
        "Sales Executive",
        "Research Scientist",
        "Laboratory Technician",
        "Manufacturing Director",
        "Healthcare Representative",
        "Manager",
        "Research Director",
        "Sales Representative",
        "Human Resources"
    ]
)

overtime = st.selectbox(
    "OverTime",
    ["No", "Yes"]
)

if st.button("Predict Attrition"):

    payload = {

        "Age": age,
        "MonthlyIncome": monthly_income,
        "JobSatisfaction": job_satisfaction,
        "WorkLifeBalance": work_life_balance,
        "YearsAtCompany": years_at_company,
        "Department": department,
        "JobRole": job_role,
        "OverTime": overtime,

        # Default values for remaining features

        "DailyRate": 800,
        "DistanceFromHome": 10,
        "Education": 3,
        "EnvironmentSatisfaction": 3,
        "HourlyRate": 80,
        "JobInvolvement": 3,
        "JobLevel": 2,
        "MonthlyRate": 15000,
        "NumCompaniesWorked": 2,
        "PercentSalaryHike": 15,
        "PerformanceRating": 3,
        "RelationshipSatisfaction": 3,
        "StockOptionLevel": 1,
        "TotalWorkingYears": 10,
        "TrainingTimesLastYear": 2,
        "YearsInCurrentRole": 3,
        "YearsSinceLastPromotion": 2,
        "YearsWithCurrManager": 3,
        "BusinessTravel": "Travel_Rarely",
        "EducationField": "Life Sciences",
        "Gender": "Male",
        "MaritalStatus": "Single"
    }

    try:

        response = requests.post(
            "https://employee-attrition-devops.onrender.com/predict",
            json=payload
        )

        result = response.json()

        prediction = result["prediction"]

        st.success(prediction)

        if prediction == "High Attrition Risk":

            st.warning("Recommended Retention Strategy")

            st.write("• Reduce overtime")
            st.write("• Improve work-life balance")
            st.write("• Career development opportunities")
            st.write("• Salary review and incentives")

        else:

            st.success("Promotion Timeline Recommendation")

            if years_at_company >= 5:
                st.write("Recommended Promotion Timeline: 6-12 Months")
            elif years_at_company >= 2:
                st.write("Recommended Promotion Timeline: 12-18 Months")
            else:
                st.write("Recommended Promotion Timeline: 18-24 Months")

    except Exception as e:

        st.error(f"Error: {e}")