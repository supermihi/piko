# Kostal PIKO 20 HTTP API Scraping Utilities

The "classic" Kostal PIKO inverters like the
[Kostal PIKO 20](https://www.kostal-solar-electric.com/en-gb/products/solar-inverter/piko-12-20/)
have an embedded web server that shows both current and historic data.

This little project contains utilities to fetch and process that data in an automated way.

## Features

- query current ("live") status (for AC and DC: current, voltage, power, per phase and total, etc.)
- export current status as Prometheus metric
- query logged data stored in device (using login)

## Project Status

Work in progress. You may find it useful, though.

## Getting Started

- install (using poetry)
- run `poetry run cli`