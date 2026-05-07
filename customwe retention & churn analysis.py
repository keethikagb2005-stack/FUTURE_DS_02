from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import os
import random

app = Flask(__name__)

# ------------------------------------------
# CREATE CUSTOMER DATASET
# ------------------------------------------

customer_data = {
    "Customer_ID": [],
    "Name": [],
    "Subscription_Type": [],
    "Monthly_Spend": [],
    "Tenure_Months": [],
    "Support_Tickets": [],
    "Last_Login_Days": [],
    "Churn_Status": []
}

names = [
    "Arun","Vijay","Karthik","Priya","Divya",
    "Rahul","Sneha","Meena","Ravi","Kiran",
    "Anu","Suresh","Lokesh","Keerthi","Varun",
    "Aakash","Nisha","Pooja","Deepak","Hari"
]

plans = ["Basic", "Standard", "Premium"]

for i in range(1, 101):

    tenure = random.randint(1, 36)
    spend = random.randint(300, 3000)
    tickets = random.randint(0, 10)
    login_days = random.randint(1, 60)

    # Churn Logic
    if tenure < 6 and login_days > 25:
        churn = "Yes"
    elif tickets > 6:
        churn = "Yes"
    else:
        churn = random.choice(["No", "No", "No", "Yes"])

    customer_data["Customer_ID"].append(i)
    customer_data["Name"].append(random.choice(names))
    customer_data["Subscription_Type"].append(random.choice(plans))
    customer_data["Monthly_Spend"].append(spend)
    customer_data["Tenure_Months"].append(tenure)
    customer_data["Support_Tickets"].append(tickets)
    customer_data["Last_Login_Days"].append(login_days)
    customer_data["Churn_Status"].append(churn)

# ------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------

df = pd.DataFrame(customer_data)

# ------------------------------------------
# KPI CALCULATIONS
# ------------------------------------------

total_customers = len(df)

churn_customers = len(df[df["Churn_Status"] == "Yes"])

retained_customers = len(df[df["Churn_Status"] == "No"])

churn_rate = round((churn_customers / total_customers) * 100, 2)

avg_spend = round(df["Monthly_Spend"].mean(), 2)

avg_tenure = round(df["Tenure_Months"].mean(), 2)

# ------------------------------------------
# SAVE CHARTS
# ------------------------------------------

if not os.path.exists("static"):
    os.makedirs("static")

# Churn Distribution Chart
plt.figure(figsize=(6,5))
df["Churn_Status"].value_counts().plot(
    kind="bar"
)
plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Customers")
plt.savefig("static/churn_chart.png")
plt.close()

# Subscription Type Analysis
plt.figure(figsize=(6,5))
df.groupby("Subscription_Type")["Monthly_Spend"].mean().plot(
    kind="bar"
)
plt.title("Average Spend by Subscription")
plt.xlabel("Plan")
plt.ylabel("Average Spend")
plt.savefig("static/subscription_chart.png")
plt.close()

# Tenure Analysis
plt.figure(figsize=(7,5))
plt.hist(df["Tenure_Months"], bins=10)
plt.title("Customer Tenure Distribution")
plt.xlabel("Tenure Months")
plt.ylabel("Customers")
plt.savefig("static/tenure_chart.png")
plt.close()

# Support Ticket Analysis
plt.figure(figsize=(7,5))
plt.scatter(df["Support_Tickets"], df["Monthly_Spend"])
plt.title("Support Tickets vs Monthly Spend")
plt.xlabel("Support Tickets")
plt.ylabel("Monthly Spend")
plt.savefig("static/support_chart.png")
plt.close()

# ------------------------------------------
# INSIGHTS
# ------------------------------------------

insights = [
    "Customers with low tenure are more likely to churn.",
    "High support ticket count increases churn probability.",
    "Premium users contribute higher revenue.",
    "Inactive customers show higher churn rate.",
    "Retention campaigns can target low-login customers."
]

# ------------------------------------------
# HOME PAGE
# ------------------------------------------

@app.route('/')

def dashboard():

    customer_table = df.head(20).to_html(
        classes='table table-bordered table-striped',
        index=False
    )

    return render_template(
        "index.html",
        total_customers=total_customers,
        churn_customers=churn_customers,
        retained_customers=retained_customers,
        churn_rate=churn_rate,
        avg_spend=avg_spend,
        avg_tenure=avg_tenure,
        customer_table=customer_table,
        insights=insights
    )

# ------------------------------------------
# RUN SERVER
# ------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)