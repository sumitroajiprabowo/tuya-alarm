# 🚀 Tuya Alarm Control API (Singapore)

Quick guide to running the Tuya Alarm Control API with Flask.

## ⚡ Setup

### 1. Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```
Fill in `.env`:
```ini
TUYA_ACCESS_ID=your_access_id
TUYA_ACCESS_SECRET=your_access_secret
TUYA_ENDPOINT=https://openapi-sg.iotbing.com
FLASK_PORT=5000
```

### 2. Run with Docker (Recommended)
Ensure Docker Desktop is running.

```bash
# Build and Run
make compose-up

# View Logs
make compose-logs

# Stop
make compose-down
```

### 3. Run Locally (Alternative)
```bash
# Install dependencies
make install

# Run server
make run
```

The server will run at `http://localhost:5000` (default).

---

## 🎯 Basic Usage

Replace `YOUR_DEVICE_ID` with your device ID.

### Health Check
```bash
curl http://localhost:5000/health
```

### Check Status
```bash
curl http://localhost:5000/api/device/YOUR_DEVICE_ID/status
```

### Activate Alarm (SOS)
```bash
curl -X POST http://localhost:5000/api/device/YOUR_DEVICE_ID/alarm/activate
```

### Deactivate Alarm
```bash
curl -X POST http://localhost:5000/api/device/YOUR_DEVICE_ID/alarm/deactivate
```

### Apply Preset
```bash
# Away (Leaving Home)
curl -X POST http://localhost:5000/api/device/YOUR_DEVICE_ID/preset/away

# Night (Sleeping)
curl -X POST http://localhost:5000/api/device/YOUR_DEVICE_ID/preset/night

# Home (At Home)
curl -X POST http://localhost:5000/api/device/YOUR_DEVICE_ID/preset/home
```

---

## 📚 Documentation

See [doc.md](doc.md) for complete API documentation.