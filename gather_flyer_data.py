import json
from get_sights import get_top_sights
from get_weather import Weather
from jinja2 import Template
import asyncio
from playwright.async_api import async_playwright

with open("data.json", "r") as f:
  data = json.load(f)

destination = data["destination"]

#fetching weather data
weather = Weather(**data)
avg_temp = weather.calculate_avg()
data["temperature"] = avg_temp 

#fetching sights data
top_sights = get_top_sights(destination)
print(top_sights)
data["attractions"] = top_sights

with open("data.json", "w") as f:
  json.dump(data, f)


with open("brochure_template.html", "r", encoding="utf8") as file:
    html_template = file.read()

# Create and render the template to HTML string
template = Template(html_template)
rendered_html = template.render(destination=destination, temperature=avg_temp, attractions=top_sights)

async def html_to_pdf(html_content, output_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content)
        await page.pdf(path=output_path)
        await browser.close()

output_path = 'custom-html-to-pdf-output.pdf'
# Pass the rendered HTML string to the function
asyncio.run(html_to_pdf(rendered_html, output_path))