# Sustainable Food Source Finder 🍃♻️🥗💚🌱

## Overview 

Welcome to Sustainable Food Finder! My name is Isabel Arvelo and I am a foodie that is passionate about sustainable food systems and mindful consumption. I built this application to help you discover local, sustainable food sources and understand seasonal eating patterns to make more food choices you can feel good about! This project aims to connect community members with fresh, local food while supporting the farmers who grow it. Not only does will help people access fresher, minimally processed foods, increasing awareness and accessibility of farmers' markets has the potential to strengthen local economies, reduce food miles, and preserve agricultural diversity. Most of the data will be sourced from the USDA Local Food Directory via their API. The directories used include:
* Farmers Market Directory: Markets with multiple farm vendors selling directly to consumers.
* CSA Directory: Farms or farm networks providing weekly deliveries of locally-grown products.
* On-Farm Market Directory: Markets run by a single farm selling products directly to consumers.



https://github.com/user-attachments/assets/ae92d1e9-8c6c-450c-8303-dbd91d738fd4



## Structure of Repo

* notebooks/
    * database_setup.ipynb: Contains code for creating the MongoDB databases
* mongo-data: Contains the data for the MongoDB database. It will not be populated until the user runs the database_setup.ipynb notebook.
* .streamlit
   * secrets.toml: Defines working directory for streamlit
* Home.py: landing page for the app - It contains the title, a brief description of the app, a choro map of the US, and a list of the food sources in Southeast United States. 
* pages/    
    * 1_📍_Geographic_Queries: Page for users to make queries based on location and products. 
    * 2_📥_API_Access.py: Page where users can query API directly for information across the entire United States
    * 3_🥗_Seasonal_Produce.py: Page to help users identify seasonal foods 
    * 4_👥_About.py: Page that contains information about the project, as well as resources for sustainable eating
* utils 
    * api_utils.py: Utility functions to query the API
    * map_utils.py: Utility functions to create the choropleth map
    * mongodb_utils.py: Utility functions to intialize and query the MongoDB database
    * query_utils.py: Utility functions to query the MongoDB database
* docker-compose.yml: Contains the instructions to build the Docker images, mount the volumes, and run the containers
* Dockerfile:  Contains the instructions to build the Python Docker image
* requirements.txt: List of all the packages needed to run the app
* us-states-by-area.csv: Data that contains the area of each state in the United States
* .env: Contains the environment variables. This file is not pushed to GitHub for security reasons.

## Replication 

To replicate this project, you will need to have Docker and Git installed on your machine. You will also need to create an account with the USDA Local Food Directory API and get an API key.

```
git clone https://github.com/isabelarvelo/sustainable-food-source-finder.git
cd sustainable-food-source-finder
```

Create a .env file in the root directory of the project and add the following environment variables:


USDA_API_KEY=Your_API_Key


Open a terminal in the root directory of the project and run the following commands:


```
docker-compose up
```

Once the containers are running, "localhost:8888" will open a jupyter login window in your browser. 


The password or token must match whatever is defined in the docker-compose file. For the current configuration, the token is 'your_secret_token'. Open the notebooks folder and run the database_setup.ipynb notebook. This will populate the MongoDB database with data in the mongo-data folder (Note that sometimes the API has connection issues. If this occurs, restart your kernel and try to run the cell again. If you are still experiencing issues, try getting a new API key.)  At this point, the user can run the Home.py file to open the Streamlit app. Open a new tab in the terminal and run the following command:

```
streamlit run Home.py
```

This will open the home page of the Streamlit app in your browser.

