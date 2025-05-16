# Cloud-Native Web Application

This project is a cloud-native web application featuring a Python backend (Flask/Django), PostgreSQL on Amazon RDS, and optional frontend deployment via Elastic Beanstalk. It follows best practices in scalability, security, and cloud resource management using AWS services.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Environment Variables](#environment-variables)
- [Deployment Guide](#deployment-guide)
- [Security Configuration](#security-configuration)
- [License](#license)

---

## Features

- FASTAPI built with Python (Flask or Django)
- Relational database hosted on Amazon RDS (PostgreSQL)
- Dockerized backend for scalable deployment
- AWS EC2-based backend hosting
- Optional frontend (React/Vue/Angular) via Elastic Beanstalk or S3
- Secure key and credential management using `.env`

---

## Project Structure

```
project-root/
│
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   │   └── schema.py
│   │   ├── main.py / app.py
│   │   └── ...
│   ├── Dockerfile
│   ├── .env
│   └── requirements.txt
│
├── frontend/                 # Optional
│   └── (React/Angular/Vue)
│
├── schema.sql                # Database schema
└── README.md
```

---

## Tech Stack

- **Backend**: Python 3.x (Flask or Django)
- **Database**: PostgreSQL (Amazon RDS)
- **Containerization**: Docker
- **Hosting**: AWS EC2 (for backend), S3/Elastic Beanstalk (for frontend)
- **Other AWS Services**: IAM, VPC, Security Groups, Route 53 (optional)

---

## Environment Variables

Create a `.env` file inside the `backend/` directory with the following:

```
DATABASE_URL=postgresql://Hamza:Pakistanarmy1@mydb.cluster-c4ngqk4m6bi3.us-east-1.rds.amazonaws.com:5432/postgres
SECRET_KEY=your_super_secret_key
DB_HOST=mydb.cluster-c4ngqk4m6bi3.us-east-1.rds.amazonaws.com
DB_NAME=postgres
DB_USER=Hamza
DB_PORT=5432
DB_PASSWORD=Pakistanarmy1
```

---

## Deployment Guide

### 1. Clone Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name/backend
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Launch EC2 and RDS

- Create a PostgreSQL RDS instance.
- Launch a t2.micro EC2 instance using Amazon Linux 2 AMI.

### 4. Configure Security Groups

#### RDS Security Group:
- Inbound:
  - PostgreSQL (port 5432) from EC2’s security group or your IP.

#### EC2 Security Group:
- Inbound:
  - SSH (port 22) from your IP.
  - HTTP (port 80), HTTPS (443) from 0.0.0.0/0.
  - Custom TCP (e.g., 8000) for backend if needed.

### 5. Connect EC2 to RDS

SSH into EC2 and run:

```bash
sudo yum update -y
sudo amazon-linux-extras enable postgresql14
sudo yum install postgresql -y

psql -h myapp-db.abcdef123456.us-east-1.rds.amazonaws.com -U Hamza -d postgres
```

### 6. Run SQL Schema

Inside `psql`, execute:

```sql
\i /home/ec2-user/path/to/schema.sql
```

Or paste SQL manually.

### 7. Dockerize and Run Backend

**Dockerfile** example:

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

Build and run container:

```bash
docker build -t backend-app .
docker run -d -p 8000:8000 --env-file .env backend-app
```

### 8. Frontend Deployment (Optional)

Deploy to Elastic Beanstalk or S3 as needed. Update backend API URLs accordingly.

---

## Security Configuration

- All secrets managed in `.env` (never commit to git)
- RDS access restricted to EC2 via security groups
- EC2 access via SSH from trusted IPs
- IAM roles created with least privilege access
- Optional: Use Route 53 and ACM for custom domain and HTTPS
