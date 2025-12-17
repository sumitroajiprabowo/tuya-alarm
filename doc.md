# 📘 API Documentation - Flask Version (Singapore)

Complete REST API for Tuya Alarm Control using Flask - Singapore Data Center.

---

## 🚀 Quick Start

### Base URL
```
http://localhost:5000
```
*(Default port is 5000, can be changed in `.env`)*

### Endpoints List

| Method | Endpoint | Description |
|--------|----------|-----------|
| GET | `/` | API info |
| GET | `/health` | Health check (Simple) |
| GET | `/credentials` | Tuya Connectivity Check |
| GET | `/api/devices` | List devices |
| GET | `/api/device/{id}` | Device info |
| GET | `/api/device/{id}/status` | Device status |
| POST | `/api/device/{id}/commands` | Send commands |
| POST | `/api/device/{id}/alarm/activate` | Activate alarm |
| POST | `/api/device/{id}/alarm/deactivate` | Deactivate alarm |
| POST | `/api/device/{id}/volume/{level}` | Set volume |
| POST | `/api/device/{id}/brightness/{level}` | Set brightness |
| POST | `/api/device/{id}/mode/{mode}` | Set mode |
| POST | `/api/device/{id}/duration/{seconds}` | Set duration |
| POST | `/api/device/{id}/preset/{name}` | Apply preset |

---

## 📖 Endpoint Details

### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "data": {
    "status": "healthy",
    "service": "tuya-alarm-api"
  },
  "meta": {
    "timestamp": "2024-11-29T...",
    "request_id": "..."
  }
}
```

### 2. Credentials Check
```http
GET /credentials
```
**Response:**
```json
{
  "data": {
    "status": "healthy",
    "tuya_api": "connected",
    "data_center": "Singapore",
    "endpoint": "https://openapi.tuyaus.com"
  },
  "meta": {
    "timestamp": "2024-11-29T...",
    "request_id": "..."
  }
}
```

### 3. Get Device Status
```http
GET /api/device/{device_id}/status
```
**Response:**
```json
{
  "data": {
    "success": true,
    "result": { ... },
    "formatted_status": {
      "alarm_switch": false,
      "alarm_volume": "middle",
      "battery_percentage": 95,
      "battery_state": "high",
      "charge_state": false,
      "temper_alarm": false
    }
  },
  "meta": {
    "timestamp": "...",
    "request_id": "..."
  }
}
```

**cURL:**
```bash
curl http://localhost:5050/api/device/YOUR_DEVICE_ID/status
```

### 3. Activate Alarm
```http
POST /api/device/{device_id}/alarm/activate
```
**Response:**
```json
{
  "data": {
    "success": true,
    "result": true
  },
  "meta": { ... }
}
```

### 4. Error Response Example
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Endpoint /api/xxx not found",
    "status": 404,
    "details": {}
  },
  "meta": {
    "timestamp": "...",
    "request_id": "..."
  }
}
```

### 4. Deactivate Alarm
```http
POST /api/device/{device_id}/alarm/deactivate
```
**cURL:**
```bash
curl -X POST http://localhost:5000/api/device/YOUR_DEVICE_ID/alarm/deactivate
```

### 5. Apply Preset
```http
POST /api/device/{device_id}/preset/{preset_name}
```
**Presets:** `home`, `away`, `night`, `silent`, `test`

**cURL:**
```bash
curl -X POST http://localhost:5000/api/device/YOUR_DEVICE_ID/preset/away
```

---

## 🐍 Python Client Example

```python
import requests

BASE_URL = "http://localhost:5000"
DEVICE_ID = "YOUR_DEVICE_ID"

class TuyaAlarmClient:
    def __init__(self, base_url=BASE_URL, device_id=DEVICE_ID):
        self.base_url = base_url
        self.device_id = device_id
    
    def get_status(self):
        return requests.get(f"{self.base_url}/api/device/{self.device_id}/status").json()
    
    def activate_alarm(self):
        return requests.post(f"{self.base_url}/api/device/{self.device_id}/alarm/activate").json()

# Usage
client = TuyaAlarmClient()
print(client.get_status())
```

---

## 🔧 Configuration

Configuration is done via environment variables in the `.env` file.
**DO NOT** hardcode credentials in the code.

```ini
TUYA_ACCESS_ID=your_access_id
TUYA_ACCESS_SECRET=your_access_secret
TUYA_ENDPOINT=your_tuya_endpoint
FLASK_PORT=5000
```