## Database Selected 
I chose MongoDB for this project because it is a NoSQL database that is well-suited for storing JSON-like documents. The data I am working with is in JSON format, so it made sense to use a database that could store the data in its original format. MongoDB can handle varied data structures, such as different types of fresh food sources (e.g., farmers' markets, CSAs, on-farm markets), each of which may have slightly different attributes. MongoDB's schema flexibility will allow me to add new fields as needed without needing major changes to the database structure. There is also built in support for geospatial data.  

## Schema
### sustainable_food_db
* Collection: food_sources
   * Stores information about local food sources including farmers markets, CSAs, and on-farm markets.

```
{
  directory_type: String,    // Type: farmers_market, csa, or onfarmmarket
  listing_id: String,        // Unique identifier
  listing_name: String,      // Name of the location
  brief_desc: String,        // Description of the location
  updatetime: Date,          // Last update timestamp

  contact: {
    name: String,
    email: String,
    phone: String
  },

  media: {
    website: String,
    facebook: String,
    twitter: String,
    instagram: String
  },

  location: {
    address: String,
    state: String,
    city: String,
    street: String,
    zipcode: String,
    coordinates: {
      type: "Point",
      coordinates: [Number, Number]  // [longitude, latitude]
    }
  },

  products: {
    available_items: [String],
    seasonal: Boolean
  },

  schedule: {
    season_range: {
      start_month: String,
      end_month: String
    }
  },

  metadata: {
    last_sync: Date,
    verified: Boolean,
    last_updated: Date
  }
}
```

**Indexes**: location.coordinates: 2dsphere (geospatial queries)

### us_geography
* Collection: states_area
   * Contains geographical information about US states.
     
```
{
  state: String,        // State name
  TotalArea: Number,    // Total area in square miles
  LandArea: Number,     // Land area in square miles
  WaterArea: Number,    // Water area in square miles
  densityMi: Number     // Population density per square mile
}
```

**Indexes**: state: 1 (ascending)

### food_database
Collection: seasonal_foods
Tracks seasonal availability of produce items.

```
{
  name: String,                 // Name of produce item
  seasons: [String],            // Array of seasons: [spring, summer, fall, winter]
  available_year_round: Boolean // Whether item is available year-round
}
```

**Indexes**:
* name: 1 (ascending)
* seasons: 1 (ascending)
* available_year_round: 1 (ascending)

Notes
* All coordinates are stored in GeoJSON format for compatibility with MongoDB's geospatial queries
* State names are stored in title case
* Timestamps are stored in UTC



## NoSQL DB Query Implementation 

1. Query Food Source by State 
2. Query Food Source by Source Type (e.g., farmers' markets, CSAs, on-farm markets)
3. Query Food Source by Products Available (e.g., Apples, Broccoli, Eggs)
4. Query Food Source by coordinates and radius 
5. Query density of Food Sources for a given state 
6. Query produce by season(s)
7. Query which season a specific product is in


## Data Sources 
* [USDA Local Food Directory](https://www.usdalocalfoodportal.com/)
* [Seasonal Food Guide](https://www.seasonalfoodguide.org/)
* [Fruits & Veggies](https://fruitsandveggies.org/stories/whats-in-season-all-year/)
* [Harvard Nutrition Source](https://nutritionsource.hsph.harvard.edu/2015/06/17/5-tips-for-sustainable-eating/)
* [World Population Review](https://worldpopulationreview.com/state-rankings/states-by-area)


## Gen AI Usage 

* I Used GenAI to help me: 
    * Brainstorm the best way to structure the repo
    * Format the Streamlit pages. The CSS code was created by iterating with Claude Sonnet 3.5. 
    * Create the choropleth map and display it successfully in Streamlit.
    * Debug API errors and MongoDB connection issues. 
    * Write documentation strings for functions
    * Make the code more modular with helper functions
    * Write more extensive and explanatory comments throughout my code
    * Proofread and edit the README file and text in the Streamlit app.
* I gave GenAI the project requirements outlined in the class slides and the project rubric and asked it to grade me across the specified criteria.

## Other Resources Used

The API was returning error codes, but I was able to resolve them by including headers in the request. I found this solution on the GithHub for [APSC-5984](https://github.com/Niche-Lab/APSC-5984-ADS/tree/main/labs/lab_07) SS: Agriculture Data Science taught at Virginia Tech.

## Contact 

If you have any questions or feedback, please reach out to me at isabel.c.arvelo@vanderbilt.edu.
