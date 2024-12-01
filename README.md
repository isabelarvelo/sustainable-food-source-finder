
## Structure of Repo
* .streamlit
    * secrets.toml: Defines working directory for streamlit
* mongo-data: Contains the data for the MongoDB database. It is not populated until the user runs the development.ipynb notebook
* notebooks
    * development.ipynb: Contains code for creating the MongoDB databases
* Home.py
    * landing page for the app - It contains the title, a brief description of the app, a choro map of the US, and a list of the food sources in Southeast United States. 
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
* .env: Contains the environment variables. This file is not pushed to GitHub for security reasons.
* docker-compose.yml: Contains the instructions to build the Docker images, mount the volumes, and run the containers
* Dockerfile:  Contains the instructions to build the Python Docker image
* requirements.txt: List of all the packages needed to run the app
* us-states-by-area.csv: Data that contains the area of each state in the United States

## Replication 

Open a terminal in the root directory of the project and run the following commands:

```
docker-compose build --no-cache
```

```
docker-compose up
```

"localhost:8888" will open a jupyer login window in your browser. 


The password or token must match whatever is defined in the docker-compose file. For the current configuration, the token is 'your_secret_token'. Open the notebooks folder and run the database_setup.ipynb notebook. This will populate the MongoDB database with the data in the mongo-data folder (Note that sometimes the API has connection issues. If this occurs, restart your kernel and try to run the cell again.)  At this point, the user can run the Home.py file to open the Streamlit app. Open a new tab in the terminal and run the following command:

```
streamlit run Home.py
```

This will open the home page of the Streamlit app in your browser.

## Data Sources 
* [USDA Local Food Directory](https://www.usdalocalfoodportal.com/)
* [Seasonal Food Guide](https://www.seasonalfoodguide.org/)
* [Fruits & Veggies](https://fruitsandveggies.org/stories/whats-in-season-all-year/)
* [Harvard Nutrition Source](https://nutritionsource.hsph.harvard.edu/2015/06/17/5-tips-for-sustainable-eating/)


## Query Implementation 
    * Home 
        * Query by State 
        * Query by Source Type (e.g., farmers' markets, CSAs, on-farm markets)
        * Query by Product (e.g., Apples, Broccoli, Eggs)
    * 1_📍_Geographic_Queries: 
        * Query by coordinates and radius 
        * Query source density for a given state 
    * 3_🥗_Seasonal_Produce.py: Page to help users identify seasonal foods 
        * Query seasonal produce by season 
        * Query which season a product is in

## Database Selected 
I chose MongoDB for this project because it is a NoSQL database that is well-suited for storing JSON-like documents. The data I am working with is in JSON format, so it made sense to use a database that could store the data in its original format. MongoDB can handle varied data structures, such as different types of fresh food sources (e.g., farmers' markets, CSAs, on-farm markets), each of which may have slightly different attributes. MongoDB's schema flexibility will allow me to add new fields as needed without needing major changes to the database structure. There is also built in support for geospatial data.  


## Gen AI Usage 

* I Used GenAI to help me 
    * format the Streamlit pages. Much of the CSS code was created by iterating with Claude Sonnet 3.5. 
    * create the choropleth map and display it successfully in Streamlit.

* I gave GenAI the project requirements outlined in the class slides and the project rubric and asked it to grade me across thoe criteria. 

## Other Resources Used

* The API was returning error codes, but I was able to resolve them by including headers in the request. I found this solution on the GithHub for [APSC-5984](https://github.com/Niche-Lab/APSC-5984-ADS/tree/main/labs/lab_07) SS: Agriculture Data Science taught at Virginia Tech.

