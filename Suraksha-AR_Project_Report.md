# Project Report: Suraksha-AR
**Next-Generation Augmented Reality Safety Training Platform**

## 1. Executive Summary
Suraksha-AR is an innovative, offline-first Augmented Reality (AR) training platform designed specifically for the mining and industrial sectors, particularly addressing the unique challenges faced in regions like Jharkhand. The platform aims to revolutionize industrial safety training by replacing passive classroom learning with interactive, 3D spatial hazard recognition and response exercises directly on Android smartphones.

## 2. Problem Statement
Mining and heavy industries experience high rates of workplace accidents due to ineffective safety training. Traditional methods (videos and manuals) fail to build spatial awareness or muscle memory. Furthermore, many mining sites are located in remote areas with poor or non-existent internet connectivity, making cloud-based training solutions unviable. Finally, linguistic diversity (e.g., Hindi, Santali) is often ignored in standard safety software, leading to poor comprehension among frontline workers.

## 3. Proposed Solution
Suraksha-AR solves these challenges through a three-pillared approach:
1. **Immersive AR Training:** Using Google ARCore, the app superimposes 3D hazards (fires, gas leaks, electrical faults) onto the real world. Workers must physically move and interact with virtual tools (like a 3D fire extinguisher) to mitigate the hazard.
2. **Offline-First Synchronization:** The entire Android application, including all 3D assets and logic, runs 100% offline. Worker progress is saved locally in an encrypted Room Database and automatically synchronized to a central backend via WorkManager only when an internet connection is established.
3. **Verifiable Digital Certificates:** Upon successful completion of a module, the system generates a cryptographic ES256-signed QR code. This allows site supervisors to instantly verify a worker's training status in the field, even completely offline.

## 4. System Architecture
The platform is built using a modern, scalable micro-architecture:

### 4.1. Android Application (Worker Interface)
- **Language:** Kotlin
- **UI Framework:** Jetpack Compose (Material Design 3)
- **AR Engine:** SceneView (ARCore wrapper) for rendering `.glb` 3D models and handling plane detection.
- **Local Storage:** Room Database for caching JSON-based training modules, user sessions, and assessment scores.
- **State Management:** MVVM architecture with Kotlin StateFlow and Coroutines.
- **Dependency Injection:** Dagger-Hilt.

### 4.2. Backend API (Central Server)
- **Framework:** Python FastAPI
- **Database:** SQLite (scalable to PostgreSQL via SQLAlchemy ORM).
- **Security:** JWT (JSON Web Tokens) for authentication, BCrypt for password hashing.
- **Cryptography:** ECDSA (ES256) signature generation for issuing unforgeable digital certificates.

### 4.3. Web Dashboard (Admin Interface)
- **Framework:** React with TypeScript and Vite.
- **Styling:** Tailwind CSS for a highly responsive, data-dense interface.
- **Functionality:** Provides Safety Managers with KPIs, compliance heatmaps, and a dedicated scanner portal to review incoming synced assessment data.

## 5. Key Modules Developed
1. **Fire & Explosion:** Users must locate an exit sign, identify a fire source, and select the correct type of extinguisher (e.g., CO2 vs. Powder) to put out virtual flames.
2. **Gas Leak Detection:** Simulates invisible hazards. The AR interface overlays a virtual gas monitor HUD; users must navigate away from an expanding semi-transparent 3D gas cloud.
3. **PPE Selection:** A virtual rack of Personal Protective Equipment (Hard Hat, Hi-Vis Vest, Safety Boots) is rendered. The worker must select the correct gear based on the designated hazard zone.

## 6. Impact and Feasibility
- **Cost-Effective:** Requires only standard Android smartphones (Android 10+) already owned by workers or provided affordably by the company; no expensive VR headsets required.
- **High Retention:** Kinesthetic learning through physical movement in AR significantly increases knowledge retention compared to multiple-choice quizzes.
- **Compliance Tracking:** Automates safety audits, removing paper trails and ensuring zero forged certificates on the worksite.

## 7. Conclusion
Suraksha-AR successfully demonstrates a production-ready blueprint for modernizing industrial safety. By combining cutting-edge spatial computing with rugged offline-first engineering, it ensures that every worker, regardless of their location or native language, is equipped with the practical knowledge to return home safely.
