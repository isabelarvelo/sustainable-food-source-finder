import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils import init_connection, create_map, get_food_sources

st.markdown("""
    <style>
        /* Custom styles for the main title */
        .main-title {
            color: #2c3e50;
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 3px solid #27ae60;
        }
        
        /* Enhance the description text */
        .app-description {
            font-size: 1.1rem;
            line-height: 1.6;
            color: #34495e;
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        /* Style the source details cards */
        .source-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        
        /* Style section headers */
        .section-header {
            color: #2c3e50;
            font-size: 1.8rem;
            font-weight: 600;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #3498db;
        }
        
        /* Style the filters section */
        .sidebar .stSelectbox, .sidebar .stMultiSelect {
            background-color: white;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
        
        /* Enhance map container */
        .map-container {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 1rem 0;
            padding: 1rem;
            background-color: white;
        }
        
        /* Style expandable cards */
        .streamlit-expanderHeader {
            background-color: #f8f9fa;
            border-radius: 5px;
            padding: 0.5rem;
        }
        
        /* Style contact information */
        .contact-info {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin-top: 0.5rem;
        }
        
        /* Style product tags */
        .product-tag {
            display: inline-block;
            background-color: #e8f6f3;
            color: #27ae60;
            padding: 0.3rem 0.6rem;
            border-radius: 15px;
            margin: 0.2rem;
            font-size: 0.9rem;
        }
        
        /* Style selected product tags */
        .product-tag-selected {
            background-color: #27ae60;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

def get_all_available_products(data):
    """Extract unique product items from all listings."""
    products = set()
    for item in data:
        if item.get('products', {}).get('available_items'):
            products.update(item['products']['available_items'])
    return sorted(list(products))

def main():
    # Title with custom styling
    st.markdown('<h1 class="main-title">Sustainable Food Finder</h1>', unsafe_allow_html=True)
    
    # Description with custom styling
    st.markdown(
        '<div class="app-description">'
        'We’re here to help you discover sustainable and fresh food sources to support your best self! '
        'Currently, the project is focused on the Southeastern United States, '
        'but if you’d like to explore other regions, please visit the API Access Page to find fresh food anywhere in the United States.'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Initialize connection and get data
    client = init_connection()
    all_data = get_food_sources(client)
    
    # Get unique values for filters
    states = sorted(list(set(item['location']['state'] 
                           for item in all_data 
                           if item.get('location', {}).get('state'))))
    source_types = sorted(list(set(item['directory_type'] 
                               for item in all_data 
                               if item.get('directory_type'))))
    available_products = get_all_available_products(all_data)
    
    # Sidebar with enhanced styling
    with st.sidebar:
        st.markdown('<h2 style="color: #2c3e50;">Filters</h2>', unsafe_allow_html=True)
        
        selected_state = st.selectbox(
            "Select State",
            ["All"] + states,
            key="state_select"
        )
        
        selected_type = st.selectbox(
            "Select Source Type",
            ["All"] + source_types,
            key="type_select"
        )
        
        selected_products = st.multiselect(
            "Select Products",
            options=available_products,
            help="Select one or more products. Sources must have ALL selected products to be shown.",
            key="product_select"
        )
        
        # Summary section with enhanced styling
        st.markdown('<h3 style="color: #2c3e50; margin-top: 2rem;">Summary</h3>', unsafe_allow_html=True)
        
    # Apply filters (same as before)
    filtered_data = filter_data(all_data, selected_state, selected_type, selected_products)
    
    # Display summary with enhanced styling
    st.sidebar.markdown(f'<div style="font-size: 1.2rem; color: #27ae60;"><strong>{len(filtered_data)}</strong> Sources Found</div>', unsafe_allow_html=True)
    
    # Create and display map with container styling
    st.markdown('<div>', unsafe_allow_html=True)
    fig = create_map(filtered_data)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
    '<div class="app-description">'
    'Use the filters on the left to refine your search. '
    'More specific queries can be made in the Geographic Queries page, where you can find food sources by location, radius, and product availability.'
    '</div>',
    unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Display food sources with enhanced styling
    if filtered_data:
        st.markdown('<h2 class="section-header">Food Source Details</h2>', unsafe_allow_html=True)
        
        for item in filtered_data:
            with st.expander(f"{item['listing_name']} ({item['location']['city']}, {item['location']['state']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📍 Location Details**")
                    st.markdown(f"Address: {item['location']['address']}")
                    st.markdown(f"Type: {item['directory_type'].title()}")
                    
                    if any(item['contact'].values()):

                        st.markdown("**📞 Contact Information**")
                        if item['contact']['name']:
                            st.markdown(f"Name: {item['contact']['name']}")
                        if item['contact']['email']:
                            st.markdown(f"Email: {item['contact']['email']}")
                        if item['contact']['phone']:
                            st.markdown(f"Phone: {item['contact']['phone']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    if item['products']['available_items']:
                        st.markdown("**🛒 Available Products**")
                        products_html = []
                        for product in item['products']['available_items']:
                            class_name = "product-tag product-tag-selected" if product in selected_products else "product-tag"
                            products_html.append(f'<span class="{class_name}">{product}</span>')
                        st.markdown(f'<div style="margin-top: 0.5rem;">{"".join(products_html)}</div>', unsafe_allow_html=True)
                    
                    if any(item['media'].values()):
                        st.markdown("**🌐 Social Media**")
                        for platform, url in item['media'].items():
                            if url:
                                st.markdown(f"[{platform.title()}]({url})")
    else:
        st.info("No food sources found matching your criteria. Try adjusting your filters.")

def filter_data(data, state, source_type, products):
    filtered = data.copy()
    
    if state != "All":
        filtered = [item for item in filtered 
                   if item.get('location', {}).get('state') == state]
    
    if source_type != "All":
        filtered = [item for item in filtered 
                   if item.get('directory_type') == source_type]
    
    if products:
        filtered = [item for item in filtered 
                   if (item.get('products', {}).get('available_items') and 
                       all(product in item['products']['available_items'] 
                           for product in products))]
    
    return filtered

if __name__ == "__main__":
    main()