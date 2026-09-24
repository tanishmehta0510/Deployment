import streamlit as st
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

st.set_page_config(
    page_title="Travel Assistant",
    page_icon="🚀"
)
#Background
BG_SOURCE = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHU1ODZzMHBpdGlwMnlnNWVtMmI4NXA4dnoyYm0wZ2JzdDhwdzhsOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/RoFXqXWN639Qs/giphy.gif"
# ==========================================================

def background_html(src: str) -> str:
    """Return the <video> or <img> tag for the fullscreen background."""
    ext = src.split("?")[0].rsplit(".", 1)[-1].lower()
    if ext in ("mp4", "webm", "ogg"):
        return (
            f'<video class="bg-media" autoplay muted loop playsinline preload="auto">'
            f'<source src="{src}" type="video/{ "mp4" if ext == "mp4" else ext }"></video>'
        )
    return f'<img class="bg-media" src="{src}" alt="">'

# Set Design
CSS = """
/* ============ Page background (fallback if the media file is missing) ============ */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #1e4d3a 0%, #1d4e6b 50%, #3b2f63 100%);
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    max-width: 820px;
    padding-top: 2rem;
    position: relative;
    z-index: 0;              /* creates a stacking context so the bg can sit at -2 */
}

/* ============ Fullscreen nature background ============ */
.bg-media {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    object-fit: cover;       /* fills the screen like a wallpaper, no stretching */
    z-index: -2;
    pointer-events: none;
}
.bg-overlay {                /* soft dark vignette so text stays readable */
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    background:
        radial-gradient(ellipse at center, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.45) 100%);
}

/* ============ Hero banner ============ */
@keyframes float {
    0%   { transform: translateY(0px) rotate(0deg); }
    50%  { transform: translateY(-8px) rotate(3deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}
@keyframes pulseGlow {
    0%   { opacity: 0.6; }
    50%  { opacity: 1; filter: drop-shadow(0 0 10px rgba(255,255,255,0.6)); }
    100% { opacity: 0.6; }
}
.travel-hero {
    background: rgba(10, 25, 30, 0.45);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 2.5rem 2rem;
    border-radius: 18px;
    color: white;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.45);
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.25);
}
.travel-icon {
    display: inline-block;
    animation: float 4s ease-in-out infinite;
    font-size: 3.5rem;
    margin-bottom: 5px;
}
.travel-title {
    font-size: 3rem;
    margin: 0;
    font-weight: 800;
    letter-spacing: 1px;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(to right, #ffffff, #a8ff78);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.travel-badge {
    margin-top: 15px;
    display: inline-block;
    background: rgba(255, 255, 255, 0.12);
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 0.9rem;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    animation: pulseGlow 3s infinite;
}

/* ============ Input card (glass panel over the nature scene) ============ */
.st-key-input_card {
    background: rgba(10, 25, 30, 0.50);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}
/* labels above the boxes: white so they read on the dark glass */
.st-key-input_card label,
.st-key-input_card label p,
.st-key-input_card [data-testid="stWidgetLabel"] p,
.st-key-input_card [data-testid="stRadio"] div[role="radiogroup"] label p {
    color: #ffffff !important;
    font-weight: 500;
}

/* ============ TEXTBOXES: white background, black text (always, also on load) ============ */
.st-key-input_card [data-baseweb="input"],
.st-key-input_card [data-baseweb="base-input"],
.st-key-input_card [data-baseweb="textarea"],
.st-key-input_card [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}
.st-key-input_card input,
.st-key-input_card textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;   /* beats browser autofill / dark-theme colours */
    caret-color: #000000;
}
.st-key-input_card input::placeholder,
.st-key-input_card textarea::placeholder {
    color: #6b7280 !important;
    -webkit-text-fill-color: #6b7280 !important;
    opacity: 1;
}
/* selectbox: shown value + dropdown arrow + popup list */
.st-key-input_card [data-baseweb="select"] div,
.st-key-input_card [data-baseweb="select"] span {
    color: #000000 !important;
}
.st-key-input_card [data-baseweb="select"] svg {
    fill: #000000 !important;
}
[data-baseweb="popover"] ul,
[data-baseweb="popover"] li {
    background-color: #ffffff !important;
    color: #000000 !important;
}
[data-baseweb="popover"] li:hover {
    background-color: #e6f4ee !important;
}
/* number input +/- buttons */
.st-key-input_card [data-testid="stNumberInputStepDown"],
.st-key-input_card [data-testid="stNumberInputStepUp"] {
    background-color: #f1f5f4 !important;
    color: #000000 !important;
}

/* ============ Plan Trip button ============ */
.stButton button {
    background: linear-gradient(135deg, #2c8a5a, #1f6f8b);
    border: none;
    border-radius: 999px;
    padding: 0.6rem 2rem;
    font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton button p {
    color: white;
}
.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.4);
}

/* ============ Itinerary result card ============ */
.st-key-result_card {
    background: rgba(255, 255, 255, 0.92);
    border-left: 5px solid #2c8a5a;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-top: 1rem;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
    color: #111111;
}
.st-key-result_card p, .st-key-result_card li,
.st-key-result_card h1, .st-key-result_card h2,
.st-key-result_card h3, .st-key-result_card h4 {
    color: #111111;
}

/* ============ Respect users who turn motion off ============ */
@media (prefers-reduced-motion: reduce) {
    .travel-icon, .travel-badge { animation: none; }
    video.bg-media { display: none; }   /* falls back to the gradient */
}
"""

