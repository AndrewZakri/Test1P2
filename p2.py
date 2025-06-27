import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Label Dashboard and configure layout
st.title("Test 1, Problem 2")

st.write("An academic institution wants to monitor their admission process and students' satisfaction.  Design a university dashboard that tracks student admissions, retention, and satisfaction. Metrics and Key Performance Indicators (KPIs) were developed to assist the university.")

st.title("University Student Dashboard")

# Load the provided CSV for problem 2
df = pd.read_csv("university_student_dashboard_data.csv")

# Rename columns for consistency
df.columns = [col.strip().replace(" ", "_") for col in df.columns]

# Convert to appropriate data types
df['Year'] = df['Year'].astype(str)

# Sidebar filters
st.sidebar.header("Filters")
selected_years = st.sidebar.multiselect("Select Year(s):", sorted(df['Year'].unique()), default=df['Year'].unique())
selected_term = st.sidebar.selectbox("Select Term:", ['All', 'Spring', 'Fall'])

# Filter data
filtered_df = df[df['Year'].isin(selected_years)]
if selected_term != 'All':
    filtered_df = filtered_df[filtered_df['Term'] == selected_term]

# Create total applications, admissions and enrollments by term.  Use filters for year and term.
st.header("Key Performance Metrics (KPIs)")

col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", f"{filtered_df['Applications'].sum():,}")
col2.metric("Total Admitted", f"{filtered_df['Admitted'].sum():,}")
col3.metric("Total Enrolled", f"{filtered_df['Enrolled'].sum():,}")

st.write("Total Applications, Total Admitted, Total Enrolled:")

st.write("Aggregate the data for the years examined.  The user has the ability to filter by both Years and Term.  A single Year can be selected, or any combination of multiple years.  The user can also select all terms, or specify Spring or Fall.  The default filter is all Years and all Terms.")

st.write("Conclusion:")

st.write("Applicants, admitted and enrolled students have gradually increased over the ten years examined.")

# PLOT 1
# Create Retention Rate Trends Over Time
st.subheader("Retention Rate Over Time")
retention_trend = filtered_df.groupby('Year')['Retention_Rate_(%)'].mean().reset_index()
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=retention_trend, x='Year', y='Retention_Rate_(%)', marker='o', ax=ax1)
ax1.set_ylabel("Retention Rate (%)")
st.pyplot(fig1)

st.write("Retention Rate Over Time:")

st.write("The retention rate has fluctuated over the tens years examined.  Initially, and in the first year examed, the retention rate was at its lowest point, 85%.  In the four years following 2015, the retention rate began to trend upward.  However, another low point occurs in 2020 as the retention rate falls to 85%.  Again, in the four years following 2020, retention rates trend upward, but unlike in the period from 2015-2019, retention increases by 1% each year.  Filters apply to the plot.")

st.write("Conclusion:")

st.write("Retention rates have steadily increased in recent years, implying students prefer to remain enrolled in the university.")


# PLOT 2
# Create Student Satisfaction Scores Over the Years
st.subheader("Student Satisfaction Over Time")
satisfaction_trend = filtered_df.groupby('Year')['Student_Satisfaction_(%)'].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(data=satisfaction_trend, x='Year', y='Student_Satisfaction_(%)', palette="Blues_d", ax=ax2)
ax2.set_ylabel("Satisfaction (%)")
st.pyplot(fig2)

st.write("Student Satisfaction Over Time:")

st.write("The student satisfaction percent is trending upward, as there is a steady increase from 2015 to 2024.  Policies instituted by the university to retain students have been successful. Filters apply to the plot.")

st.write("Conclusion:")

st.write("The university should continue with its current programs/policies on student retention and consider new options to maintain or increase satisfaction.")

# PLOT 3
# Create Enrollment breakdown by department (Engineering, Business, Art & Science
st.subheader("Departmental Enrollment Breakdown")
dept_enroll = filtered_df[['Engineering_Enrolled', 'Business_Enrolled', 'Arts_Enrolled', 'Science_Enrolled']].sum()
dept_df = dept_enroll.reset_index()
dept_df.columns = ['Department', 'Enrolled']
dept_df['Department'] = dept_df['Department'].str.replace("_Enrolled", "")

fig3, ax3 = plt.subplots()
sns.barplot(data=dept_df, x='Department', y='Enrolled', palette='Set2', ax=ax3)
st.pyplot(fig3)

st.write("Department Enrollment:")

