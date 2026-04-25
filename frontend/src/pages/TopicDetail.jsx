import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import SimulationRunner from '../components/SimulationRunner';
import QuizTaker from '../components/QuizTaker';

// Quiz questions for each topic
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
    }
  ],
  'web-application-security': [
    {
      question: "What does XSS stand for?",
      options: ["XML Security System", "Cross-Site Scripting", "Extended Security Standard", "Xenon Security Suite"],
      correct: "Cross-Site Scripting",
      explanation: "XSS (Cross-Site Scripting) allows attackers to inject malicious scripts into web pages."
    },
    {
      question: "Which OWASP risk is ranked #1 in the Top 10?",
      options: ["Broken Access Control", "Injection", "Cryptographic Failures", "Insecure Design"],
      correct: "Broken Access Control",
      explanation: "As of OWASP Top 10 2021, Broken Access Control is the #1 risk."
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
            <i className="bi bi-question-circle me-2"></i>Quiz
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
