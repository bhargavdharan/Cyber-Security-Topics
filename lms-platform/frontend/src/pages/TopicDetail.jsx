import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import SimulationRunner from '../components/SimulationRunner';
import QuizTaker from '../components/QuizTaker';

// Quiz questions for all 15 topics
const topicQuizzes = {
  'intro-to-cybersecurity': [
    {
      question: "What does the 'C' in CIA Triad stand for?",
      options: ["Control", "Confidentiality", "Cybersecurity", "Compliance"],
      correct: "Confidentiality",
      explanation: "The CIA Triad stands for Confidentiality, Integrity, and Availability."
    },
    {
      question: "Which principle ensures data is not modified by unauthorized parties?",
      options: ["Availability", "Confidentiality", "Integrity", "Authentication"],
      correct: "Integrity",
      explanation: "Integrity ensures that data is accurate and has not been tampered with."
    },
    {
      question: "What is the primary goal of social engineering attacks?",
      options: ["Destroy hardware", "Manipulate people into revealing information", "Encrypt files", "Slow down networks"],
      correct: "Manipulate people into revealing information",
      explanation: "Social engineering targets human psychology to extract sensitive information."
    },
    {
      question: "Which of the following is NOT a type of malware?",
      options: ["Virus", "Worm", "Firewall", "Ransomware"],
      correct: "Firewall",
      explanation: "A firewall is a security device, not malware. Viruses, worms, and ransomware are all types of malware."
    }
  ],
  'networking-fundamentals': [
    {
      question: "What is the default port for HTTP?",
      options: ["21", "80", "443", "8080"],
      correct: "80",
      explanation: "HTTP uses port 80 by default, while HTTPS uses port 443."
    },
    {
      question: "Which protocol translates domain names to IP addresses?",
      options: ["DHCP", "DNS", "FTP", "SMTP"],
      correct: "DNS",
      explanation: "DNS (Domain Name System) resolves domain names to IP addresses."
    },
    {
      question: "What does TCP stand for?",
      options: ["Transmission Control Protocol", "Transfer Connection Protocol", "Transport Communication Protocol", "Total Control Path"],
      correct: "Transmission Control Protocol",
      explanation: "TCP is a connection-oriented protocol that ensures reliable data delivery."
    },
    {
      question: "Which layer of the OSI model handles routing?",
      options: ["Transport", "Network", "Data Link", "Session"],
      correct: "Network",
      explanation: "Layer 3 (Network Layer) handles logical addressing and routing between networks."
    }
  ],
  'operating-systems-security': [
    {
      question: "What does DAC stand for in access control?",
      options: ["Digital Access Control", "Discretionary Access Control", "Dynamic Access Control", "Distributed Access Control"],
      correct: "Discretionary Access Control",
      explanation: "DAC allows resource owners to decide who can access their resources."
    },
    {
      question: "Which Linux command changes file permissions?",
      options: ["chown", "chmod", "chgrp", "perms"],
      correct: "chmod",
      explanation: "chmod changes the permissions of a file or directory."
    },
    {
      question: "What is the principle of least privilege?",
      options: ["Grant maximum access", "Grant minimum necessary access", "Allow root access to all", "Disable all permissions"],
      correct: "Grant minimum necessary access",
      explanation: "Users should only have the minimum access necessary to perform their job functions."
    },
    {
      question: "Which Windows feature provides memory protection?",
      options: ["UAC", "ASLR", "BitLocker", "Defender"],
      correct: "ASLR",
      explanation: "ASLR (Address Space Layout Randomization) randomizes memory locations to prevent exploitation."
    }
  ],
  'cryptography': [
    {
      question: "Which encryption type uses the same key for encryption and decryption?",
      options: ["Asymmetric", "Symmetric", "Hashing", "Quantum"],
      correct: "Symmetric",
      explanation: "Symmetric encryption uses a single shared secret key."
    },
    {
      question: "What is the primary purpose of a hash function?",
      options: ["Encrypt data", "Verify data integrity", "Generate keys", "Compress files"],
      correct: "Verify data integrity",
      explanation: "Hash functions produce a fixed-size output to verify data integrity."
    },
    {
      question: "Which algorithm is considered the standard for symmetric encryption?",
      options: ["RSA", "AES", "MD5", "SHA-1"],
      correct: "AES",
      explanation: "AES (Advanced Encryption Standard) is the most widely used symmetric encryption algorithm."
    },
    {
      question: "In asymmetric cryptography, which key is shared publicly?",
      options: ["Private key", "Public key", "Session key", "Master key"],
      correct: "Public key",
      explanation: "The public key can be freely distributed, while the private key must be kept secret."
    }
  ],
  'web-application-security': [
    {
      question: "What does XSS stand for?",
      options: ["XML Security System", "Cross-Site Scripting", "Extended Security Standard", "Xenon Security Suite"],
      correct: "Cross-Site Scripting",
      explanation: "XSS allows attackers to inject malicious scripts into web pages viewed by other users."
    },
    {
      question: "Which OWASP risk is ranked #1 in the Top 10?",
      options: ["Broken Access Control", "Injection", "Cryptographic Failures", "Insecure Design"],
      correct: "Broken Access Control",
      explanation: "As of OWASP Top 10 2021, Broken Access Control is the #1 risk."
    },
    {
      question: "What is SQL Injection?",
      options: ["A database backup method", "An attack that injects malicious SQL code", "A query optimization technique", "A type of firewall"],
      correct: "An attack that injects malicious SQL code",
      explanation: "SQL Injection exploits vulnerabilities in database queries to execute unauthorized commands."
    },
    {
      question: "Which HTTP header helps prevent XSS attacks?",
      options: ["X-Frame-Options", "Content-Security-Policy", "X-Powered-By", "Accept-Encoding"],
      correct: "Content-Security-Policy",
      explanation: "CSP restricts the sources from which content can be loaded, mitigating XSS attacks."
    }
  ],
  'network-security': [
    {
      question: "What is the primary purpose of a firewall?",
      options: ["Detect viruses", "Control network traffic", "Encrypt data", "Backup files"],
      correct: "Control network traffic",
      explanation: "Firewalls monitor and control incoming and outgoing network traffic based on security rules."
    },
    {
      question: "What does an IDS do?",
      options: ["Blocks attacks", "Detects and alerts on intrusions", "Encrypts traffic", "Manages passwords"],
      correct: "Detects and alerts on intrusions",
      explanation: "An Intrusion Detection System monitors network traffic for suspicious activity and alerts administrators."
    },
    {
      question: "What is the difference between IDS and IPS?",
      options: ["IDS is faster", "IPS can block traffic, IDS only alerts", "IDS encrypts data", "They are the same"],
      correct: "IPS can block traffic, IDS only alerts",
      explanation: "IPS (Intrusion Prevention System) actively blocks threats, while IDS only detects and alerts."
    },
    {
      question: "Which VPN protocol is known for speed and security?",
      options: ["PPTP", "WireGuard", "L2TP", "WEP"],
      correct: "WireGuard",
      explanation: "WireGuard is a modern VPN protocol known for its simplicity, speed, and strong cryptography."
    }
  ],
  'security-assessment-testing': [
    {
      question: "What is the main goal of penetration testing?",
      options: ["Install antivirus", "Identify and exploit vulnerabilities", "Monitor network traffic", "Train employees"],
      correct: "Identify and exploit vulnerabilities",
      explanation: "Penetration testing simulates attacks to identify security weaknesses before real attackers do."
    },
    {
      question: "What is a vulnerability scanner used for?",
      options: ["Hack websites", "Identify known security weaknesses", "Encrypt files", "Block DDoS attacks"],
      correct: "Identify known security weaknesses",
      explanation: "Vulnerability scanners automate the detection of known security flaws in systems and applications."
    },
    {
      question: "What does 'black box' testing mean?",
      options: ["Testing with full source code access", "Testing with no prior knowledge", "Testing at night", "Testing only hardware"],
      correct: "Testing with no prior knowledge",
      explanation: "Black box testing simulates an external attacker with no internal knowledge of the system."
    },
    {
      question: "Which tool is commonly used for web app security scanning?",
      options: ["Nmap", "Burp Suite", "Wireshark", "Metasploit"],
      correct: "Burp Suite",
      explanation: "Burp Suite is a popular platform for performing security testing of web applications."
    }
  ],
  'incident-response-forensics': [
    {
      question: "What is the first step in incident response?",
      options: ["Eradication", "Preparation", "Recovery", "Lessons Learned"],
      correct: "Preparation",
      explanation: "The NIST incident response lifecycle begins with Preparation."
    },
    {
      question: "What does a SIEM system do?",
      options: ["Block malware", "Collect and analyze security logs", "Encrypt emails", "Manage passwords"],
      correct: "Collect and analyze security logs",
      explanation: "SIEM (Security Information and Event Management) aggregates and analyzes security logs in real-time."
    },
    {
      question: "What is chain of custody in forensics?",
      options: ["A network topology", "Documentation of evidence handling", "A type of encryption", "A password policy"],
      correct: "Documentation of evidence handling",
      explanation: "Chain of custody documents every person who handled evidence to maintain its integrity in court."
    },
    {
      question: "Which type of malware hides in the boot sector?",
      options: ["Ransomware", "Rootkit", "Bootkit", "Spyware"],
      correct: "Bootkit",
      explanation: "A bootkit infects the Master Boot Record (MBR) to load before the operating system."
    }
  ],
  'cloud-security': [
    {
      question: "What is the shared responsibility model in cloud security?",
      options: ["Cloud provider secures everything", "Security is shared between provider and customer", "Only the customer is responsible", "Only the provider is responsible"],
      correct: "Security is shared between provider and customer",
      explanation: "The cloud provider secures the infrastructure, while the customer secures their data and applications."
    },
    {
      question: "What does CASB stand for?",
      options: ["Cloud Access Security Broker", "Central Authentication Service Bus", "Cloud Application Security Boundary", "Content Access Security Block"],
      correct: "Cloud Access Security Broker",
      explanation: "CASB sits between cloud service users and providers to enforce security policies."
    },
    {
      question: "Which AWS service helps monitor API calls?",
      options: ["CloudWatch", "CloudTrail", "GuardDuty", "Inspector"],
      correct: "CloudTrail",
      explanation: "AWS CloudTrail records API calls and account activity for auditing and compliance."
    },
    {
      question: "What is data sovereignty?",
      options: ["Data encryption method", "Legal requirement that data stays in certain jurisdictions", "Data backup strategy", "Cloud migration technique"],
      correct: "Legal requirement that data stays in certain jurisdictions",
      explanation: "Data sovereignty laws require that data about citizens remain within the country's borders."
    }
  ],
  'mobile-security': [
    {
      question: "What is jailbreaking?",
      options: ["Installing antivirus", "Removing manufacturer restrictions on iOS", "Encrypting data", "Creating backups"],
      correct: "Removing manufacturer restrictions on iOS",
      explanation: "Jailbreaking removes software restrictions on iOS devices to gain root access."
    },
    {
      question: "Which Android permission is most dangerous?",
      options: ["INTERNET", "READ_CONTACTS", "VIBRATE", "BLUETOOTH"],
      correct: "READ_CONTACTS",
      explanation: "READ_CONTACTS allows access to personal contact information, posing significant privacy risks."
    },
    {
      question: "What is an MDM solution?",
      options: ["Malware Detection Module", "Mobile Device Management", "Multi-Domain Monitor", "Memory Dump Manager"],
      correct: "Mobile Device Management",
      explanation: "MDM solutions allow organizations to manage, monitor, and secure mobile devices remotely."
    },
    {
      question: "Which attack targets NFC mobile payments?",
      options: ["Phishing", "Eavesdropping", "Skimming", "Spoofing"],
      correct: "Eavesdropping",
      explanation: "NFC eavesdropping intercepts radio signals between a mobile device and a payment terminal."
    }
  ],
  'threat-intelligence': [
    {
      question: "What is an IOC?",
      options: ["International Olympic Committee", "Indicator of Compromise", "Internet Operation Center", "Intrusion Operation Code"],
      correct: "Indicator of Compromise",
      explanation: "IOCs are forensic artifacts that indicate a potential intrusion on a network or system."
    },
    {
      question: "What does TTP stand for in threat intelligence?",
      options: ["Tactics, Techniques, and Procedures", "Threat Tracking Protocol", "Traffic Transfer Point", "Targeted Threat Prevention"],
      correct: "Tactics, Techniques, and Procedures",
      explanation: "TTPs describe the behavior and methods used by threat actors."
    },
    {
      question: "What is the purpose of a threat feed?",
      options: ["Slow down networks", "Share real-time threat information", "Encrypt communications", "Block all traffic"],
      correct: "Share real-time threat information",
      explanation: "Threat feeds provide continuously updated information about emerging threats and IOCs."
    },
    {
      question: "Which framework is used for structured threat information?",
      options: ["MITRE ATT&CK", "STIX/TAXII", "NIST CSF", "ISO 27001"],
      correct: "STIX/TAXII",
      explanation: "STIX (Structured Threat Information Expression) and TAXII (Trusted Automated Exchange of Intelligence Information) standardize threat data sharing."
    }
  ],
  'ics-security': [
    {
      question: "What does ICS stand for?",
      options: ["Internet Control System", "Industrial Control System", "Internal Communication Standard", "Integrated Cyber Security"],
      correct: "Industrial Control System",
      explanation: "ICS refers to systems used to control industrial processes like manufacturing and power generation."
    },
    {
      question: "What is SCADA?",
      options: ["A type of firewall", "Supervisory Control and Data Acquisition", "A malware scanner", "A cloud service"],
      correct: "Supervisory Control and Data Acquisition",
      explanation: "SCADA is a type of ICS that controls and monitors industrial processes across large geographical areas."
    },
    {
      question: "Why are ICS systems difficult to patch?",
      options: ["They don't need patches", "Downtime can be dangerous/expensive", "They are always air-gapped", "They use proprietary protocols only"],
      correct: "Downtime can be dangerous/expensive",
      explanation: "ICS systems often run critical infrastructure where downtime can cause physical harm or massive costs."
    },
    {
      question: "Which malware targeted Iranian nuclear facilities?",
      options: ["WannaCry", "Stuxnet", "NotPetya", "Conficker"],
      correct: "Stuxnet",
      explanation: "Stuxnet was a sophisticated worm that targeted Siemens SCADA systems at Iran's Natanz nuclear facility."
    }
  ],
  'advanced-persistent-threats': [
    {
      question: "What defines an APT?",
      options: ["Quick opportunistic attacks", "Long-term targeted attacks by skilled adversaries", "Automated scanning tools", "Denial of service attacks"],
      correct: "Long-term targeted attacks by skilled adversaries",
      explanation: "APTs are sophisticated, prolonged attacks where intruders establish a long-term presence."
    },
    {
      question: "What is the APT kill chain?",
      options: ["A hardware device", "A sequence of attack stages", "An antivirus scanner", "A network protocol"],
      correct: "A sequence of attack stages",
      explanation: "The kill chain describes the stages of a cyberattack from reconnaissance to exfiltration."
    },
    {
      question: "What is lateral movement?",
      options: ["Moving servers physically", "Spreading through a network after initial access", "DDoS attack pattern", "Data encryption method"],
      correct: "Spreading through a network after initial access",
      explanation: "Lateral movement is the technique used by attackers to spread from an initial compromised system to others."
    },
    {
      question: "What is a watering hole attack?",
      options: ["A DDoS technique", "Compromising websites frequented by targets", "A phishing email", "A hardware exploit"],
      correct: "Compromising websites frequented by targets",
      explanation: "Watering hole attacks infect websites that specific targets are known to visit regularly."
    }
  ],
  'secure-software-development': [
    {
      question: "What is the purpose of input validation?",
      options: ["Speed up processing", "Ensure data meets expected format", "Encrypt data", "Compress files"],
      correct: "Ensure data meets expected format",
      explanation: "Input validation ensures that only properly formed data enters the application workflow."
    },
    {
      question: "What is SAST?",
      options: ["Static Application Security Testing", "System Authorization Security Token", "Secure Access Storage Technology", "Software Authentication Standard Test"],
      correct: "Static Application Security Testing",
      explanation: "SAST analyzes source code for security vulnerabilities without executing the program."
    },
    {
      question: "What does OWASP SAMM help with?",
      options: ["Network monitoring", "Software Assurance Maturity Model", "Malware detection", "Password management"],
      correct: "Software Assurance Maturity Model",
      explanation: "OWASP SAMM helps organizations formulate and implement a tailored software security strategy."
    },
    {
      question: "What is the safest way to store passwords?",
      options: ["Plain text", "Base64 encoding", "bcrypt/Argon2 hashing with salt", "MD5 hashing"],
      correct: "bcrypt/Argon2 hashing with salt",
      explanation: "Modern password hashing algorithms like bcrypt and Argon2 are designed to be slow and use salts to resist attacks."
    }
  ],
  'emerging-technologies': [
    {
      question: "What is the biggest security risk of IoT devices?",
      options: ["They are too fast", "Weak/default credentials and poor update mechanisms", "They use too much power", "They are too expensive"],
      correct: "Weak/default credentials and poor update mechanisms",
      explanation: "Many IoT devices ship with default passwords and lack secure update mechanisms."
    },
    {
      question: "What does post-quantum cryptography protect against?",
      options: ["Classical computers", "Quantum computers breaking current encryption", "Physical theft", "Social engineering"],
      correct: "Quantum computers breaking current encryption",
      explanation: "Post-quantum cryptography develops algorithms resistant to attacks by quantum computers."
    },
    {
      question: "What is a 51% attack in blockchain?",
      options: ["A DDoS attack", "Controlling majority of network hashing power", "A phishing scheme", "A firewall bypass"],
      correct: "Controlling majority of network hashing power",
      explanation: "A 51% attack occurs when a single entity controls the majority of a blockchain's mining power."
    },
    {
      question: "What is homomorphic encryption?",
      options: ["A type of firewall", "Computing on encrypted data without decrypting", "A password manager", "A blockchain protocol"],
      correct: "Computing on encrypted data without decrypting",
      explanation: "Homomorphic encryption allows computations to be performed on ciphertext without decrypting it first."
    }
  ]
};