st.write("Total enrollment broken down by the four university departments: Engineering, Business, Arts & Science.  The default displays data for all years and all terms.  However, if we examine individual years, and one department is underperforming.  Engineering, Business and Arts have steadily increased enrollment over the ten year period.  Science had consistent enrollment for the first few years, and achieved a high of 130 students in each term of 2020.  Unfortunately, there has been a decline in enrollment in the following years, and the department has reached a low point of 100 students in each term of 2024.Filters apply to the plot.")

st.write("Conclusion:")

st.write("Student retention rate and student satisfaction rate could be driving department enrollment, as we can see a gradual increase for three out of the four departments.  Administration should examine why enrollment for Science has declined in the past five years.  There could be an issue with overall interest in the field by current and prospective students.  Administration could also examine the instructors, as well as other factors to determine student satisfaction.  The university could also prepare a specific survey for Science students to determine the root cause of enrollment decline. ")

# PLOT 4
# Create trends between departments, retention rates and satisfaction levels
st.subheader("Departmental Comparison: Retention vs. Satisfaction")

departments = ['Engineering', 'Business', 'Arts', 'Science']
dept_data = []

for dept in departments:
    enrolled_col = f"{dept}_Enrolled"
    
    if enrolled_col in filtered_df.columns:
        dept_enrolled = filtered_df[enrolled_col].sum()
        total_enrolled = filtered_df['Enrolled'].sum()
        
        weight = dept_enrolled / total_enrolled if total_enrolled else 0
        avg_retention = weight * filtered_df['Retention_Rate_(%)'].mean()
        avg_satisfaction = weight * filtered_df['Student_Satisfaction_(%)'].mean()
        
        dept_data.append({
            'Department': dept,
            'Avg_Retention': avg_retention,
            'Avg_Satisfaction': avg_satisfaction
        })

# Convert to DataFrame
dept_comp = pd.DataFrame(dept_data)

# Scatter plot
fig5, ax5 = plt.subplots(figsize=(6, 6))
sns.scatterplot(
    data=dept_comp, 
    x='Avg_Retention', 
    y='Avg_Satisfaction', 
    hue='Department', 
    s=150, 
    ax=ax5
)
ax5.set_xlabel("Retention Score (Weighted)")
ax5.set_ylabel("Satisfaction Score (Weighted)")
ax5.set_title("Retention vs. Satisfaction by Department")
st.pyplot(fig5)

st.write("Department Comparison - Retention vs. Satisfaction:")

st.write("Visualization compares weighted satisfactions scores vs. weighted retention scores for each department.  The default displays data for all years combined. Individual years can be examined, but the combined data provides a compelling narative.  We can determine that retention vs satisfaction for Engineering is much higher than any of the other departments.  Business and Arts are within 5% of each other, but 8 to 12% lower than Engineering.  The low point was achieved by the Science department, 14%.  Filters apply to the plot.")

st.write("Conclusion:")

st.write("The low point of 14% achieved by the Science department reinforces prior conclusions.  University administration should examine why the Science values are low, but also examine why Engineering is so much higher.  What is the Engineering department doing right, and can those policies/procedures then be applied to the Science department?")

# PLOT 5
# Create Comparison between Spring vs Fall term trends

df['Term'] = df['Term'].str.strip().str.capitalize()

# Sort years
df['Year'] = df['Year'].astype(int)
df = df.sort_values(by=['Year', 'Term'])

st.subheader("Spring vs Fall Enrollment Over Time")

# Group and aggregate
term_trend = df.groupby(['Year', 'Term'])['Enrolled'].sum().reset_index()

# Bar chart
fig4, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=term_trend, x='Year', y='Enrolled', hue='Term', ax=ax)

# Labels and formatting
ax.set_title("Enrollment Trends by Term")
ax.set_ylabel("Number of Enrolled Students")
ax.set_xlabel("Year")
ax.tick_params(axis='x', rotation=45)

# Display in Streamlit
st.pyplot(fig4)

st.write("Spring vs Fall Enrollment Over Time:")

st.write("Visualization displays the enrollment trends by term.  The bar chart displays data by year and term.  We can determine that in all years examined, enrollment is consistent between the Fall and Spring terms.  It should be noted that the filters do not apply to this plot.")

st.write("Conclusion:")

st.write("Enrollment has been steadily increasing over the ten year period.  The low point in 2015 with 600 students per term, and a high point in 2024 with 800 students per term.  The total number of students enrolled is increasing, but as we can determine from other plots, enrollment is not spread evenly across all departments.  ")

st.subheader("Overall conclusion:")

st.write("Overall retention rates and student satisfaction rates are increasing.")

st.write("Science may be underperforming compared to the other three departments.")

st.write("Enrollment is increasing, but Engineering appears to be driving the increase.")

st.write("Administration should review policies and procedures in an effort to increase rentition and enrollment.")
