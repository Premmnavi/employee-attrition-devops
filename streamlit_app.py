import streamlit as st
import requests

st.set_page_config(
    page_title="Employee Attrition Prediction System",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Employee Attrition Prediction System")
st.write("Predict employee attrition risk and receive HR recommendations.")

# =========================
# USER INPUTs
# =========================

age = st.number_input(
    "Age",
    min_value=18,
    max_value=65,
    value=30
)

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

# =========================
# PREDICT BUTTON
# =========================

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

        # Default Values

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

        # =========================
        # PERFORMANCE RATING
        # =========================

        performance_score = (
            (job_satisfaction * 10)
            + (work_life_balance * 10)
            + (min(years_at_company, 10) * 2)
        )

        if performance_score >= 55:
            rating = "Excellent ⭐⭐⭐⭐⭐"
        elif performance_score >= 40:
            rating = "Good ⭐⭐⭐⭐"
        elif performance_score >= 25:
            rating = "Average ⭐⭐⭐"
        else:
            rating = "Needs Improvement ⭐⭐"

        # =========================
        # RESULT DISPLAY
        # =========================

        st.divider()

        if prediction == "High Attrition Risk":

            st.error(f"Prediction: {prediction}")
            st.metric(
                label="Estimated Attrition Risk",
                value="85%"
            )

        else:

            st.success(f"Prediction: {prediction}")
            st.metric(
                label="Estimated Attrition Risk",
                value="15%"
            )

        # =========================
        # EMPLOYEE ASSESSMENT
        # =========================

        st.subheader("Employee Assessment")

        st.write(f"**Performance Rating:** {rating}")

        st.write(f"**Department:** {department}")

        st.write(f"**Job Role:** {job_role}")

        # =========================
        # RETENTION STRATEGY
        # =========================

        if prediction == "High Attrition Risk":

            st.subheader("Recommended Retention Strategy")

            if overtime == "Yes":
                st.write("• Reduce overtime workload")
                st.write("• Improve staffing allocation")

            if job_satisfaction <= 2:
                st.write("• Conduct employee engagement sessions")
                st.write("• Improve manager feedback process")

            if work_life_balance <= 2:
                st.write("• Flexible working arrangements")
                st.write("• Encourage leave utilization")

            if monthly_income < 4000:
                st.write("• Salary review recommended")
                st.write("• Introduce performance incentives")

            st.write("• Career growth opportunities")
            st.write("• Training and development programs")

        # =========================
        # PROMOTION TIMELINE
        # =========================

        else:

            st.subheader("Promotion Assessment")

            if rating.startswith("Excellent"):
                st.success(
                    "Recommended Promotion Timeline: 6-12 Months"
                )

            elif rating.startswith("Good"):
                st.success(
                    "Recommended Promotion Timeline: 12-18 Months"
                )

            elif rating.startswith("Average"):
                st.warning(
                    "Recommended Promotion Timeline: 18-24 Months"
                )

            else:
                st.error(
                    "Promotion Not Recommended Currently"
                )

    except Exception as e:

        st.error(f"Error: {e}")