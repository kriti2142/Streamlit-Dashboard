from email.errors import ObsoleteHeaderDefect
from itertools import count
from re import X
from sqlalchemy import false
import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from PIL import Image
import turtle

img=Image.open("download.jpg")
st.set_page_config(layout='wide', page_title='iHRMS Dashboard',page_icon=img)
st.sidebar.markdown("Welcome to iHRMS Dashboard!")

col1 , col2 , col3 =st.columns(3)
with col1:
    st.subheader("iHRMS DASHBOARD")
    st.markdown("Integrated Human Resource Management System is developed by NIC Punjab for looking into various aspects of the manpower planning, easy availability of information to the government, employees and other such stakeholders. The iHRMS application is under implementation in all Administrative Departments throughout the state of Punjab down to the field level offices.")

with col3:
    img = Image.open("logo.jpg")
    st.image(img, caption='Integrated Human Resourse Management',width=120)


@st.cache(allow_output_mutation=True)
def get_data():
    data=pd.read_csv("EmpdatasetKriti.csv")
    return data
df = get_data()

df.replace({"F":"Female"},inplace=True)
df.replace({"M":"Male"},inplace=True)
df.replace({"T":"Others"},inplace=True)
df.replace({"N":"Others"},inplace=True)

Total_no_of_employees=len(df)
total_districts=len(pd.unique(df["District"]))
total_departments=len(pd.unique(df["Admin Department"]))
total_posting_departments=len(pd.unique(df["Posting Department"]))

#Gender=len(pd.unique(df["Gender"]))
female=sum(df["Gender"]=="Female")
male=sum(df["Gender"]=="Male") 
others=sum(df['Gender']=="Others")

#total_service_groups=len(pd.unique(df["Service Group"]))
group_A=sum(df['Service Group']=="Group A")
group_B=sum(df['Service Group']=="Group B")
group_C=sum(df['Service Group']=="Group C")
group_D=sum(df['Service Group']=="Group D")


district =df.groupby(['District']).size().reset_index(name='Employees')
admin_department =df.groupby(['Admin Department']).size().reset_index(name='Employees')
gender =df.groupby(['Gender']).size().reset_index(name='Employees')
service_group =df.groupby(['Service Group']).size().reset_index(name='Employees')
age=df.groupby(['Age']).size().reset_index(name='Employees')
employee_type=df.groupby(['Employee Type']).size().reset_index(name='Employees')
category=df.groupby(['Category']).size().reset_index(name='Employees')

col1 , col2 , col3 , col4, col5, col6   = st.columns(6)

col1.metric('#Employees',Total_no_of_employees)
col2.metric('Districts',total_districts)
col3.metric('Admin Departments',total_departments)
col4.metric('Females',female)
col5.metric("Males",male)
col6.metric("Others",others)

col1 , col2 , col3 , col4,col5,col6  = st.columns(6)

col1.metric("Posting Department",total_posting_departments)
col2.metric("Group A",group_A)
col3.metric("Group B",group_B)
col4.metric("Group C",group_C)
col5.metric("Group D",group_D)

query=df.groupby(["District","Admin Department","Gender","Service Group"], as_index=False,sort=false)["Total"].aggregate('sum')
st.info("#Summarized View")
st.write(query)

st.sidebar.header("Select the filters :-")
if st.sidebar.checkbox("District Filter"):
    district_select = st.sidebar.multiselect("Select the District :",pd.unique(district['District']))
    district = district[district['District'].isin(district_select)]


if st.sidebar.checkbox("Department Filter"):
    department_select = st.sidebar.multiselect("Select the Department :",pd.unique(admin_department['Admin Department']))
    admin_department = admin_department[admin_department['Admin Department'].isin(department_select)]

if st.sidebar.checkbox("Gender Filter"):
    gender_select = st.sidebar.multiselect("Select the Gender :",pd.unique(gender['Gender']))
    gender = gender[gender['Gender'].isin(gender_select)]

if st.sidebar.checkbox("Service Group Filter"):
    group_select=st.sidebar.multiselect("Select The Group :",pd.unique(service_group['Service Group']))
    service_group=service_group[service_group['Service Group'].isin(group_select)]

if st.sidebar.checkbox("Age Filter"):
    age_select = st.sidebar.select_slider("Select your age :",options =pd.unique(age['Age']))
    age=age[age['Age']==(age_select)] 

if st.sidebar.checkbox("Employee Type Filter"):
    employee_select = st.sidebar.multiselect("Select the Employee Type :",pd.unique( employee_type['Employee Type']))
    employee_type = employee_type[employee_type['Employee Type'].isin(employee_select)]

if st.sidebar.checkbox("Category Filter"):
    category_select = st.sidebar.multiselect("Select the Category :",pd.unique(category['Category']))
    category = category[category['Category'].isin(category_select)]



col1, col2  =st.columns(2)

with col1:
    st.info("Visual Representation ")
    fig = px.bar(district, x="District", y="Employees", color="Employees", title="")
    st.plotly_chart(fig, use_container_width=True)
    
with col2:
    st.warning('Districts')
    st.write(district)

col1, col2  =st.columns(2)

with col1:
    st.success("Visual Representation" )
    fig = px.bar(admin_department, x="Employees", y="Admin Department", color="Employees", title="", orientation='h')
    st.plotly_chart(fig , use_container_width=True)

with col2:
    st.info("Admin department")
    st.write(admin_department)

col3 , col4 = st.columns(2)  

with col3:
    st.success("Visual Representation")
    fig = px.bar(gender, x="Gender", y="Employees",color="Employees", title="")
    st.plotly_chart(fig ,use_container_width=True)


with col4:
    st.error("Gender")
    st.write(gender)

col1, col2  =st.columns(2) 

with col1:
    st.success("Visual Representation")
    fig = px.bar(service_group, x="Service Group", y="Employees",color="Employees", title="")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.warning("Service Group")
    st.write(service_group)     

col1, col2  =st.columns(2) 
with col1:
    st.info("Visual Representation")
    fig = px.bar(age, x="Age", y="Employees",color="Employees", title="")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.warning("Age")
    st.write(age)     

col1, col2  =st.columns(2) 
with col1:
    st.info("Visual Representation")
    fig = px.bar(employee_type, x="Employee Type", y="Employees",color="Employees", title="")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.warning("Employee Type")
    st.write(employee_type) 

col1, col2  =st.columns(2) 
with col1:
    st.info("Visual Representation")
    fig = px.bar(category, x="Category", y="Employees",color="Employees", title="")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.warning("Category")
    st.write(category) 




#st.info(""+district_select   +department_select   +gender_select   +group_select)
    #st.write(query)
    #col1 , col2 =st.columns(2)
    #with col1:
    #    st.warning("Visualization for Filters being Applied:")
    #    fig = px.bar(query, x="Total", y=["District","Admin Department","Gender","Service Group"], title="")
    #   st.plotly_chart(fig, use_container_width=True)
    #with col2:
    #   st.error("Visualization for Filters being Applied:")
    #    fig = px.pie(
    #   hole = 0.8,
    #   labels = query,
    #   names = query.keys(),)
    #   st.plotly_chart(fig, use_container_width=True)

#Group by :
#gk = df.groupby('Parent Department')
#st.write(gk.first())
#st.write(gk.get_group('CONTROLLER  PRINTING & STATIONERY'))
#gkk=df.groupby(['Parent Department','Age'])
#st.write(gkk.first())
#district_group = df.groupby('District')  
#    
#st.text('Your age is : {}'.format(level))

