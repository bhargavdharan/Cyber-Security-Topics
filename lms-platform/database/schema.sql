-- Cybersecurity Learning Platform Database Schema
-- Run: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS cybersec_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cybersec_platform;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role ENUM('student', 'admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Topics table (15 cybersecurity topics)
CREATE TABLE IF NOT EXISTS topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    category VARCHAR(50),
    order_num INT DEFAULT 0,
    icon VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User progress tracking
CREATE TABLE IF NOT EXISTS user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    topic_id INT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completion_percentage INT DEFAULT 0 CHECK (completion_percentage BETWEEN 0 AND 100),
    simulations_completed INT DEFAULT 0,
    quizzes_taken INT DEFAULT 0,
    avg_quiz_score DECIMAL(5,2) DEFAULT 0,
    last_accessed TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_topic (user_id, topic_id)
);

-- Quiz results
CREATE TABLE IF NOT EXISTS quiz_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    topic_id INT NOT NULL,
    quiz_name VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    total_questions INT NOT NULL,
    answers_json JSON,
    taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

-- Simulation execution logs
CREATE TABLE IF NOT EXISTS simulation_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    topic_id INT NOT NULL,
    simulation_name VARCHAR(100) NOT NULL,
    input_params JSON,
    result_summary TEXT,
    result_json JSON,
    execution_time_ms INT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

-- Insert the 15 cybersecurity topics
INSERT INTO topics (title, slug, description, category, order_num, icon) VALUES
('Introduction to Cybersecurity', 'intro-to-cybersecurity', 'Fundamentals including CIA Triad, threats, and security principles', 'Fundamentals', 1, 'shield'),
('Networking Fundamentals', 'networking-fundamentals', 'TCP/IP, IP addressing, subnetting, network devices and protocols', 'Fundamentals', 2, 'network'),
('Operating Systems and Security', 'operating-systems-security', 'Windows, Linux, macOS security features and hardening', 'Fundamentals', 3, 'desktop'),
('Cryptography', 'cryptography', 'Encryption, hashing, digital signatures, and certificates', 'Fundamentals', 4, 'lock'),
('Web Application Security', 'web-application-security', 'OWASP Top 10, secure architecture, WAFs', 'Application Security', 5, 'globe'),
('Network Security', 'network-security', 'Firewalls, IDS/IPS, VPNs, wireless security', 'Infrastructure', 6, 'firewall'),
('Security Assessment and Testing', 'security-assessment-testing', 'Vulnerability assessment, penetration testing, ethical hacking', 'Offensive Security', 7, 'search'),
('Incident Response and Forensics', 'incident-response-forensics', 'IR frameworks, digital forensics, malware analysis', 'Defense', 8, 'ambulance'),
('Cloud Security', 'cloud-security', 'Cloud models, IAM, encryption, security architecture', 'Cloud', 9, 'cloud'),
('Mobile Security', 'mobile-security', 'Device security, app security, MDM, secure development', 'Mobile', 10, 'mobile'),
('Threat Intelligence and Security Analytics', 'threat-intelligence', 'Threat intel sources, SIEM, log analysis, hunting', 'Intelligence', 11, 'brain'),
('Industrial Control Systems Security', 'ics-security', 'SCADA, PLCs, OT security, critical infrastructure', 'ICS/OT', 12, 'industry'),
('Advanced Persistent Threats', 'advanced-persistent-threats', 'APT lifecycle, detection, malware analysis, case studies', 'Advanced', 13, 'user-secret'),
('Secure Software Development', 'secure-software-development', 'Secure coding, SDL, threat modeling, DevSecOps', 'Development', 14, 'code'),
('Emerging Technologies in Cybersecurity', 'emerging-technologies', 'IoT, AI/ML, blockchain, quantum cryptography', 'Emerging', 15, 'rocket');