# Plain string concatenation (not an f-string) so the CSS braces are left alone
st.markdown("<style>" + CSS + "</style>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    /* target the image inside your background_html wrapper */
    .stApp img, .bg-img {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover; /* Forces image to scale and crop perfectly */
        z-index: -2;
    }
    
    /* target your overlay div */
    .bg-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.4); /* Optional: darkens image for text readability */
        z-index: -1;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Nature background + readability overlay
st.markdown(background_html(BG_SOURCE) + '<div class="bg-overlay"></div>', unsafe_allow_html=True)

# Hero banner
st.markdown(
    """
    <div class="travel-hero">
        <div class="travel-icon">✈️🌍</div>
        <h1 class="travel-title">AI Travel Assistant</h1>
        <p style="font-size: 1.2rem; margin-top: 12px; color: #e6ecef; font-weight: 300;">
            Your intelligent companion for seamless journeys, itineraries, and local secrets.
        </p>
        <div class="travel-badge">
            🚀 Ready for takeoff • Let's explore the world
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(key="input_card"):
    destination = st.text_input("Please select a travel destination :", placeholder="Enter a destination...")
    days = st.number_input("Please provide number of days of trip : ", min_value=1, max_value=90, placeholder="Enter number of days...")
    budget = st.selectbox("Select Budget", ["Luxury", "Moderate", "Budgeted"])
    travel_type = st.radio("Please select travel-type", ["Family", "Solo", "Friends", "Other"])
    details = st.text_area("Please provide any specific requirements if any...", placeholder="Enter what you wish to keep in mind while generating itinerary...")

prompt = f"""Act as a travel assistant. 
    Destination = {destination}
    No of days of trip = {days}
    Budget = {budget}
    Traveller type = {travel_type}
    Keep in mind user-specific requirements to generate itinerary if any = {details}
    """

if st.button("Plan Trip"):
    with st.spinner("Generating best itinerary for the trip...", show_time=True):
        interaction = client.interactions.create(
                model="gemini-3.5-flash-lite",
                input=prompt,
                system_instruction="""Provide helpful and informative responses to the user's travel-related queries.
                    Be direct and clear. Answer in syntax (always when needed but if needed only, or you can even apply syntax but add/remove parameters of syntax if you feel not necessary for given input) - Answer to users question relating previous chat (if any, not always), destinations covered in trip, duration of trip, mode of transports in between locations of the trip (transit transport modes), usual climate condition and any other such relevant parameter.
                    Do not generate parameters in code-like snippets but in bullets/lists only.
                    Then leave a line and give a detailed itinerary. 
                    If the user asks for a specific destination to be added in trip, provide detailed information about that destination with respect to earlier itinerary provided/generated. 
                    If the user asks for a travel itinerary, provide a detailed itinerary based on their preferences(or improvised). 
                    Generate itinerary for the location based on practical considerations. 
                    If the user asks for travel tips, provide helpful tips and advice. 
                    If the user asks for travel recommendations, provide personalized recommendations based on their interests and preferences. 
                    Note to ask user for details - days, dates, triptype, traveler-type,etc. - however do not irritate user by asking many questions. If user resists giving details, ignore that parameter and generate itinerary assuming ideal and practical and majority of cases.
                    If the user asks for travel-related information that is not available, politely inform them that you do not have that information and suggest alternative options or resources like the user's preferences. 
                    Suggest nearby must-visits. Always maintain a friendly and helpful tone in your responses. 
                    Most importantly remember all earlier inputs and outputs and provide a detailed itinerary based on the user's preferences i.e new itinerary generated must be adding/removing/editing of older itinerary generated as per user's request.
                    If the user asks for travel tips, provide helpful tips and advice. 
                    Ask for details of trip only if really necessary details are specified i.e for example location, no. of days, etc. but do not ask personal information.
                    Avoid generation of code snippets, JSONS, Lists, Tuples, etc. or any other system-type formats in the itinerary.
                    Do appropriate formatting - bold, underline, italics, subscript, superscript, emoji, strikethrough only wherever necessary. Use lists or numbers, horizontal lines, font sizes but use standard font faces like Times New Roman, Arial, Verdana, etc.
                    Response must be easy to read and good to look (colorful).
                    """
            )
    st.success("Itinerary successfully generated...")
    with st.container(key="result_card"):
        st.write(interaction.output_text)