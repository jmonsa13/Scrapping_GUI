# Download python from docker hub
FROM python:3.7

# Declaring working directory in our container
WORKDIR /app

# Copy all relevant files to our working dir
COPY requirements.txt ./requirements.txt

# Install all requrements for our app
RUN pip3 install -r requirements.txt

# Copy source files to $WORKDIR
COPY . /app

# Expose container port to outside host
EXPOSE 8501

# Run the application
ENTRYPOINT [ "streamlit", "run" ]
CMD [ "Home_Dashboard_Pricing.py" ]