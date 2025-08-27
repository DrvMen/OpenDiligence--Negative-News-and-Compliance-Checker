# OpenDiligence – Negative News and Compliance Checker

OpenDiligence is a **due diligence and compliance monitoring tool** that helps detect negative news and compliance risks related to individuals or companies.  
It aggregates data from public sources (news, government portals, etc.), applies AI-based filtering, and presents structured intelligence through a web interface.

---

## 🚀 Features

- **News & Compliance Monitoring**: Fetches and processes data from multiple sources.
- **AI-Powered Filtering**: Highlights high-risk mentions (fraud, bankruptcy, legal actions, etc.).
- **Frontend UI**: Built with modern frameworks for a clean and interactive experience.
- **Backend API**: Provides endpoints for scraping, processing, and serving results.
- **Scalable Design**: Can be extended with cloud deployment (AWS/GCP/Vercel).

---

## 📂 Project Structure

```
OpenDiligence--Negative-News-and-Compliance-Checker/
│
├── backend/ # Node.js/Express backend (APIs, scraping, AI filters)
├── frontend/ # React-based frontend UI
├── node_modules/ # Dependencies (should be ignored in production)
├── package.json # Project dependencies
├── package-lock.json # Dependency lockfile
└── README.md # Project documentation
```


---

## 🛠️ Tech Stack

- **Frontend:** React, TailwindCSS 
- **Backend:** Node.js, Express.js
- **Database:** MongoDB (planned integration)
- **Scraping:** Playwright / BeautifulSoup (Python integration possible)
- **AI/NLP:** Transformers for text classification & risk tagging
- **Deployment:** AWS

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/DrvMen/OpenDiligence--Negative-News-and-Compliance-Checker.git
cd OpenDiligence--Negative-News-and-Compliance-Checker
```

2. Install Dependencies

Backend:
```bash
cd backend
npm install
```

Frontend:
```bash
cd ../frontend
npm install
```
3. Run the Project

Backend:
```bash
python app.py
```

Frontend:
```bash
npm run dev
```
📌 Future Improvements

✅ Multi-language news filtering

✅ Dashboard with risk scoring

✅ Export reports (PDF/Excel)
