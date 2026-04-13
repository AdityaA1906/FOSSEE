# Chemical Equipment Parameter Visualizer
**FOSSEE (IIT Bombay) Internship Screening Task**

🔗 **Live Demo:** [fossee-two.vercel.app](https://fossee-two.vercel.app)

---

## About
A full-stack web app to upload chemical equipment CSV data, visualize parameters interactively, and generate PDF reports.

## Tech Stack
- **Frontend:** React 19, Vite, Plotly.js, Framer Motion
- **Backend:** Django 5, Django REST Framework, Pandas, ReportLab
- **Auth:** JWT | **DB:** SQLite | **Deploy:** Vercel + Render

## Key Features
- CSV upload with instant parsing and storage
- Interactive 3D charts (Flowrate, Pressure, Temperature)
- Auto-calculated statistics (mean, min, max, std deviation)
- PDF report generation and download
- Upload history — reload any of last 5 datasets

## Quick Start
# Backend
cd fosse/chemical-equipment-app-new
pip install -r requirements.txt
python manage.py migrate && python manage.py runserver

# Frontend
cd fosse/chemical-equipment-app
npm install && npm run dev
