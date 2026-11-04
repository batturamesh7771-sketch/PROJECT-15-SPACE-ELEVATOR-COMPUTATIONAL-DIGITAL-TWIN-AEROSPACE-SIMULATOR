# API & CONNECTOR INVENTORY
## SPACE ELEVATOR COMPUTATIONAL DIGITAL TWIN
**Document Identifier:** API-SE-2026-CONN-001  
**Version:** 3.0.0  
**Security Standard:** Strict Credential Masking & Local-First Architectural Integrity  

---

### 1. INTERNAL SERVICE CONNECTORS

| Connector ID | Source Module | Destination | Protocol | Port | Data Description | Security / Auth |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `CONN-INT-REST-01` | `dashboard_ui.js` | `server.py` | HTTP/REST | 8095 | Parameter configuration & batch FEA request | Local CORS (`*`) |
| `CONN-INT-WS-02` | `dashboard_ui.js` | `server.py` | WebSocket | 8095 | High-rate 10 Hz telemetry state stream | Localhost unencrypted |
| `CONN-INT-IPC-03` | `server.py` | `matlab.EXE` | Process Pipe | Host OS | Offline benchmark calculation batch job | Local process sandbox |
| `CONN-INT-IPC-04` | `server.py` | `ansys.exe` | APDL Script | Host OS | High-resolution structural deflection validation | Local process sandbox |
| `CONN-INT-IPC-05` | `server.py` | `GmatConsole.exe`| GMAT Script | Host OS | Gravitational n-body perturbation trajectory run | Local process sandbox |

---

### 2. EXTERNAL SCIENTIFIC DATA APIS (ROADMAP & MOCK STATUS)

| External API | Provider | Usage Purpose | Current Status | Credential Handling |
| :--- | :--- | :--- | :--- | :--- |
| **NASA JPL Horizons** | NASA / JPL | Ephemerides of Sun, Earth, Moon, and Planets | Local SPICE Kernel Fallback | Unauthenticated public API / masked |
| **NOAA Space Weather**| NOAA SWPC | Real-time solar wind flux, Kp index, proton events | Local US Standard / AP-8 Model | Public JSON endpoint / token-free |
| **ESA Space Debris** | ESA DISCOS | LEO/GEO trackable orbital debris population | Local NASA ORDEM 3.1 Model | Token required (Stored in local `.env`) |

*Security Assurance:* No hardcoded API keys, private credentials, or unauthorized external data transmissions exist within the codebase.
