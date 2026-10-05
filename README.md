# Suraksha-AR

**Suraksha-AR** is an offline-first Augmented Reality (AR) safety training platform designed specifically for industrial and mining workers (e.g., in Jharkhand). It provides immersive hazard recognition and response training directly on Android smartphones, requiring no continuous internet connection.

## 🌟 Key Features
- **Immersive AR Training:** Real-time 3D modules (Fire Extinguisher, Gas Leak, PPE Selection) using Google ARCore.
- **Offline-First Architecture:** Workers can complete training and earn certificates entirely offline. Data seamlessly syncs to the server when a connection is restored.
- **Multilingual Support:** Built-in support for English, Hindi (हिन्दी), and Santali (ᱥᱟᱱᱛᱟᱲᱤ).
- **Secure Digital Certificates:** Issues cryptographic ES256-signed QR codes that supervisors can instantly verify offline.
- **Web Admin Dashboard:** A React-based portal for Safety Managers to track site compliance and worker KPIs.

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, SQLite, SQLAlchemy, JWT Authentication
- **Web Dashboard:** React, TypeScript, Vite, Tailwind CSS
- **Android App:** Kotlin, Jetpack Compose, ARCore (SceneView), Room Database, Hilt, WorkManager

---

## 🚀 Project Setup Tutorial

### Prerequisites
Before you begin, ensure you have the following installed on your machine:
- **Python 3.10+** (For the backend)
- **Node.js 18+** (For the web dashboard)
- **Android Studio** (For compiling the Android app)
- **Git**

---

### 1. Backend Setup (FastAPI)
The backend manages the database, authentication, and offline sync resolution.

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Seed the database with demo users, sites, and mock certificates:
   ```bash
   python -m app.seed
   ```
5. Start the backend server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   *(The API will now be running at `http://localhost:8000`)*

---

### 2. Web Dashboard Setup (React)
The web dashboard is used by administrators to monitor safety compliance.

1. Open a **new** terminal and navigate to the web directory:
   ```bash
   cd web
   ```
2. Install the Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *(The dashboard will be available at `http://localhost:5173`)*

---

### 3. Android App Setup (Kotlin/ARCore)
The Android app is the primary interface for the workers.

1. Open **Android Studio**.
2. Click **Open** and select the `android` folder located inside the `suraksha-ar` repository.
3. Wait for the **Gradle Sync** to finish downloading all dependencies.
   - *Note: If you get an "Invalid Gradle JDK" error, go to `Settings > Build, Execution, Deployment > Build Tools > Gradle` and select **Java 17**.*
4. **Important for testing on a physical phone:**
   Open `android/app/build.gradle.kts` and find the `API_BASE_URL` config. Change `10.0.2.2` to your computer's actual local Wi-Fi IP address (e.g., `192.168.1.5`) so your phone can talk to your local backend.
   ```kotlin
   buildConfigField("String", "API_BASE_URL", "\"http://192.168.1.5:8000/api/v1\"")
   ```
5. Connect an Android 10+ phone via USB (with USB Debugging enabled).
6. Click the green **Run (▶)** button in Android Studio to install the app on your phone.

---

## 🔑 Demo Login Credentials

Because the database was seeded in Step 1, you can use the following credentials to test the system immediately:

**For the Web Dashboard (Admin):**
- **Email:** `admin@suraksha.demo`
- **Password:** `Admin@123`

**For the Android App (Worker):**
- **Phone Number:** `9000000001`
- **6-Digit PIN:** `1234`

---
*Built for SIH 2024.*
