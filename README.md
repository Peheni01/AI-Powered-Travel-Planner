# 🌟 AI-Powered Travel Planner ✈️🌍
Your smart travel companion — plan smarter, travel better!

This intelligent travel agent leverages cutting-edge AI to transform your travel planning experience. Whether you're booking flights or hotels, exploring top destinations, or crafting the perfect itinerary, this agent has you covered — all in one seamless app.

![App Screenshot](https://github.com/Peheni01/AI-Powered-Travel-Planner/blob/809f45db4e314eca4b3e1cd0ed382560bc3be684/app_pic1.png)
![App Screenshot](https://github.com/Peheni01/AI-Powered-Travel-Planner/blob/809f45db4e314eca4b3e1cd0ed382560bc3be684/app_pic2.png)

## 🚀 Key Features
- 🧠 **AI-Powered Itinerary Builder**: Generate personalized travel plans based on your interests and trip duration.
- 💸 **Smart Budget Optimization**: Uses real-time search to suggest the most cost-effective flights, flight bookings, and accommodations.
- 🧳 **Destination & Activity Recommender**: Discover top-rated attractions, restaurants, and hidden gems.
- 🧾 **Custom Travel Checklist**: Stay organized with a dynamic pre-travel checklist tailored to your trip.
- 🔍 **Integrated Search**: Uses SerpAPI and Gemini to retrieve real-time travel information and suggestions.
- 🌐 **Beautiful & Intuitive UI**: Built with Streamlit to ensure a smooth, user-friendly experience.

## 🔧 Tech Stack
- **Streamlit** – for the interactive UI  
- **Google Gemini + Agno Agents** – for intelligent query handling  
- **SerpAPI** – for real-time search and travel data  
- **Python** – the core logic and integrations

## 📡 API Reference

This AI-powered travel planner integrates several APIs and AI models to provide a seamless and intelligent travel experience.

### 🔍 SerpAPI
- **Purpose**: Fetches real-time web search results including travel guides, places, and services.
- **Base URL**: `https://serpapi.com/search`
- **Method**: `GET`
- **Parameters**:
  - `q`: Search query (e.g., "top places in Paris")
  - `engine`: Search engine (e.g., `google`)
  - `api_key`: Your SerpAPI key
- **Documentation**: [https://serpapi.com/](https://serpapi.com/)

### 🧠 Gemini API (Google AI)
- **Purpose**: Natural language processing, itinerary generation, and intelligent response generation.
- **Model**: `gemini-pro`
- **Endpoint**: Varies depending on library used (`generativeai`, etc.)
- **Method**: `POST`
- **Usage**:
  - Takes in user preferences and trip details.
  - Returns suggestions, summaries, or custom responses.
- **Documentation**: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 🧠 Agno Agents
- **Purpose**: Facilitates conversational workflows and modular query handling in multi-step planning.
- **Function**: Manages agent routing, context-aware conversations, and task delegation.
- **Documentation**: [https://docs.agno.ai/](https://docs.agno.ai/) *(if publicly available)*

---

> 💡 *Plan with intelligence. Travel with ease.*
