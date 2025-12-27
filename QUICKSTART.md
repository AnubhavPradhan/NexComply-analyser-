# 🚀 NexComply Analyzer - Quick Start Guide

## How to Run the Application

After downloading the NexComply Analyzer, follow these steps to get it running:

---

## Option 1: Run with Docker (Recommended - Easiest)

### Prerequisites
- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop))

### Steps

1. **Navigate to the project directory**
   ```bash
   cd NexComply-analyser-
   ```

2. **Start all services with Docker Compose**
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

3. **Access the applications**
   - **Dashboard**: Open your browser to http://localhost:8501
   - **API Documentation**: http://localhost:8000/docs

4. **Stop the services**
   ```bash
   docker-compose -f docker/docker-compose.yml down
   ```

---

## Option 2: Run Locally (Full Control)

### Prerequisites
- Python 3.9 or higher installed
- pip (Python package manager)

### Steps

1. **Navigate to the project directory**
   ```bash
   cd NexComply-analyser-
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package in development mode**
   ```bash
   pip install -e .
   ```

5. **Run the Streamlit Dashboard**
   ```bash
   streamlit run streamlit_app.py
   ```
   - Open your browser to http://localhost:8501
   - The dashboard will start automatically

6. **Run the FastAPI Server** (in a new terminal)
   ```bash
   # Activate virtual environment first
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   
   # Run the API server
   uvicorn src.api.routes:app --host 0.0.0.0 --port 8000 --reload
   ```
   - API will be available at http://localhost:8000
   - Interactive docs at http://localhost:8000/docs

---

## What You Can Do

### 1. Dashboard (http://localhost:8501)

The dashboard has 6 pages:

- **📊 Dashboard**: View KPIs, compliance trends, and risk distribution
- **🔍 Compliance Analysis**: 
  - Upload policy documents (PDF, DOCX, TXT)
  - Select a compliance framework (ISO27001, NIST-CSF, SOC2, etc.)
  - Analyze compliance gaps
  - Export results to CSV or Excel
  
- **⚠️ Risk Assessment**:
  - Define risk factors
  - Set likelihood and impact
  - Get automated risk calculations
  - View mitigation recommendations
  
- **📚 Framework Explorer**: Browse and search compliance framework controls
- **📄 Reports**: Generate various compliance and risk reports
- **⚙️ Settings**: Configure the application

### 2. API (http://localhost:8000/docs)

Use the interactive API documentation to:

- **POST /api/v1/analyze**: Analyze compliance gaps
- **POST /api/v1/assess-risk**: Perform risk assessments
- **POST /api/v1/search**: Search frameworks semantically
- **GET /api/v1/frameworks**: List available frameworks
- **GET /health**: Check API health

---

## Quick Test

### Test the Dashboard
1. Open http://localhost:8501
2. Navigate to "Compliance Analysis" page
3. Upload a sample policy document (you can use any text file for testing)
4. Select "ISO27001" as the framework
5. Click "Analyze Compliance"

### Test the API
1. Open http://localhost:8000/docs
2. Click on "GET /health"
3. Click "Try it out" then "Execute"
4. You should see: `{"status": "healthy", "version": "1.0.0", ...}`

---

## Troubleshooting

### Issue: "Module not found" errors
**Solution**: Make sure you ran `pip install -e .` to install the package

### Issue: Port already in use
**Solution**: 
- For dashboard: `streamlit run streamlit_app.py --server.port 8502`
- For API: Change the port in the uvicorn command to 8001

### Issue: Docker containers won't start
**Solution**: 
- Make sure Docker Desktop is running
- Check logs: `docker-compose -f docker/docker-compose.yml logs`

### Issue: Dependencies fail to install
**Solution**:
- Make sure you have Python 3.9 or higher
- Try upgrading pip: `pip install --upgrade pip`
- Install dependencies one by one if needed

---

## Configuration (Optional)

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` to configure:
- OpenAI API key (for enhanced features)
- Database settings
- Model configurations
- Processing parameters

---

## Sample Workflow

1. **Start the application** (choose Docker or Local)
2. **Open the Dashboard** at http://localhost:8501
3. **Go to "Framework Explorer"** to browse available frameworks
4. **Go to "Compliance Analysis"**:
   - Upload a policy document
   - Select ISO27001 framework
   - Click "Analyze Compliance"
   - Review gaps and recommendations
   - Export results
5. **Go to "Risk Assessment"**:
   - Define risk factors
   - Set likelihood and impact scores
   - Click "Assess Risk"
   - Review risk level and recommendations

---

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- View API documentation at http://localhost:8000/docs
- Check logs in the terminal where you ran the application

---

## System Requirements

- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 2GB free space
- **Python**: 3.9 or higher
- **OS**: Windows 10+, macOS 10.14+, or Linux

---

**You're all set! Start exploring the NexComply Analyzer! 🎉**
