# Libraries to be imported 
import streamlit as st
import json
import os
from serpapi import GoogleSearch 
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.google import Gemini
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd

# Adding the API Keys
SERPAPI_KEY = "your_serpapi_key_here"
GOOGLE_API_KEY = "your_gemini_api_key_here"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Helper Class for URL Buttons
class URLButton:
    def __init__(self, url: str, text: str, background_color: str = "#007bff"):
        self.url = url
        self.text = text
        self.background_color = background_color

    def _build_html(self) -> str:
        return f"""
        <a href="{self.url}" target="_blank" style="
            display: inline-block;
            padding: 0.5em 1em;
            color: white;
            background-color: {self.background_color};
            border-radius: 3px;
            text-decoration: none;
            font-weight: bold;
            border: none;
            cursor: pointer;
        ">{self.text}</a>
        """

    def show(self):
        st.markdown(self._build_html(), unsafe_allow_html=True)

# Airport Code Mapping Dictionary
def get_airport_code(city_name):
    airport_mapping = {
        # Asia
        "Mumbai": "BOM",
        "Delhi": "DEL",
        "Bangkok": "BKK",
        "Singapore": "SIN",
        "Tokyo": "HND",
        "Hong Kong": "HKG",
        "Beijing": "PEK",
        "Shanghai": "PVG",
        "Seoul": "ICN",
        "Dubai": "DXB",
        "Abu Dhabi": "AUH",
        "Kuala Lumpur": "KUL",
        "Jakarta": "CGK",
        "Manila": "MNL",
        "Ho Chi Minh City": "SGN",
        
        # Europe
        "London": "LHR",
        "Paris": "CDG",
        "Amsterdam": "AMS",
        "Rome": "FCO",
        "Madrid": "MAD",
        "Barcelona": "BCN",
        "Frankfurt": "FRA",
        "Munich": "MUC",
        "Zurich": "ZRH",
        "Vienna": "VIE",
        "Brussels": "BRU",
        "Copenhagen": "CPH",
        "Stockholm": "ARN",
        "Athens": "ATH",
        "Istanbul": "IST",
        
        # North America
        "New York": "JFK",
        "Los Angeles": "LAX",
        "Chicago": "ORD",
        "San Francisco": "SFO",
        "Miami": "MIA",
        "Las Vegas": "LAS",
        "Toronto": "YYZ",
        "Vancouver": "YVR",
        "Montreal": "YUL",
        "Mexico City": "MEX",
        "Cancun": "CUN",
        
        # South America
        "Sao Paulo": "GRU",
        "Rio de Janeiro": "GIG",
        "Buenos Aires": "EZE",
        "Lima": "LIM",
        "Santiago": "SCL",
        "Bogota": "BOG",
        
        # Oceania
        "Sydney": "SYD",
        "Melbourne": "MEL",
        "Brisbane": "BNE",
        "Auckland": "AKL",
        "Wellington": "WLG",
        
        # Africa
        "Cairo": "CAI",
        "Cape Town": "CPT",
        "Johannesburg": "JNB",
        "Nairobi": "NBO",
        "Casablanca": "CMN"
    }
    return airport_mapping.get(city_name.strip().title(), None)

# Set up Streamlit UI
st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")

