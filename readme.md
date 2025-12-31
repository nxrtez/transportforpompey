# Transport for Portsmouth (TfP)

<p align="center">
  <img
    src="https://raw.githubusercontent.com/nxrtez/transportforpompey/main/static/img/tfp/Blue%20Full%20Transparent.png"
    alt="Transport for Portsmouth"
    height=400
  />
</p>


A modern, TfL-style public transport information platform for Portsmouth.

## Features
- Live-style service status by mode, operator, and route
- Operator-specific branded pages
- Route maps and visual previews
- Admin-managed service disruptions
- Scalable Django architecture

## Tech Stack
- Python 3.11+
- Django 6.x
- PostgreSQL (recommended for production)
- HTML / CSS / Vanilla JS

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