// Simulation mappings for each topic
const topicSimulations = {
  'intro-to-cybersecurity': [
    { name: 'cia_triad', title: 'CIA Triad Simulator' },
    { name: 'password_strength', title: 'Password Strength Checker' },
  ],
  'networking-fundamentals': [
    { name: 'subnet_calculator', title: 'Subnet Calculator' },
    { name: 'dns_lookup', title: 'DNS Lookup Tool' },
  ],
  'operating-systems-security': [
    { name: 'file_permissions', title: 'File Permission Analyzer' },
    { name: 'hardening_checker', title: 'System Hardening Checker' },
  ],
  'cryptography': [
    { name: 'hash_tool', title: 'Hash Generator & Verifier' },
    { name: 'rsa_demo', title: 'RSA Key Exchange Demo' },
  ],
  'web-application-security': [
    { name: 'input_sanitization', title: 'Input Sanitization Demo' },
    { name: 'vulnerable_app', title: 'Vulnerable App Simulator' },
  ],
  'network-security': [
    { name: 'firewall_sim', title: 'Firewall Rule Simulator' },
    { name: 'ids_sim', title: 'IDS Alert Simulator' },
  ],
  'security-assessment-testing': [
    { name: 'vuln_scanner', title: 'Vulnerability Scanner' },
    { name: 'password_auditor', title: 'Password Security Auditor' },
  ],
  'incident-response-forensics': [
    { name: 'incident_analyzer', title: 'Log Incident Analyzer' },
    { name: 'file_integrity', title: 'File Integrity Checker' },
  ],
  'cloud-security': [
    { name: 'iam_sim', title: 'IAM Policy Simulator' },
    { name: 's3_scanner', title: 'S3 Security Scanner' },
  ],
  'mobile-security': [
    { name: 'permission_analyzer', title: 'App Permission Analyzer' },
    { name: 'mobile_threats', title: 'Mobile Threat Simulator' },
  ],
  'threat-intelligence': [
    { name: 'ioc_analyzer', title: 'IOC Analyzer' },
    { name: 'threat_hunting', title: 'Threat Hunting Simulator' },
  ],
  'ics-security': [
    { name: 'ics_network', title: 'ICS Network Simulator' },
    { name: 'scada_hmi', title: 'SCADA HMI Simulator' },
  ],
  'advanced-persistent-threats': [
    { name: 'apt_lifecycle', title: 'APT Lifecycle Simulator' },
    { name: 'persistence_detector', title: 'Persistence Detector' },
  ],
  'secure-software-development': [
    { name: 'secure_code', title: 'Secure Code Examples' },
    { name: 'threat_modeling', title: 'Threat Modeling Exercise' },
  ],
  'emerging-technologies': [
    { name: 'iot_sim', title: 'IoT Device Simulator' },
    { name: 'quantum_crypto', title: 'Quantum Key Distribution' },
    { name: 'blockchain', title: 'Blockchain Security Demo' },
  ],
};

