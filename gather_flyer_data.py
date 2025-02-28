import json
from get_sights import get_top_sights
from get_weather import Weather
from generate_image import generate_image
from jinja2 import Template
import weasyprint
import asyncio
from playwright.sync_api import sync_playwright


def gather_data():

  with open("data.json", "r") as f:
    data = json.load(f)

  destination = data["destination"]

  # Generate image
  #generate_image(destination)

  # Fetch weather data
  weather = Weather(**data)
  avg_temp = weather.calculate_avg()

  # Fetch sights data
  top_sights = get_top_sights(destination)

  with open("brochure_template.html", "r", encoding="utf8") as file:
      html_template = file.read()

  # Create and render the template to HTML string
  template = Template(html_template)
  rendered_html = template.render(destination=destination, temperature=avg_temp, attractions=top_sights)


  weasyprint.HTML(string=str(rendered_html), base_url=".").write_pdf(f"{destination}-flyer.pdf")
