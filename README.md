# ✈️ Wayfinder – AI Travel Agent

Wayfinder is an AI-powered travel assistant that helps users plan trips intelligently by providing flight recommendations, hotel suggestions, tourist attractions, and AI-generated travel assistance.

The project integrates Large Language Models (LLMs), APIs, and intelligent tools to create an interactive travel planning system.

---

# 🚀 Features

- ✈️ Flight Search using SerpAPI
- 🏨 Hotel Recommendations
- 📍 Tourist Attractions Finder
- 🤖 AI-Powered Travel Planning
- 📧 Send Travel Plans via Email
- 🎨 Interactive Streamlit UI
- 🌍 Natural Language Query Processing

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend Development |
| Streamlit | Frontend UI |
| LangChain | AI Orchestration |
| LangGraph | Agent Workflow |
| Groq API | LLM Inference |
| SerpAPI | Flights & Hotel Search |
| Geoapify API | Tourist Attractions |
| Gmail SMTP | Email Integration |
| Poetry | Dependency Management |

---

# 📂 Project Structure

```bash
travel_agent/
│
├── app.py
├── attractions_finder.py
├── flights_finder.py
├── hotels_finder.py
├── test_tools.py
├── .env
├── .gitignore
├── pyproject.toml
├── poetry.lock
│
├── agents/
│   └── agent.py
│
├── images/
│   └── ai-travel.png
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Nandini-Alapati/travel_agent.git
cd travel_agent
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

### Using pip

```bash
pip install -r requirements.txt
```

### Using Poetry

```bash
poetry install
```

---

# 🔑 Environment Variables

Create a `.env` file and add the following:

```env
GROQ_API_KEY=your_groq_api_key
SERPAPI_API_KEY=your_serpapi_key
GEOAPIFY_API_KEY=your_geoapify_key

GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_app_password
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

# 💡 Example Query

```text
Plan a trip from Hyderabad to Paris,
depart October 10 2025 and return October 20 2025.
Find flights, 3-4 star hotels near the Eiffel Tower,
and must-see attractions.
```

---

# 🧠 How the System Works

## Step 1: User Input
The user enters a travel query through the Streamlit interface.

## Step 2: AI Agent Processing
LangChain agents analyze the request and identify:
- Flight requirements
- Hotel requirements
- Attraction searches

## Step 3: API Integration
The system fetches data using:
- SerpAPI for flights & hotels
- Geoapify for attractions

## Step 4: Response Generation
The AI agent combines all information into a structured travel plan.

## Step 5: Email Sharing
Users can optionally send travel details via email.

---

# 🎯 Key Functionalities

✔ Natural language travel planning  
✔ Multi-tool AI agent system  
✔ Real-time travel information retrieval  
✔ Attraction discovery using coordinates or city names  
✔ Email integration  
✔ Interactive frontend UI  

---

# 📸 UI Preview

Add your screenshots here.

Example:

```markdown
![Home Page](images/homepage.png)
```

---

# 🔍 APIs Used

## 🌍 Geoapify API
Used for:
- Geocoding
- Tourist attraction discovery

## 🔎 SerpAPI
Used for:
- Flight search
- Hotel search

## 🤖 Groq API
Used for:
- LLM-powered AI responses

---

# 🧪 Testing

Run:

```bash
python test_tools.py
```

This checks:
- API key loading
- Agent functionality
- Query processing

---

# 🚧 Future Improvements

- 🌐 Real-time flight booking
- 🗺️ Interactive maps
- 🎙️ Voice-enabled assistant
- 📱 Mobile responsiveness
- 💳 Booking integration
- 🌦️ Weather forecasting
- 🧳 Personalized itinerary generation
- 🔐 User authentication system

---

# 📚 Learning Outcomes

Through this project, we learned:

- Building AI agents with LangChain
- API integration
- Streamlit frontend development
- Environment variable management
- Email automation
- Intelligent travel planning systems
- Multi-tool orchestration

---

# 📄 License

This project is developed for educational and learning purposes.

---

# ⭐ Acknowledgements

- LangChain
- Streamlit
- SerpAPI
- Geoapify
- Groq AI
