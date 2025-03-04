# 🌏 Traveller

Traveller is your buddy to help you find the best flight deals. But that is not all what it can do! 
It also has an artistic flair so it can paint good-looking (but I mean real good) pictures of and design informative flyers for your city of destination.

## How does it do that?

It first welcomes you with a user-friendly Streamlit (very nice library FYI) interface where you can I ask for amazing flight deals. 
Once you tell the necessary information, it then fetches deals using SerpAPI and present them to you. 
In the meantime if you look at the top left corner of the interface you will see that the "Design Flyer" button getting activated which means it's time for art.
By clicking the button you can have your flyer generated and then download it, if you will, as well as the AI-generated picture. The AI behind the picture is DALL-E 3.

### Techstack
- **Models:** GPT-4o-mini, DALL-E 3
- **Languages:** Python, HTML, CSS
- **Libraries:** OpenAI, LangChain, Streamlit, Pydantic, Jinja 2, Weasyprint, SerpAPI
