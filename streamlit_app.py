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
    "Job Satisfaction(Least-1, Best-4)")",
    [1, 2, 3, 4]
)

work_life_balance = st.selectbox(
    "Work Life Balance(Least-1, Best-4)" )",
    [1, 2, 3, 4]
)

years_at_company = st.number_input(
    "Years At Company",
    min_value=0,
    value=5
)

experience = st.number_input(
    "Total Experience (Years)",
    min_value=0,
    value=3
)

salary_lpa = st.number_input(
    "Annual Salary (LPA)",
    min_value=1.0,
    value=6.0
)

department = st.selectbox(
    "Department",
    [
        "IT",
        "Sales",
        "Human Resources"
    ]
)

if department == "IT":

    display_role = st.selectbox(
        "Job Role",
        [
            "Software Engineer",
            "Data Scientist",
            "Data Analyst",
            "DevOps Engineer",
            "QA Engineer"
        ]
    )

    role_mapping = {
        "Software Engineer": "Research Scientist",
        "Data Scientist": "Research Director",
        "Data Analyst": "Research Scientist",
        "DevOps Engineer": "Manager",
        "QA Engineer": "Laboratory Technician"
    }

    model_department = "Research & Development"

elif department == "Sales":

    display_role = st.selectbox(
        "Job Role",
        [
            "Sales Executive",
            "Business Development Executive",
            "Account Manager",
            "Sales Manager"
        ]
    )

    role_mapping = {
        "Sales Executive": "Sales Executive",
        "Business Development Executive": "Sales Representative",
        "Account Manager": "Sales Executive",
        "Sales Manager": "Manager"
    }

    model_department = "Sales"
else:

    display_role = st.selectbox(
        "Job Role",
        [
            "HR Executive",
            "Recruiter",
            "HR Manager"
        ]
    )

    role_mapping = {
        "HR Executive": "Human Resources",
        "Recruiter": "Human Resources",
        "HR Manager": "Manager"
    }

    model_department = "Research & Development"

job_role = role_mapping[display_role]

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
        "Department": model_department,
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

# Business Risk Score

        risk_score = 0
        risk_factors = []

        if overtime == "Yes":
            risk_score += 25
            risk_factors.append("Frequent Overtime")

        if job_satisfaction <= 2:
            risk_score += 25
            risk_factors.append("Low Job Satisfaction")

        if work_life_balance <= 2:
            risk_score += 20
            risk_factors.append("Poor Work-Life Balance")

        if years_at_company > 3:
            risk_score += 10
            risk_factors.append("Long Tenure Without Change")

        if department == "IT":
            if experience >= 5 and salary_lpa < 12:
                risk_score += 20
                risk_factors.append("Salary Below Market Average")

        elif department == "Sales":
              if experience >= 5 and salary_lpa < 10:
                  risk_score += 20
                  risk_factors.append("Salary Below Market Average")

        elif department == "Human Resources":
              if experience >= 5 and salary_lpa < 8:
                  risk_score += 20
                  risk_factors.append("Salary Below Market Average")

        if risk_score >= 60:
            business_risk = "High Risk"
        elif risk_score >= 30:
            business_risk = "Medium Risk"
        else:
            business_risk = "Low Risk"

# Performance Rating
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

# Result Display

        st.divider()

        if prediction == "High Attrition Risk":
            st.error(f"Prediction: {prediction}")
            st.metric("Estimated Attrition Risk", "85%")
        else:
            st.success(f"Prediction: {prediction}")
            st.metric("Estimated Attrition Risk", "15%")

# Employee Assessment

        st.subheader("Employee Assessment")

        st.write(f"**Performance Rating:** {rating}")
        st.write(f"**Business Risk Level:** {business_risk}")
        st.write(f"**Risk Score:** {risk_score}/100")
        st.write(f"**Department:** {department}")
        st.write(f"**Job Role:** {display_role}")

        if risk_factors:
           st.write("### Key Risk Factors")
        for factor in risk_factors:
           st.write(f"• {factor}")

# Retention Strategy

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

        else:

            st.subheader("Promotion Assessment")

            if rating.startswith("Excellent"):
                st.success("Recommended Promotion Timeline: 6-12 Months")

            elif rating.startswith("Good"):
                st.success("Recommended Promotion Timeline: 12-18 Months")

            elif rating.startswith("Average"):
                st.warning("Recommended Promotion Timeline: 18-24 Months")

            else:
                st.error("Promotion Not Recommended Currently")

    except Exception as e:
        st.error(f"Error: {e}")