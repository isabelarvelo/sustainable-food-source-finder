import streamlit as st

def show_about_page():
    st.title("About Sustainable Food Finder")
    
    st.write("""
    Welcome to Sustainable Food Finder! My name is Isabel Arvelo and I am a foodie that is passionate about sustainable food 
    systems and mindful consumption. I built this application to help you discover local, sustainable food sources 
    and understand seasonal eating patterns to make more food choices you can make feel good about! 
    """)
    
    # Benefits Section
    st.header("Benefits of Sustainable & Local Eating")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Economic Benefits")
        st.markdown("""
        - **Reduced Food Costs**: Seasonal, direct-to-consumer purchases are typically less expensive
        - **Supports Local Economy**: Creates local jobs and stimulates economic growth
        - **Helps Farmers**: Direct sales provide better profits for farmers
        - **Lower Operating Costs**: Reduces transportation, handling, and storage expenses
        """)
        
        st.subheader("Community Benefits")
        st.markdown("""
        - **Builds Connections**: Creates meaningful farmer-consumer relationships
        - **Community Engagement**: Opportunities through farmers' markets and CSAs
        - **Improved Food Skills**: Enhanced cooking and food preparation knowledge
        - **Cultural Preservation**: Maintains local food traditions and practices
        """)
    
    with col2:
        st.subheader("Environmental Impact")
        st.markdown("""
        - **Reduced Carbon Footprint**: Less transportation and storage needs
        - **Resource Conservation**: Lower pressure on land and water resources
        - **Biodiversity**: Promotes ecological diversity and wildlife
        - **Less Food Waste**: Minimizes losses from transport and storage
        """)
        
        st.subheader("Global Contributions")
        st.markdown("""
        - **Food Security**: Improves local food availability
        - **Climate Action**: Reduces greenhouse gas emissions
        - **Sustainability**: Promotes responsible resource use
        - **Health**: Supports better nutrition through fresh, seasonal foods
        """)
    
    # Tips Section
    st.header("Tips for Sustainable Eating")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        ### Planning & Purchasing
        - Plan meals ahead to reduce waste
        - Buy seasonal produce
        - Shop at local farmers' markets
        - Join Community Supported Agriculture (CSA) programs
        """)
    
    with tips_col2:
        st.markdown("""
        ### Dietary Choices
        - Prioritize plant-based foods
        - Minimize meat consumption
        - Choose diverse food sources
        - Focus on whole, unprocessed foods
        """)
    
    # Resources Section
    st.header("Resources")
    
    st.markdown("""
    ### Featured Companies
    - [Misfits Market](https://www.misfitsmarket.com/): Subscription-based grocery delivery that sources sustainably with a focus on reducing food waste
    - [Too Good To Go](https://toogoodtogo.com/): Saves surplus food from restaurants and stores     
    
    ### Data Sources
    - [USDA Local Food Directory](https://www.usdalocalfoodportal.com/)
    - [Seasonal Food Guide](https://www.seasonalfoodguide.org/)
    - [Foundation for Fresh Produce](https://fruitsandveggies.org/stories/whats-in-season-all-year/)
    - [Harvard Nutrition Source](https://nutritionsource.hsph.harvard.edu/2015/06/17/5-tips-for-sustainable-eating/)
    """)

    st.header("Restaurant Recommendations")
    
    st.markdown("""
    ### Nashville, TN           
    - [Avo](https://www.eatavo.com/): Midtown
    - [Two Hands](https://www.twohandshospitality.com/location/two-hands-nashville/):  The Gulch    
    - [Miel](https://www.mielrestaurant.com/): West Nashville              
    """
)
    
    
    # Methodology Section
    st.header("Methodology")
    st.write("""
    Our application combines data from multiple authoritative sources to provide accurate, up-to-date 
    information about local food sources and seasonal availability. We regularly update our database 
    to ensure the most current information about local farmers' markets, CSAs, and food sources.
    
    The seasonal produce data is compiled from agricultural databases and cross-referenced with 
    local growing seasons to provide accurate availability information.
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    *Sustainable Food Finder is committed to promoting environmental sustainability, supporting local 
    communities, and making sustainable eating accessible to everyone.*
    """)

if __name__ == "__main__":
    show_about_page()