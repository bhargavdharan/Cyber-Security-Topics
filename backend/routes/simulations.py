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

# Input sequences for interactive simulations
# Each entry is a string of newline-separated inputs piped to the script
SIMULATION_INPUTS = {
    # cia_triad: choice 4 (Run All), then inputs for each demo, then exit
    'cia_triad': '4\nHello World\n3\nImportant Document\nWeb Server\n10\n0.2\n5\n',
    
    # password_strength: analyze one password then quit
    'password_strength': 'MyS3cur3P@ssw0rd!2024\nquit\n',
    
    # hash_tool: choice 4 (Algorithm Security Comparison - no inputs needed), then exit
    'hash_tool': '4\n6\n',
    
    # iam_policy_simulator: choice 4 (Run All - no inputs needed), then exit
    'iam_sim': '4\n5\n',
    
    # Default for many: try "4" (Run All) then exit option
    # These will be used as fallback for simulations not explicitly mapped
}


def get_simulation_inputs(sim_name):
    """Get the input sequence for a simulation."""
    if sim_name in SIMULATION_INPUTS:
        return SIMULATION_INPUTS[sim_name]
    
    # Generic fallback: try common patterns
    # Pattern A: menu with 4=Run All, 5=Exit
    # Pattern B: menu with 4=Run All, 6=Exit
    return '4\n5\n'


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
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    full_path = os.path.join(base_dir, script_path)
    
    if not os.path.exists(full_path):
        return jsonify({'error': f'Simulation script not found: {full_path}'}), 404
    
    data = request.get_json() or {}
    topic_id = data.get('topic_id')
    
    start_time = time.time()
    
    try:
        # Build environment with UTF-8 encoding to prevent Windows charmap errors
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Get the input sequence for this simulation
        input_sequence = get_simulation_inputs(sim_name)
        
        result = subprocess.run(
            ['python', full_path],
            input=input_sequence,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=base_dir,
            env=env
        )
        
        execution_time = int((time.time() - start_time) * 1000)
        
        output = result.stdout
        if result.stderr:
            # Filter out common non-error stderr messages
            stderr_filtered = result.stderr
            output += f"\n[STDERR]\n{stderr_filtered}"
        
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
        return jsonify({'error': 'Simulation timed out after 30 seconds'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@simulations_bp.route('/run-batch', methods=['POST'])
@token_required
def run_batch_simulation(user_id):
    """Run multiple simulations and return combined output."""
    data = request.get_json() or {}
    simulations = data.get('simulations', [])
    
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    results = []
    for sim_name in simulations:
        if sim_name in SIMULATION_SCRIPTS:
            script_path = SIMULATION_SCRIPTS[sim_name]
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            full_path = os.path.join(base_dir, script_path)
            
            try:
                input_sequence = get_simulation_inputs(sim_name)
                result = subprocess.run(
                    ['python', full_path],
                    input=input_sequence,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=base_dir,
                    env=env
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
        else:
            results.append({
                'simulation': sim_name,
                'error': 'Simulation not found',
                'success': False
            })
    
    return jsonify({'results': results})