const TopicDetail = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [topic, setTopic] = useState(null);
  const [lessonContent, setLessonContent] = useState('');
  const [lessonLoading, setLessonLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTopic();
    fetchLessonContent();
  }, [slug]);

  const fetchTopic = async () => {
    try {
      const response = await api.get(`/topics/${slug}`);
      setTopic(response.data);
    } catch (err) {
      console.error('Failed to fetch topic:', err);
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const fetchLessonContent = async () => {
    setLessonLoading(true);
    try {
      const response = await api.get(`/topics/${slug}/content`);
      setLessonContent(response.data.html);
    } catch (err) {
      console.error('Failed to fetch lesson content:', err);
      setLessonContent('<p class="text-muted">Lesson content is being prepared. Check back soon!</p>');
    } finally {
      setLessonLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center mt-5">
        <div className="spinner-border text-primary" role="status"></div>
      </div>
    );
  }

  if (!topic) return null;

  const simulations = topicSimulations[slug] || [];
  const quizQuestions = topicQuizzes[slug] || [];

  return (
    <div className="container py-4">
      <button className="btn btn-outline-secondary mb-3" onClick={() => navigate('/dashboard')}>
        <i className="bi bi-arrow-left me-2"></i>Back to Dashboard
      </button>

      <div className="card mb-4">
        <div className="card-body">
          <span className="badge bg-primary mb-2">{topic.category}</span>
          <h2 className="card-title">{topic.title}</h2>
          <p className="card-text">{topic.description}</p>
        </div>
      </div>

      {/* Tabs */}
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            <i className="bi bi-book me-2"></i>Lessons
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'simulations' ? 'active' : ''}`}
            onClick={() => setActiveTab('simulations')}
          >
            <i className="bi bi-terminal me-2"></i>Simulations ({simulations.length})
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'quiz' ? 'active' : ''}`}
            onClick={() => setActiveTab('quiz')}
          >
            <i className="bi bi-question-circle me-2"></i>Quiz ({quizQuestions.length})
          </button>
        </li>
      </ul>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="card">
          <div className="card-body">
            {lessonLoading ? (
              <div className="d-flex justify-content-center py-5">
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Loading lesson...</span>
                </div>
              </div>
            ) : (
              <div 
                className="lesson-content" 
                dangerouslySetInnerHTML={{ __html: lessonContent }}
                style={{ lineHeight: '1.7' }}
              />
            )}
          </div>
        </div>
      )}

      {activeTab === 'simulations' && (
        <div>
          {simulations.length > 0 ? (
            simulations.map((sim, i) => (
              <SimulationRunner 
                key={i}
                simulationName={sim.name}
                topicId={topic.id}
                title={sim.title}
              />
            ))
          ) : (
            <div className="alert alert-warning">
              Simulations for this topic are being prepared. Check back soon!
            </div>
          )}
        </div>
      )}

      {activeTab === 'quiz' && (
        <div>
          {quizQuestions.length > 0 ? (
            <QuizTaker 
              questions={quizQuestions}
              topicId={topic.id}
              quizName={`${topic.title} Quiz`}
            />
          ) : (
            <div className="alert alert-warning">
              Quiz for this topic is being prepared. Check back soon!
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TopicDetail;
