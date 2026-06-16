# <div align="center">⚖️ BIASLENS: THE COMPLETE BLUEPRINT</div>

<div align="center">
  <img src="https://img.shields.io/badge/AI_FAIRNESS_AUDITOR-00f5ff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/GOOGLE_PROMPT_WARS-2026-7000ff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/POWERED_BY-NVIDIA_NIM-76B900?style=for-the-badge" />
</div>

---

## 👥 Development Team
* **🔹 Ayush Bhatnagar** — *Lead Developer / DevOps Engineer & Security Analyst*
* **🔹 Ansh Singh** — *Backend & AI/ML Architect*
* **🔹 Abhyuday Gautam** — *Data Researcher & Frontend, UI/UX Specialist*

---

## 🎯 Project Vision
**BiasLens** was built to solve a critical problem in Modern AI: **Unconscious Algorithmic Discrimination**. When datasets are used to train models for hiring, loans, or admissions, they often contain historical biases. BiasLens acts as a "cyber-x-ray" for data, exposing these biases before they harm real people.

---

## 🧠 The 9-Metric Fairness Core
We utilize **IBM AIF360** and **Fairlearn** to provide mathematical rigor. BiasLens doesn't just guess; it computes:

| Metric | Purpose |
| :--- | :--- |
| **Disparate Impact** | Checks if a protected group receives outcomes at < 80% of the majority group. |
| **Statistical Parity** | Measures the raw difference in outcome rates between demographics. |
| **Equal Opportunity** | Ensures "True Positive" rates are equal across groups. |
| **Average Odds** | Balances both false positives and true positives across groups. |
| **Theil Index** | Calculates individual vs. group benefit inequality. |
| **Individual Fairness** | Ensures similar individuals receive similar outcomes. |
| **Proxy Detection** | Identifies non-sensitive columns (like Zip Code) that hide bias. |
| **Predictive Parity** | Checks if model precision is consistent across groups. |
| **Calibration Score** | Ensures probability estimates are accurate for all segments. |

---

## 🏗️ Technical Architecture & Stack
### ☁️ In-Memory Processing (Zero-Storage)
BiasLens saves **0 bytes** of user data. Files are streamed as multipart forms, converted to Pandas DataFrames in RAM, audited, and cleared instantly. 
* **Maximum Privacy:** GDPR-ready by design.
* **Cost Efficiency:** $0 monthly storage cost.

### 🛠️ The Stack
`Python 3.11` • `FastAPI` • `NVIDIA NIM` • `Vercel` • `Render` • `Chart.js` • `Three.js` • `Firebase Auth`

---

## 🤖 NVIDIA NIM Integration
We integrated the **Llama-3.1-Nemotron-70B-Instruct** model via **NVIDIA NIM**. While the math engine provides raw scores, the AI provides the "Human Context"—generating a plain-English executive summary explaining the findings and offering mitigation strategies.

---

## 🚀 Evolution & Critical Fixes
- **The "Free-Tier" Pivot:** Migrated from Google Cloud to a custom Render-Vercel bridge to avoid billing mandates while maintaining elite performance.
- **CORS & Security:** Implemented specialized middleware for secure cross-origin communication.
- **Floating Cyber-UI:** Developed a custom Three.js animated background with `colorSpace` optimizations.

---

<div align="center">
  <p><i>Built with ❤️ for the future of Ethical AI.</i></p>
  <b>BIASLENS </b>
</div>
