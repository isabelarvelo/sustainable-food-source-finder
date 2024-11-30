# Sustainable Food Finder

## Structure of Repo
* notebooks
    * development.ipynb: Contains code for creating the MongoDB databases
* Home.py
    * landing page for the app - It contains the title, a brief description of the app, a choropleth map of the US, and a list of the food sources in Southeast United States. 
* pages    
    * 1_📍_Geographic_Queries: Page for users to make queries based on location and products. 
    * 2_📥_API_Access.py: Page where users can query API directly for information across the entire United States
    * 3_🥗_Seasonal_Produce.py: Page to help users identify seasonal foods 
    * 4_👥_About.py: Page that contains information about the project, as well as resources for sustainable eating
* utils 
    * api_utils.py: Utility functions to query the API
    * map_utils.py: Utility functions to create the choropleth map
    * mongodb_utils.py: Utility functions to intialize and query the MongoDB database
    * query_utils.py: Utility functions to query the MongoDB database
* .env: Contains the environment variables. This file is not pushed to GitHub for security reasons, but it should contain USDA_API_KEY=your_api_key
* docker-compose.yml: Contains the instructions to build the Docker images, mount the volumes, and run the containers
* Dockerfile:  Contains the instructions to build the Python Docker image
* requirements.txt: List of all the packages needed to run the app
* us-states-by-area.csv: Data that contains the area of each state in the United States
* .streamlit
    * secrets.toml: Defines working directory for streamlit
* mongo-data: Contains the data for the MongoDB database

## How to Run the App

```
docker-compose up
```

```
streamlit run Home.py
```

## Data Sources 


## Gen AI Usage 

* I Used GenAI to help me 
    * format the Streamlit pages. Much of the CSS code was created by iterating with Claude Sonnet 3.5. 
    * create the choropleth map and display it successfully in Streamlit.