# Styling
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #ff5733;
            margin-bottom: 20px;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #555;
            margin-bottom: 30px;
        }
        .flight-details {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .price-tag {
            font-size: 24px;
            font-weight: bold;
            color: #2ecc71;
        }
        .flight-time {
            font-size: 18px;
            font-weight: bold;
            color: #34495e;
        }
        .airport-code {
            font-weight: bold;
            color: #2c3e50;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.markdown('<h1 class="title">✈️ AI-Powered Travel Planner</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plan your dream trip with AI! Get personalized recommendations for flights, hotels, and activities.</p>', unsafe_allow_html=True)

# User Inputs Section
st.markdown("### 🌍 Where are you headed?")
col1, col2 = st.columns(2)

with col1:
    source_city = st.text_input("🛫 Departure City:", "Mumbai")
    source_country = st.text_input("Departure Country:", "India")
    source_airport = get_airport_code(source_city)
    if source_airport:
        st.success(f"✓ Airport found: {source_airport}")
    else:
        st.warning("⚠️ Could not find airport code for this city. Please check the city name.")

with col2:
    destination_city = st.text_input("🛬 Destination City:", "London")
    destination_country = st.text_input("Destination Country:", "United Kingdom")
    destination_airport = get_airport_code(destination_city)
    if destination_airport:
        st.success(f"✓ Airport found: {destination_airport}")
    else:
        st.warning("⚠️ Could not find airport code for this city. Please check the city name.")

# Trip Planning Inputs
st.markdown("### 📅 Plan Your Adventure")
num_days = st.slider("🕒 Trip Duration (days):", 1, 14, 5)
travel_theme = st.selectbox(
    "🎭 Select Your Travel Theme:",
    ["💑 Couple Getaway", "👨‍👩‍👧‍👦 Family Vacation", "🏔️ Adventure Trip", "🧳 Solo Exploration"]
)

activity_preferences = st.text_area(
    "🌍 What activities do you enjoy?",
    "Relaxing on the beach, exploring historical sites"
)

col3, col4 = st.columns(2)
with col3:
    departure_date = st.date_input("Departure Date")
with col4:
    return_date = st.date_input("Return Date")

# Sidebar Setup
st.sidebar.title("🌎 Travel Assistant")
st.sidebar.subheader("Personalize Your Trip")

# Travel Preferences
budget = st.sidebar.radio("💰 Budget Preference:", ["Economy", "Standard", "Luxury"])
flight_class = st.sidebar.radio("✈️ Flight Class:", ["Economy", "Business", "First Class"])
hotel_rating = st.sidebar.selectbox("🏨 Preferred Hotel Rating:", ["Any", "3⭐", "4⭐", "5⭐"])

# Packing Checklist
st.sidebar.subheader("🎒 Packing Checklist")
packing_list = {
    "👕 Clothes": True,
    "🩴 Comfortable Footwear": True,
    "🕶️ Sunglasses & Sunscreen": False,
    "📖 Travel Guidebook": False,
    "💊 Medications & First-Aid": True,
    "🔌 Travel Adapters": False,
    "📱 Electronics & Chargers": True,
    "🛂 Travel Documents": True
}
for item, checked in packing_list.items():
    st.sidebar.checkbox(item, value=checked)

# Travel Essentials
st.sidebar.subheader("🛂 Travel Essentials")
visa_required = st.sidebar.checkbox("🛃 Check Visa Requirements")
travel_insurance = st.sidebar.checkbox("🛡️ Get Travel Insurance")
currency_converter = st.sidebar.checkbox("💱 Currency Exchange Rates")

# Helper Functions
def format_datetime(iso_string):
    try:
        dt = datetime.strptime(iso_string, "%Y-%m-%d %H:%M")
        return dt.strftime("%b-%d, %Y | %I:%M %p")
    except:
        return "N/A"

# Flight Functions
def fetch_flights(source_city, destination_city, departure_date, return_date):
    try:
        source_airport = get_airport_code(source_city)
        destination_airport = get_airport_code(destination_city)
        
        if not source_airport or not destination_airport:
            st.error(f"Could not find airport codes for one or both cities. Please check city names.")
            return None

        params = {
            "engine": "google_flights",
            "departure_id": source_airport,
            "arrival_id": destination_airport,
            "outbound_date": str(departure_date),
            "return_date": str(return_date),
            "currency": "INR",
            "hl": "en",
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get('best_flights', [])
            
    except Exception as e:
        st.error(f"Error fetching flights: {str(e)}")
        return None

def extract_cheapest_flights(flight_data):
    best_flights = flight_data if isinstance(flight_data, list) else []
    sorted_flights = sorted(best_flights, key=lambda x: x.get("price", float("inf")))[:3]
    return sorted_flights

def display_flight_card(flight, source_city, destination_city, departure_date):
    airline_logo = flight.get("airline_logo", "")
    airline_name = flight.get("airline", "Unknown Airline")
    price = flight.get("price", "Not Available")
    total_duration = flight.get("total_duration", "N/A")
    
    flights_info = flight.get("flights", [{}])
    departure = flights_info[0].get("departure_airport", {})
    arrival = flights_info[-1].get("arrival_airport", {})
    
    departure_time = format_datetime(departure.get("time", "N/A"))
    arrival_time = format_datetime(arrival.get("time", "N/A"))
    
    source_airport = get_airport_code(source_city)
    destination_airport = get_airport_code(destination_city)
    formatted_date = departure_date.strftime("%Y-%m-%d")

    # Create booking link for Google Flights only
    booking_link = {
        "Google Flights": {
            "url": f"https://www.google.com/travel/flights?hl=en&q=Flights%20from%20{source_airport}%20to%20{destination_airport}%20on%20{formatted_date}",
            "color": "#4285f4",
            "icon": "🔍"
        }
    }

    st.markdown(
        f"""
        <div style="
            border: 2px solid #ddd; 
            border-radius: 15px; 
            padding: 20px; 
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            background-color: white;
            margin-bottom: 20px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="flex: 1; text-align: center;">
                    <img src="{airline_logo}" width="80" alt="Airline Logo" style="margin-bottom: 10px;"/>
                    <h3 style="margin: 0; color: #2c3e50;">{airline_name}</h3>
                </div>
                <div style="flex: 2; display: flex; justify-content: space-around; align-items: center;">
                    <div style="text-align: center;">
                        <p style="font-size: 24px; font-weight: bold; margin: 0; color: #34495e;">{departure_time}</p>
                        <p style="margin: 0; color: #7f8c8d;">{source_airport}</p>
                    </div>
                    <div style="text-align: center;">
                        <p style="margin: 0; color: #7f8c8d;">✈️</p>
                        <p style="margin: 0; color: #7f8c8d;">{total_duration} min</p>
                    </div>
                    <div style="text-align: center;">
                        <p style="font-size: 24px; font-weight: bold; margin: 0; color: #34495e;">{arrival_time}</p>
                        <p style="margin: 0; color: #7f8c8d;">{destination_airport}</p>
                    </div>
                </div>
                <div style="flex: 1; text-align: center;">
                    <h2 style="color: #27ae60; margin: 0;">💰 {price}</h2>
                </div>
            </div>
            <div style="border-top: 1px solid #eee; padding-top: 15px; margin-top: 15px;">
                <div style="display: flex; justify-content: center; gap: 15px;">
        """, 
        unsafe_allow_html=True
    )

    # Create column for Google Flights booking button
    for platform, link_info in booking_link.items():
        st.markdown(
            f"""
            <a href="{link_info['url']}" target="_blank" style="
                display: inline-block;
                padding: 8px 16px;
                background-color: {link_info['color']};
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                transition: opacity 0.2s;
                width: 100%;
                text-align: center;
            ">{link_info['icon']} {platform}</a>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div></div></div>", unsafe_allow_html=True)

# AI Agents Setup
researcher = Agent(
    name="Researcher",
    instructions=[
        "Identify the travel destination specified by the user.",
        "Gather detailed information on the destination, including climate, culture, and safety tips.",
        "Find popular attractions, landmarks, and must-visit places.",
        "Search for activities that match the user's interests and travel style.",
        "Prioritize information from reliable sources and official travel guides.",
        "Provide well-structured summaries with key insights and recommendations."
    ],
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[SerpApiTools(api_key=SERPAPI_KEY)],
    add_datetime_to_instructions=True,
)

planner = Agent(
    name="Planner",
    instructions=[
        "Create a detailed day-by-day itinerary based on the research provided.",
        "Include specific times, locations, and estimated costs.",
        "Consider travel time between locations and rest periods.",
        "Adapt recommendations based on weather and seasonal factors.",
        "Include backup plans and alternative activities.",
        "Ensure the schedule is realistic and well-paced."
    ],
    model=Gemini(id="gemini-2.0-flash-exp"),
    add_datetime_to_instructions=True,
)

hotel_restaurant_finder = Agent(
    name="Hotel & Restaurant Finder",
    instructions=[
        "Find accommodations matching the user's preferences and budget.",
        "Research highly-rated restaurants near attractions and hotels.",
        "Include price ranges, ratings, and booking information.",
        "Consider dietary restrictions and local specialties.",
        "Provide specific recommendations with contact details."
    ],
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[SerpApiTools(api_key=SERPAPI_KEY)],
    add_datetime_to_instructions=True,
)

# Generate Travel Plan
if st.button("🚀 Generate Travel Plan"):
    if not source_airport or not destination_airport:
        st.error("Please ensure both cities are entered correctly and have valid airport codes.")
    else:
        with st.spinner("✈️ Fetching best flight options..."):
            flight_data = fetch_flights(source_city, destination_city, departure_date, return_date)
            if flight_data:
                cheapest_flights = extract_cheapest_flights(flight_data)
                st.subheader("✈️ Best Flight Options")
                if cheapest_flights:
                    for flight in cheapest_flights:
                        display_flight_card(flight, source_city, destination_city, departure_date)
                else:
                    st.warning("⚠️ No flight options found for these dates.")
            else:
                st.warning("⚠️ No flight data available for these dates. Try different dates or cities.")

        with st.spinner("🔍 Researching destination..."):
            research_prompt = f"""
            Research a detailed travel guide for a trip from {source_city}, {source_country} 
            to {destination_city}, {destination_country} for a {num_days}-day {travel_theme.lower()} trip.

            Please include:
            1. Best time to visit and current weather conditions
            2. Must-visit attractions based on these interests: {activity_preferences}
            3. Local customs and cultural considerations
            4. Recommended areas to stay based on a {budget} budget
            5. Transportation options within the city
            6. Local cuisine recommendations
            7. Safety tips and travel advisories
            8. Essential phrases in the local language

            Additional preferences:
            - Flight Class: {flight_class}
            - Hotel Rating: {hotel_rating}
            - Visa Required: {visa_required}
            - Travel Insurance: {travel_insurance}
            """
            research_results = researcher.run(research_prompt, stream=False)

        with st.spinner("🏨 Finding accommodations and restaurants..."):
            hotel_restaurant_prompt = f"""
            Find the best accommodations and dining options in {destination_city} based on:
            - Budget Level: {budget}
            - Hotel Rating: {hotel_rating}
            - Trip Style: {travel_theme}
            - Activities: {activity_preferences}

            Include:
            1. Top 3 hotel recommendations with prices and amenities
            2. Best local restaurants near attractions
            3. Must-try local dishes
            4. Booking information and contact details
            """
            hotel_restaurant_results = hotel_restaurant_finder.run(hotel_restaurant_prompt, stream=False)

        with st.spinner("🗺️ Creating your personalized itinerary..."):
            planning_prompt = f"""
            Create a detailed {num_days}-day itinerary for {destination_city}, {destination_country}.

            Trip Details:
            - Duration: {num_days} days
            - Style: {travel_theme}
            - Interests: {activity_preferences}
            - Budget Level: {budget}

            Please provide:
            1. Day-by-day schedule with specific times
            2. Estimated costs for activities
            3. Transportation recommendations between locations
            4. Meal suggestions at recommended restaurants
            5. Rest/flexible time slots
            6. Alternative activities for bad weather
            7. Evening entertainment options
            8. Local tips and tricks

            Based on research: {research_results.content}
            Hotels & Restaurants: {hotel_restaurant_results.content}
            """
            itinerary = planner.run(planning_prompt, stream=False)

        # Display Results
        st.subheader("🏨 Accommodation & Dining Recommendations")
        st.write(hotel_restaurant_results.content)

        st.subheader("📍 Destination Research")
        st.write(research_results.content)

        st.subheader("📅 Your Personalized Itinerary")
        st.write(itinerary.content)

        st.success("✅ Travel plan generated successfully!")
