# Kostal PIKO 20 Scraping Utilities

I have a [Kostal PIKO 20](https://www.kostal-solar-electric.com/en-gb/products/solar-inverter/piko-12-20/) solar inverter. It comes with embedded
web server that shows both current and historic data. However, the web site
is very ugly and loads super slowly. My use case, displaying the current power inside a widget on my phone, requires a fast & simple API, which this package provides.

## Getting Started
- Install [pdm](https://pdm.fming.dev)
- `pdm install`
- `pdm run uvicorn pikoapi:app`
- `curl http://localhost:8000/live`
- start hacking!


