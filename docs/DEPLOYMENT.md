# Deployment Guide: AI Learning Buddy

This guide explains how to deploy and run the **AI Learning Buddy** in three different environments: **Locally**, using **Docker**, and via **Google Colab & ngrok**.

---

## 1. Local Deployment (Standard Python)

### Prerequisites
* Python 3.10 or higher installed.
* A Google Gemini API Key.

### Step-by-Step Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/ai-learning-buddy.git
   cd ai-learning-buddy
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   
   # Activate on Windows:
   venv\Scripts\activate
   
   # Activate on macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   * Copy the example environment template:
     ```bash
     cp .env.example .env
     ```
   * Open `.env` in a text editor and paste your Google Gemini API Key:
     ```env
     GEMINI_API_KEY=AIzaSy...
     GEMINI_MODEL=gemini-3.5-flash
     ```

5. **Launch the Application:**
   ```bash
   streamlit run app.py
   ```
   The application will automatically open in a browser tab at `http://localhost:8501`.

---

## 2. Containerized Deployment (Docker)

Docker allows you to run the application in an isolated environment without needing to install Python packages directly on your machine.

### Prerequisites
* Docker and Docker Compose installed.

### Step-by-Step Instructions
1. Ensure your `.env` file is configured in the project root directory.
2. **Build and Run the Containers:**
   ```bash
   docker-compose up --build -d
   ```
3. **Verify Containers are Running:**
   ```bash
   docker ps
   ```
4. **Access the App:**
   Open `http://localhost:8501` in your browser.
5. **Stop the Containers:**
   ```bash
   docker-compose down
   ```

---

## 3. Remote Deployment (Google Colab & ngrok)

If you are running the app on Google Colab (which runs on a remote cloud server), you cannot access `localhost:8501` directly. We use `ngrok` to create a secure tunnel.

### Prerequisites
* A Google Account.
* An ngrok Account (sign up at [ngrok.com](https://ngrok.com)).
* Your ngrok Auth Token.

### Step-by-Step Instructions
1. Open Google Colab and upload or import the notebook: `notebooks/AI_Learning_Buddy_Colab.ipynb`.
2. Follow the instructions in the notebook cells:
   * **Step 1:** Install dependencies (`streamlit`, `pyngrok`, `google-generativeai`).
   * **Step 2:** Clone this repository.
   * **Step 3:** Fill in your API Keys inside the `.env` generation cell.
   * **Step 4:** Launch Streamlit in the background (`!nohup streamlit run app.py &`).
   * **Step 5:** Start ngrok. The cell will output a clickable public URL (e.g., `https://xxxx-xx-xx-xx.ngrok-free.app`).
3. Click the link to access the app running from Colab!
