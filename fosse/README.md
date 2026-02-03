# Chemical Equipment Parameter Visualizer

A premium, futuristic web application dashboard for analyzing chemical equipment data with advanced 3D interactive visualizations and integrated reporting.

## 🚀 Key Features

### 🏰 High-End Command Center
- **Premium Dark Glass UI**: A professional "Aero-Glass" aesthetic using translucency, blur effects, and neon accents.
- **Glassmorphic Layout**: Responsive Bento Grid design for intuitive data organization.
- **Smooth Animations**: Framer Motion powered entry transitions and spring-physics interactions.

### 📊 Advanced 3D Visualizations
- **3D Bubble Charts**: Parameter analysis (Temperature × Pressure × Flowrate) with drop lines for spatial orientation.
- **Interactive Distribution**: 3D Pie charts with "pull" effects and Bar charts with hover scaling.
- **Hover Dynamics**: Automatic detail exposure and visual feedback on chart interaction.

### 📁 Data & History Management
- **CSV Processing**: High-speed parsing using Pandas backend.
- **History Bento Grid**: Persistent timeline of past uploads with the ability to "Load to Dashboard" or "Download Original".
- **Visual Feedback**: Canvas-confetti effects on successful data processing.

### 📄 Integrated Reporting
- **In-App PDF Viewer**: Generate professional PDF reports and view them directly in a glassmorphic modal.
- **Statistical Analysis**: Automatic calculation of averages, ranges, and equipment distributions.

## 🛠️ Tech Stack

### Backend
- **Core**: Django 5.0 + Django REST Framework
- **Data Engine**: Pandas
- **Persistence**: SQLite (optimized for history management)
- **Security**: JWT Authentication

### Frontend
- **Framework**: React 18 + Vite
- **Visuals**: Plotly.js (3D engine)
- **Animation**: Framer Motion
- **Styling**: Vanilla CSS (High-end Custom Design System)

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd chemical-equipment-app-new
pip install django djangorestframework django-cors-headers pandas djangorestframework-simplejwt reportlab
python manage.py migrate
python manage.py runserver
```

### 2. Frontend Setup
```bash
cd chemical-equipment-app
npm install
npm run dev
```

The application will be available at `http://localhost:5173/`

## 🧪 Usage Guide

1. **Login**: Use the "Quick Demo Login" to access the dashboard immediately.
2. **Upload**: Select any CSV (e.g., `public/sample_equipment_data.csv`) to trigger the visualization engine.
3. **Analyze**: Explore the 3D plots, check metric cards, and use the sidebar for history and reports.
4. **History**: Reload past datasets directly from the History grid in the Reports view.

---

## 📄 License
MIT License - Developed for the FOSSE Program Screening Task.
