# Lead Gen Pro - Vercel Ready

This version is fixed for Vercel.

## Project structure

```text
lead-gen-pro/
│
├── app.py
├── main.py
├── config.py
├── vercel.json
├── scraper/
│   ├── __init__.py
│   ├── maps_scraper.py
│   ├── details_scraper.py
│   └── email_finder.py
│
├── automation/
│   ├── __init__.py
│   ├── whatsapp_sender.py
│   └── email_sender.py
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── helpers.py
│
├── data/
│   └── leads.csv
│
├── logs/
│   └── app.log
│
├── requirements.txt
└── README.md
```

## Why the old deployment failed

Vercel needs a Python web entrypoint such as `app.py`. A local script alone is not enough.

## What this fixed version does

- Adds `app.py` as the Vercel entrypoint
- Keeps `main.py` for local execution
- Exposes:
  - `/` health route
  - `/run` to run lead extraction

## Vercel environment variables

Add these in Vercel Project Settings → Environment Variables:

- `GOOGLE_MAPS_API_KEY`
- `LOCATION` = `Cairo Egypt`
- `BUSINESS_TYPE` = `restaurants`
- `RADIUS` = `3000`
- `EMAIL_SENDER` = optional
- `EMAIL_PASSWORD` = optional
- `WHATSAPP_MESSAGE` = optional

## Local run

```bash
pip install -r requirements.txt
python main.py
```

## Vercel run

After deployment open:

- `/`
- `/run?limit=20`

Example:

```text
https://your-project.vercel.app/run?limit=20
```

## Important note

Vercel has a temporary filesystem. `data/leads.csv` and `logs/app.log` are not permanent storage in production. For long-term storage use Google Sheets, Supabase, Airtable, or a database.
