# VNSFT

**VNSFT** (VIN Software Tool) is a specialized Python application designed for auction vehicle identification and reconditioning workflow tracking. It connects directly to Manheim’s AS400 system via the Manheim RECON API, providing real-time VIN scan processing and status updates.

## 🚗 Purpose

- Accurately pull vehicle data directly from the Manheim AS400 database.
- Identify and verify auction vehicles by VIN scan.
- Check vehicle status, type of reconditioning work required, and location details.
- Track cycle times between vehicle scans to monitor workflow efficiency.

## 🔗 How It Works

1. **VIN Scan:**  
   Employees or managers scan a vehicle’s VIN barcode.

2. **AS400 Lookup:**  
   The system queries Manheim’s AS400 system through the RECON API to pull relevant vehicle details.

3. **Status & Work Type:**  
   Retrieves the vehicle’s current status and the specific type of work needed (e.g., detail, body shop, mechanical).

4. **Cycle Time Tracking:**  
   Logs the timestamps between scans to calculate total time spent in each phase, enabling performance metrics and workflow improvements.

## ⚙️ Core Features

- ✅ Real-time VIN scan and validation.
- ✅ Integration with Manheim’s RECON API for up-to-date status.
- ✅ Detailed tracking of work types and locations.
- ✅ Cycle time analysis for operational efficiency.
- ✅ Future support for discrepancy reports and manager dashboards.

## 🔒 Security & Compliance

This tool is designed to work within Manheim’s vendor and security guidelines, ensuring data access complies with auction security protocols.

## 📈 Roadmap

Planned future enhancements include:
- OCR scanning of VINs for mobile use.
- Discrepancy reporting to flag vehicles with mismatched work orders.
- Team and employee performance dashboards.

## 👨‍💻 Author

Brandon Wynn  
brandon.wynn@me.com

---

**Where efficiency meets accountability — every VIN, every scan.**
