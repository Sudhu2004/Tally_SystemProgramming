import streamlit as st
from pymongo import MongoClient

mongo_uri = "mongodb+srv://sudhrshan18:NaZFjUKdKlr2JrZF@cluster0.ma0bt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri)

db = client['organization_database']
collection = db['jobs']

st.title = ("MongoDB CRUD Operations with Streamlit")

st.header("Create Job")
create_title = st.text_input("Job Title", key = "create_title")
create_company = st.text_input("Company", key = "create_company")
create_location = st.text_input("Location", key = "create_location")
create_salary = st.number_input("Salary", min_value=0.0, key = "create_salary", format = "%.2f")

if st.button("Create Job"):

    job = {
        "title": create_title,
        "company": create_company,
        "location": create_location,
        "salary": create_salary
    }

    result = collection.insert_one(job)
    st.success(f"Job created with id : {result.inserted_id}")

st.header("Read Jobs")
if st.button("Read Jobs"):
    jobs = collection.find()
    for job in jobs:
        st.write(job)
    

st.header("Update Job")
update_title = st.text_input("Job Title", key = "update_title")
update_company = st.text_input("Company", key = "update_company")
update_location = st.text_input("Location", key = "update_location")
update_salary = st.number_input("Salary", min_value=0.0, key = "update_salary", format = "%.2f")

if st.button("Update Job"):
    query = {"title": update_title}
    update=  {"$set": {"company" : update_company, "location": update_location, "salary": update_salary}}
    result = collection.update_one(query, update)

    if result.matched_count > 0:
        st.success(f"Deleted {result.matched_count} document(s)")
    else:
        st.warning("No matching document found")

client.close()