# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DOTApy is a Booking.com web scraper that extracts hotel information, reviews, and pricing data into a MySQL database. It is written in Python 3 and uses Selenium for browser automation.

## Running the Scripts

There is no build system. Scripts are run directly with Python:

```bash
# Stage 1: Extract hotel URLs for a city over a date range
python URIextractor.py -c <city> -d <"month year"> -m <num_months>
# Example:
python URIextractor.py -c Milano -d "maggio 2020" -m 3

# Stage 2: Extract hotel info and reviews
python InfoReviews.py -c <city> [-nr <num_review_pages>] [-ph <num_hotel_pages>]

# Stage 3: Extract prices (reads URLs from DB, no city argument needed)
python Prices.py

# Run the full pipeline
bash run.sh
```

Verbosity flags `-v` (level 1) and `-vv` (level 2) are supported across all scripts.

## Setup Requirements

Install dependencies manually (no requirements.txt):
```bash
pip install selenium mysql-connector
```

External requirements:
- MySQL/MariaDB with database `o.t.a.` initialized from `DBstruttura.sql`
- Chrome browser + matching ChromeDriver on PATH
- Database credentials configured in `config.ini` (`[mysqlDB]` section: host, db, user, pass)

## Architecture

The system is a **three-stage sequential pipeline**:

1. **`URIextractor.py`** — Navigates Booking.com's search calendar for a given city and date range, captures the resulting search URLs, and stores them in the `urlhotel` table. Key function: `data(inpu, inpu1)` drives the calendar interaction.

2. **`InfoReviews.py`** — Iterates through hotel listing pages for a city, visits each hotel page, and extracts structured data (metadata + reviews) into the `accomodation`, `accomodationrecensioni`, `accomodationservice`, and related tables. Key functions: `estrazioneInfoHotel()`, `recen()`, `entraHotel()`.

3. **`Prices.py`** — Reads every URL from `urlhotel`, opens the search results page for each date, and scrapes hotel prices into `accomodationprice`. Key function: `trovaHtPr()`.

**`utility.py`** provides shared date/month helpers used by the other modules (Italian↔English month translation, date normalization).

## Database Schema

The `o.t.a.` MySQL database has 8 tables. The main ones:

| Table | Contents |
|---|---|
| `urlhotel` | Search URLs with check-in date and city (input for Prices.py) |
| `accomodation` | Hotel metadata (name, address, coordinates, type, star rating) |
| `accomodationrecensioni` | Customer reviews linked to hotel |
| `accomodationprice` | Price records (hotel, price, stay date, search date, city) |
| `accomodationservice` | Junction table linking hotels to `servizi` |

## Key Implementation Notes

- **Selenium version:** The code uses the deprecated `find_element_by_xpath()` / `find_elements_by_class_name()` API (Selenium 3 style). Selenium 4+ requires `find_element(By.XPATH, ...)`.
- **State management:** Scripts use module-level global variables extensively for shared state between functions.
- **Cookie/popup handling:** Each script manually accepts Booking.com consent dialogs via multiple XPath fallbacks.
- **Debug logging:** A local `debug(string, level)` function is used throughout instead of the `logging` module. Level 0 = errors, 1 = info, 2 = verbose.
- **Database inserts:** Uses `mysql-connector` with `%s` parameterized queries and explicit `conn.commit()` after each insert.
