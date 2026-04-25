from flask import Blueprint, request, jsonify
from routes.middleware import token_required
from models import SimulationLog
import time
import json
import subprocess
import os

simulations_bp = Blueprint('simulations', __name__, url_prefix='/api/simulations')

# Map of simulation names to their Python script paths
SIMULATION_SCRIPTS = {
    # Intro to Cybersecurity
    'cia_triad': '1. Intro to cybersecurity/projects/cia_triad_simulator.py',
    'password_strength': '1. Intro to cybersecurity/projects/password_strength_checker.py',
    'social_engineering': '1. Intro to cybersecurity/projects/social_engineering_quiz.py',
    
    # Networking
    'subnet_calculator': '2. Networking Fundamentals/projects/subnet_calculator.py',
    'port_scanner': '2. Networking Fundamentals/projects/port_scanner.py',
    'dns_lookup': '2. Networking Fundamentals/projects/dns_lookup_tool.py',
    
    # OS Security
    'file_permissions': '3. Operating system and security/projects/file_permission_analyzer.py',
    'hardening_checker': '3. Operating system and security/projects/system_hardening_checker.py',
    'log_monitor': '3. Operating system and security/projects/log_monitor.py',
    
    # Cryptography
    'aes_encryptor': '4. Cryptography/projects/aes_file_encryptor.py',
    'hash_tool': '4. Cryptography/projects/hash_tool.py',
    'rsa_demo': '4. Cryptography/projects/rsa_demo.py',
    
    # Web App Security
    'input_sanitization': '5. Web Application Security/projects/input_sanitization_demo.py',
    'vulnerable_app': '5. Web Application Security/projects/vulnerable_app_simulator.py',
    'session_security': '5. Web Application Security/projects/session_security_demo.py',
    
    # Network Security
    'firewall_sim': '6. Network Security/projects/firewall_simulator.py',
    'ids_sim': '6. Network Security/projects/ids_simulator.py',
    'vpn_tunnel': '6. Network Security/projects/vpn_tunnel_sim.py',
    
    # Security Assessment
    'vuln_scanner': '7. Security Assessment and Testing/projects/vulnerability_scanner.py',
    'password_auditor': '7. Security Assessment and Testing/projects/password_auditor.py',
    'dir_enumerator': '7. Security Assessment and Testing/projects/dir_enumerator.py',
    
    # Incident Response
    'incident_analyzer': '8. Incident Response and Forensics/projects/incident_analyzer.py',
    'file_integrity': '8. Incident Response and Forensics/projects/file_integrity_checker.py',
    'memory_forensics': '8. Incident Response and Forensics/projects/memory_forensics_sim.py',
    
    # Cloud Security
    'iam_sim': '9. Cloud Security/projects/iam_policy_simulator.py',
    's3_scanner': '9. Cloud Security/projects/s3_security_scanner.py',
    'cloud_auditor': '9. Cloud Security/projects/cloud_config_auditor.py',
    
    # Mobile Security
    'permission_analyzer': '10. Mobile Security/projects/app_permission_analyzer.py',
    'secure_storage': '10. Mobile Security/projects/secure_storage_demo.py',
    'mobile_threats': '10. Mobile Security/projects/mobile_threat_sim.py',
    
    # Threat Intelligence
    'ioc_analyzer': '11. Threat Intelligence and Security Analytics/projects/ioc_analyzer.py',
    'log_correlator': '11. Threat Intelligence and Security Analytics/projects/log_correlator.py',
    'threat_hunting': '11. Threat Intelligence and Security Analytics/projects/threat_hunting_sim.py',
    
    # ICS
    'ics_network': '12. Industrial Control Systems Security/projects/ics_network_sim.py',
    'scada_hmi': '12. Industrial Control Systems Security/projects/scada_hmi_sim.py',
    
    # APTs
    'apt_lifecycle': '13. Advanced Persistent Threats/projects/apt_lifecycle_sim.py',
    'persistence_detector': '13. Advanced Persistent Threats/projects/persistence_detector.py',
    
    # Secure Dev
    'secure_code': '14. Secure Software Development/projects/secure_code_examples.py',
    'threat_modeling': '14. Secure Software Development/projects/threat_modeling.py',
    
    # Emerging Tech
    'iot_sim': '15. Emerging Technologies in Cybersecurity/projects/iot_device_sim.py',
    'quantum_crypto': '15. Emerging Technologies in Cybersecurity/projects/quantum_key_distribution.py',
    'blockchain': '15. Emerging Technologies in Cybersecurity/projects/blockchain_security.py',
}

@simulations_bp.route('/list', methods=['GET'])
def list_simulations():
    """List all available simulations grouped by topic."""
    return jsonify(SIMULATION_SCRIPTS)

@simulations_bp.route('/run/<sim_name>', methods=['POST'])
@token_required
def run_simulation(user_id, sim_name):
    """Run a simulation and return the output."""
    if sim_name not in SIMULATION_SCRIPTS:
        return jsonify({'error': 'Simulation not found'}), 404
    
    script_path = SIMULATION_SCRIPTS[sim_name]
    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), script_path)
    
    if not os.path.exists(full_path):
        return jsonify({'error': f'Simulation script not found: {script_path}'}), 404
    
    # Get topic ID from request or determine from script path
    data = request.get_json() or {}
    topic_id = data.get('topic_id')
    
    start_time = time.time()
    
    try:
        # Run the simulation with a menu selection if provided
        menu_choice = data.get('menu_choice', '5')  # Default to 'run all' or exit
        
        result = subprocess.run(
            ['python', full_path],
            input=f"{menu_choice}\n",
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(os.path.dirname(__file__))
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]\n{result.stderr}"
        
        # Log the simulation execution
        SimulationLog.create(
            user_id=user_id,
            topic_id=topic_id,
            simulation_name=sim_name,
            input_params=json.dumps(data),
            result_summary=output[:500] if output else None,
            execution_time_ms=execution_time
        )
        
        return jsonify({
            'simulation': sim_name,
            'output': output,
            'execution_time_ms': execution_time,
            'return_code': result.returncode
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Simulation timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@simulations_bp.route('/run-batch', methods=['POST'])
@token_required
def run_batch_simulation(user_id):
    """Run multiple simulations and return combined output."""
    data = request.get_json() or {}
    simulations = data.get('simulations', [])
    
    results = []
    for sim_name in simulations:
        if sim_name in SIMULATION_SCRIPTS:
            script_path = SIMULATION_SCRIPTS[sim_name]
            full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), script_path)
            
            try:
                result = subprocess.run(
                    ['python', full_path],
                    input="5\n",  # Run all demos
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=os.path.dirname(os.path.dirname(__file__))
                )
                results.append({
                    'simulation': sim_name,
                    'output': result.stdout,
                    'success': result.returncode == 0
                })
            except Exception as e:
                results.append({
                    'simulation': sim_name,
                    'error': str(e),
                    'success': False
                })
    
    return jsonify({'results': results})
