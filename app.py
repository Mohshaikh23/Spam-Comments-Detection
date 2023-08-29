import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
import pickle
import streamlit as st

# Load and preprocess the data
data = pd.read_csv("Youtube01-Psy.csv")
data["CLASS"] = data["CLASS"].map({0: "Not Spam", 1: "Spam Comment"})
data = data[["CONTENT", "CLASS"]]

# Train the classification model
x = np.array(data["CONTENT"])
y = np.array(data["CLASS"])

cv = CountVectorizer()
x = cv.fit_transform(x)
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

model = BernoulliNB()
model.fit(xtrain, ytrain)
print("Model accuracy:", model.score(xtest, ytest))

# Save the CountVectorizer
with open('countvectorizer.pkl', 'wb') as f:
    pickle.dump(cv, f)

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Create Streamlit app
st.title("Spam Classifier App")

# Load the CountVectorizer
with open('countvectorizer.pkl', 'rb') as f:
    cv = pickle.load(f)

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Get user input
user_input = st.text_area("Enter a text message:")

if st.button("Classify"):
    # Preprocess user input using the CountVectorizer
    data = cv.transform([user_input]).toarray()
    prediction = model.predict(data)
    
    if prediction[0] == "Not Spam":
        st.success("This is not spam!")
    else:
        st.error("This is spam!")
