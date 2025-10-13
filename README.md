# 🚗 ParkSmart – Cloud-Based Smart Parking System

## 🏁 Introduction
**ParkSmart** is a cloud-powered parking management system designed to simplify the process of finding, booking, and managing parking spaces in real-time.  
The application leverages **AWS RDS** for reliable cloud-based data storage and integrates **automated email services** for billing and reporting.  

With an intuitive interface, ParkSmart ensures a smooth experience for both parking lot administrators and users, enabling smart, efficient, and paperless parking management.

---

## ✨ Features Implemented
- 🔐 **User Authentication** – Secure login and registration.
- 🅿️ **Real-Time Parking Availability** – Displays available and booked slots dynamically.
- 📅 **Parking Slot Booking System** – Users can reserve parking spaces for a chosen time.
- 💳 **Automated Billing System** – On successful booking, a bill is generated and sent via email.
- 📧 **Email Integration** – Uses SMTP-based mail service for bill generation and reporting.
- ☁️ **Cloud Database (AWS RDS)** – All user and booking data are securely stored in AWS RDS.
- 🖥️ **Responsive Web UI** – Works seamlessly on desktop and mobile browsers.
- 🧩 **Environment Variable Management** – Sensitive credentials (like AWS credentials, DB passwords) stored securely in `.env`.

---

## 🧰 Tech Stack

| Category              | Technology Used              |
|------------------------|------------------------------|
| **Frontend**           | HTML, CSS, JavaScript        |
| **Backend**            | Python (Flask)               |
| **Database**           | AWS RDS (MySQL)              |
| **Email Service**      | Python `smtplib` + Gmail SMTP|
| **Version Control**    | Git & GitHub                 |
| **Environment Mgmt.**  | Python Virtual Environment (`venv`) |
| **Cloud Provider**     | Amazon Web Services (AWS)    |

---

## ⚙️ How to Run the Project Locally

Follow these steps to get **ParkSmart** running on your local machine:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/NinadGawali/ParkSmart.git
cd ParkSmart
```
### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
```

### 3️⃣ Activate the Virtual Environment

#### Windows (PowerShell):
```bash
venv\Scripts\activate
```

#### macOS/Linux:
```bash
source venv/bin/activate
```

### 4️⃣ Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Set Up AWS RDS Database

1. **Create an AWS RDS MySQL instance**
   - Go to [AWS Management Console](https://aws.amazon.com/console/).
   - Navigate to **RDS → Databases → Create database**.
   - Choose **MySQL** as the engine type.
   - Select configuration options (Free Tier if available).
   - Create the instance and wait for it to be available.

2. **Note down the following details:**
   - 🏷️ **Hostname (Endpoint)**
   - 🔢 **Port**
   - 🗄️ **Database Name**
   - 👤 **Username**
   - 🔒 **Password**

3. **Configure Security Group:**
   - Open your RDS instance in the AWS console.
   - Under **Connectivity & Security**, find your **VPC Security Group** and click on it.
   - Add an **Inbound Rule**:
     - **Type:** MySQL/Aurora  
     - **Protocol:** TCP  
     - **Port Range:** `3306`  
     - **Source:** Your **current public IP (e.g., 106.xxx.xxx.xxx/32)**  
   - Click **Save Rules**.

✅ Once done, your local system will be able to connect to the RDS database securely.

### 6️⃣ Configure the .env File

Create a .env file in your project root and add the following values:
```bash
DB_HOST=<your_aws_rds_endpoint>
DB_USER=<your_username>
DB_PASSWORD=<your_password>
DB_NAME=<your_database_name>
EMAIL_USER=<your_email_id>
EMAIL_PASS=<your_email_password_or_app_password>
```

### 7️⃣ Run the Application
```bash
python app.py
```
The app will start running on:
```bash
http://127.0.0.1:5000/
```

#### 🎥 Output Video Sample


https://github.com/user-attachments/assets/d7ecae1a-0d53-4709-831b-d684a885282f


## 🧑‍💻 Author

**Ninad Gawali**  
🔗 [GitHub Profile](https://github.com/NinadGawali)

### 📝 License

This project is licensed under the MIT License – see the LICENSE file for details.

### 🌟 Show Your Support

If you found this project helpful, please ⭐ the repository and share it with others!
