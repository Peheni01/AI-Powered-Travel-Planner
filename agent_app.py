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
        "Beijing": ["PEK", "PKX"],
        "Hong Kong": ["HKG"],
        "Tokyo": ["HND", "NRT"],
        "Seoul": ["ICN", "GMP"],
        "Shanghai": ["PVG", "SHA"],
        "Osaka": ["KIX"],
        "Fukuoka": ["FUK"],
        "Jeju City": ["CJU"],
        "Taipei": ["TPE"],
        "Guangzhou": ["CAN"],
        "Shenzhen": ["SZX"],
        "Chengdu": ["CTU"], 
        "Kunming": ["KMG"],
        "Xi'an": ["XIY"],
        "Chongqing": ["CKG"],
        "Hangzhou": ["HGH"],
        "Tianjin": ["TSN"],
        "Nanjing": ["NKG"],
        "Changsha": ["CSX"],
        "Wuhan": ["WUH"],
        "Xiamen": ["XMN"],
        "Qingdao": ["TAO"],
        "Harbin": ["HRB"],
        "Shenyang": ["SHE"],
        "Ulaanbaatar": ["ULN"],
        "Macau": ["MFM"],
        "Pyongyang": ["FNJ"],
        "Singapore": ["SIN"],
        "Bangkok": ["BKK", "DMK"],
        "Kuala Lumpur": ["KUL"],
        "Jakarta": ["CGK"],
        "Manila": ["MNL"],
        "Ho Chi Minh City": ["SGN"],
        "Hanoi": ["HAN"],
        "Denpasar": ["DPS"],
        "Surabaya": ["SUB"],
        "Da Nang": ["DAD"],
        "Bandar Seri Begawan": ["BWN"],
        "Phnom Penh": ["PNH"],
        "Yangon": ["RGN"],
        "Cebu": ["CEB"],
        "Medan": ["KNO"],
        "Phuket": ["HKT"],
        "Chiang Mai": ["CNX"],
        "Kota Kinabalu": ["BKI"],
        "Delhi": ["DEL"],
        "Mumbai": ["BOM"],
        "Bangalore": ["BLR"],
        "Hyderabad": ["HYD"],
        "Chennai": ["MAA"],
        "Kolkata": ["CCU"],
        "Dhaka": ["DAC"],
        "Kathmandu": ["KTM"],
        "Colombo": ["CMB"],
        "Malé": ["MLE"],
        "Islamabad": ["ISB"],
        "Karachi": ["KHI"],
        "Lahore": ["LHE"],
        "Dubai": ["DXB"],
        "Abu Dhabi": ["AUH"],
        "Doha": ["DOH"],
        "Jeddah": ["JED"],
        "Riyadh": ["RUH"],
        "Kuwait City": ["KWI"],
        "Muscat": ["MCT"],
        "Manama": ["BAH"],
        "Tehran": ["THR", "IKA"],
        "Beirut": ["BEY"],
        "Tel Aviv": ["TLV"],
        "Amman": ["AMM"],
        "Damascus": ["DAM"],
        "Basrah": ["BSR"],
        "Baghdad": ["BGW"],
        "Baku": ["GYD"],
        "Almaty": ["ALA"],
        "Tashkent": ["TAS"],
        "Bishkek": ["FRU"],
        "Dushanbe": ["DYU"],

        # Europe
        "London": ["LHR", "LGW", "STN", "LTN"],
        "Paris": ["CDG", "ORY"],
        "Amsterdam": ["AMS"],
        "Frankfurt": ["FRA"],
        "Istanbul": ["IST", "SAW"],
        "Madrid": ["MAD"],
        "Barcelona": ["BCN"],
        "Munich": ["MUC"],
        "Rome": ["FCO"],
        "Milan": ["MXP", "LIN"],
        "Dublin": ["DUB"],
        "Zurich": ["ZRH"],
        "Copenhagen": ["CPH"],
        "Palma de Mallorca": ["PMI"],
        "Manchester": ["MAN"],
        "Oslo": ["OSL"],
        "Lisbon": ["LIS"],
        "Stockholm": ["ARN"],
        "Antalya": ["AYT"],
        "Brussels": ["BRU"],
        "Düsseldorf": ["DUS"],
        "Vienna": ["VIE"],
        "Athens": ["ATH"],
        "Helsinki": ["HEL"],
        "Málaga": ["AGP"],
        "Moscow": ["SVO", "DME", "VKO"],
        "Hamburg": ["HAM"],
        "Geneva": ["GVA"],
        "St. Petersburg": ["LED"],
        "Ankara": ["ESB"],
        "Warsaw": ["WAW"],
        "Prague": ["PRG"],
        "Alicante": ["ALC"],
        "Edinburgh": ["EDI"],
        "Nice": ["NCE"],
        "Budapest": ["BUD"],
        "Gran Canaria": ["LPA"],
        "Birmingham": ["BHX"],
        "Bucharest": ["OTP"],
        "Cologne": ["CGN"],
        "Bergamo": ["BGY"],
        "Tenerife": ["TFS"],
        "Stuttgart": ["STR"],
        "Porto": ["OPO"],
        "Kyiv": ["KBP"],
        "Venice": ["VCE"],
        "Lyon": ["LYS"],
        "Glasgow": ["GLA"],
        "Toulouse": ["TLS"],
        "Catania": ["CTA"],
        "Marseille": ["MRS"],
        "Faro": ["FAO"],
        "Keflavik": ["KEF"],
        "Bologna": ["BLQ"],
        "Naples": ["NAP"],
        "Bristol": ["BRS"],
        "Ibiza": ["IBZ"],
        "Basel": ["BSL"],
        "Charleroi": ["CRL"],
        "Heraklion": ["HER"],
        "Lanzarote": ["ACE"],
        "Gothenburg": ["GOT"],
        "Valencia": ["VLC"],
        "Sofia": ["SOF"],
        "Sevilla": ["SVQ"],
        "Palermo": ["PMO"],
        "Bergen": ["BGO"],
        "Riga": ["RIX"],
        "Thessaloniki": ["SKG"],
        "Bilbao": ["BIO"],
        "Luxembourg": ["LUX"],
        "Trondheim": ["TRD"],
        "Eindhoven": ["EIN"],
        "Bordeaux": ["BOD"],
        "Nantes": ["NTE"],
        "Zagreb": ["ZAG"],
        "Cagliari": ["CAG"],
        "Tirana": ["TIA"],
        "Belfast": ["BFS"],
        "Sarajevo": ["SJJ"],
        "Larnaca": ["LCA"],
        "Paphos": ["PFO"],
        "Tbilisi": ["TBS"],
        "Yerevan": ["EVN"],
        "Belgrade": ["BEG"],
        "Bratislava": ["BTS"],
        "Ljubljana": ["LJU"],
        "Tallinn": ["TLL"],
        "Vilnius": ["VNO"],
        "Chisinau": ["KIV"],

        # North America
        "Atlanta": ["ATL"],
        "Dallas/Fort Worth": ["DFW"],
        "Denver": ["DEN"],
        "Chicago": ["ORD"],
        "Los Angeles": ["LAX"],
        "New York": ["JFK", "LGA", "EWR"],
        "Orlando": ["MCO"],
        "Charlotte": ["CLT"],
        "Las Vegas": ["LAS"],
        "Phoenix": ["PHX"],
        "Miami": ["MIA"],
        "Seattle": ["SEA"],
        "Houston": ["IAH"],
        "San Francisco": ["SFO"],
        "Boston": ["BOS"],
        "Fort Lauderdale": ["FLL"],
        "Detroit": ["DTW"],
        "Philadelphia": ["PHL"],
        "Minneapolis/St. Paul": ["MSP"],
        "Toronto": ["YYZ"],
        "Mexico City": ["MEX"],
        "Vancouver": ["YVR"],
        "Montreal": ["YUL"],
        "Cancun": ["CUN"],
        "Calgary": ["YYC"],
        "Washington, D.C.": ["IAD", "DCA"],
        "Salt Lake City": ["SLC"],
        "San Diego": ["SAN"],
        "Tampa": ["TPA"],
        "Honolulu": ["HNL"],
        "Nashville": ["BNA"],
        "Austin": ["AUS"],
        "Portland": ["PDX"],
        "St. Louis": ["STL"],
        "San Juan": ["SJU"],
        "Punta Cana": ["PUJ"],
        "Havana": ["HAV"],
        "Guadalajara": ["GDL"],
        "Monterrey": ["MTY"],
        "Panama City": ["PTY"],
        "Nassau": ["NAS"],
        "Kingston": ["KIN"],
        "Montego Bay": ["MBJ"],
        "Santo Domingo": ["SDQ"],
        "Ottawa": ["YOW"],
        "Edmonton": ["YEG"],
        "Winnipeg": ["YWG"],
        "Halifax": ["YHZ"],
        "Québec City": ["YQB"],
        "San José (Costa Rica)": ["SJO"],
        "San Salvador": ["SAL"],
        "Guatemala City": ["GUA"],
        "Tegucigalpa": ["TGU"],
        "Managua": ["MGA"],

        # South America
        "São Paulo": ["GRU", "CGH"],
        "Rio de Janeiro": ["GIG", "SDU"],
        "Bogotá": ["BOG"],
        "Santiago": ["SCL"],
        "Lima": ["LIM"],
        "Buenos Aires": ["EZE", "AEP"],
        "Salvador": ["SSA"],
        "Brasília": ["BSB"],
        "Fortaleza": ["FOR"],
        "Recife": ["REC"],
        "Porto Alegre": ["POA"],
        "Belo Horizonte": ["CNF"],
        "Medellín": ["MDE"],
        "Cali": ["CLO"],
        "Guayaquil": ["GYE"],
        "Quito": ["UIO"],
        "Montevideo": ["MVD"],
        "Asunción": ["ASU"],
        "Santa Cruz de la Sierra": ["VVI"],
        "La Paz": ["LPB"],
        "Cusco": ["CUZ"],
        "Barranquilla": ["BAQ"],
        "Manaus": ["MAO"],
        "Curitiba": ["CWB"],
        "Florianópolis": ["FLN"],
        "Córdoba": ["COR"],
        "Rosario": ["ROS"],
        "Concepción": ["CCP"],
        "Cartagena": ["CTG"],
        "Georgetown": ["GEO"],
        "Paramaribo": ["PBM"],
        "Cayenne": ["FSP"],

        # Oceania
        "Sydney": ["SYD"],
        "Melbourne": ["MEL"],
        "Brisbane": ["BNE"],
        "Perth": ["PER"],
        "Auckland": ["AKL"],
        "Christchurch": ["CHC"],
        "Wellington": ["WLG"],
        "Adelaide": ["ADL"],
        "Gold Coast": ["OOL"],
        "Cairns": ["CNS"],
        "Denpasar": ["DPS"], 
        "Nadi": ["NAN"],
        "Port Moresby": ["POM"],
        "Nouméa": ["NOU"],
        "Papeete": ["PPT"],
        "Apia": ["APW"],
        "Suva": ["SUV"],
        "Rarotonga": ["RAR"],
        "Honiara": ["HIR"],
        "Port Vila": ["VLI"],
        "Tarawa": ["TRW"],
        "Majuro": ["MAJ"],
        "Palau": ["ROR"],
        "Funafuti": ["FUN"],
        "Nuku'alofa": ["TBU"],
        "Christmas Island": ["CXI"],
        "Pago Pago": ["PPG"],

        # Africa
        "Johannesburg": ["JNB"],
        "Cairo": ["CAI"],
        "Addis Ababa": ["ADD"],
        "Casablanca": ["CMN"],
        "Cape Town": ["CPT"],
        "Hurghada": ["HRG"],
        "Marrakech": ["RAK"],
        "Algiers": ["ALG"],
        "Nairobi": ["NBO"],
        "Tunis": ["TUN"],
        "Sharm el-Sheikh": ["SSH"],
        "Lagos": ["LOS"],
        "Abuja": ["ABV"],
        "Durban": ["DUR"],
        "Accra": ["ACC"],
        "Agadir": ["AGA"],
        "Dakar": ["DSS"],
        "Dar es Salaam": ["DAR"],
        "Abidjan": ["ABJ"],
        "Tangier": ["TNG"],
        "Zanzibar": ["ZNZ"],
        "Kampala": ["EBB"],
        "Marsa Alam": ["RMF"],
        "Djerba": ["DJE"],
        "Luanda": ["LAD"],
        "Harare": ["HRE"],
        "Entebbe": ["EBB"],
        "Port Louis": ["MRU"],
        "Antananarivo": ["TNR"],
        "Kigali": ["KGL"],
        "Maputo": ["MPM"],
        "Kinshasa": ["FIH"],
        "Lusaka": ["LUN"],
        "Douala": ["DLA"],
        "Yaoundé": ["YAO"],
        "Conakry": ["CKY"],
        "Freetown": ["FNA"],
        "Lomé": ["LFW"],
        "Bamako": ["BKO"],
        "Tripoli": ["TIP"],
        "Brazzaville": ["BZV"],
        "Bujumbura": ["BJM"],
        "Libreville": ["LBV"],
        "Malabo": ["SSG"],
        "Maseru": ["MSU"],
        "Gaborone": ["GBE"],
        "Windhoek": ["WDH"],
        "Djibouti City": ["JIB"],
        "Moroni": ["YVA"],
        "Asmara": ["ASM"],
        "Banjul": ["BJL"]
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
