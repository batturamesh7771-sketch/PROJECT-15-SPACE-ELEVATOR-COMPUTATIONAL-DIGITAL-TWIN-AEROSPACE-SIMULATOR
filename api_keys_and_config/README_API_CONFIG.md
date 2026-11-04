# Multi-API Telemetry & AI MoE Autopilot Configuration Guide

This Space Elevator Digital Twin integrates **5 Large Language Model APIs** for autonomous decision-making and **4 Live Planetary Meteorological & Ephemeris APIs** for 1:1 real-time Earth synchronization.

## 1. 5-LLM Mixture of Experts (MoE) Architecture
- **Model A (Google Gemini)**: Real-time high-speed telemetry ingestion ($1000\text{ ms}$ interval).
- **Model B (Anthropic Claude)**: Structural continuum mechanics & Pearson cable integrity.
- **Model C (OpenAI GPT-4o)**: Executive Mission Commander (balances transit speed vs. risk).
- **Model D (DeepSeek-R1)**: Numerical error residual & mathematical redundancy verifier.
- **Model E (Mistral Large)**: Hard safety constraint & Byzantine consensus auditor.

## 2. 1:1 Live Earth Synchronization APIs
- **OpenWeatherMap & WeatherAPI**: Real-time atmospheric conditions (wind shear, temperature, air density) at the Galapagos Sea-Anchor Base ($0.00^\circ\text{ N}, 90.00^\circ\text{ W}$).
- **OpenEphemeris & Le Système Solaire**: Real-time Earth axial tilt ($23.44^\circ$), GMST rotation, and dynamic solar illumination vector mapping the true day/night terminator.

## 3. Setting Up Your Local `.env`
Copy `.env.template` to `backend/.env` and insert your API credentials:
```bash
cp api_keys_and_config/.env.template backend/.env
```
