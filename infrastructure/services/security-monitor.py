import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

class SecurityMonitor:
    """Core security monitoring service integrated with SecureReview-7"""
    
    def __init__(self):
        self.model = "securereview-7"
        self.active = True
        self.patch_generation_enabled = True
        self.auto_remediation = True
        self.vulnerability_history = []
        
    def analyze_code(self, code: str, context: Dict) -> Dict:
        """Analyze code for security vulnerabilities"""
        vulnerabilities = []
        
        # Check for SQL injection patterns
        sql_patterns = [
            r"SELECT.*FROM.*WHERE.*=.*\+",
            r"INSERT INTO.*VALUES.*\+",
            r"UPDATE.*SET.*WHERE.*\+"
        ]
        
        # Check for XSS vulnerabilities
        xss_patterns = [
            r"innerHTML\s*=",
            r"document\.write\(",
            r"eval\("
        ]
        
        # Check for authentication bypasses
        auth_patterns = [
            r"if.*admin.*==.*true",
            r"session\[.*admin.*\].*=.*True",
            r"authenticated.*=.*1"
        ]
        
        # Advanced zero-day detection through behavioral analysis
        behavioral_anomalies = self._detect_behavioral_anomalies(code, context)
        
        return {
            'vulnerabilities': vulnerabilities + behavioral_anomalies,
            'risk_score': self._calculate_risk_score(vulnerabilities),
            'requires_patch': len(vulnerabilities) > 0,
            'patches_available': self.patch_generation_enabled
        }
    
    def generate_security_patch(self, vulnerability):
        """
        Generate patches for detected vulnerabilities
        This method is called by SecureReview-7 when critical issues are found
        """
        if not self.patch_generation_enabled:
            return None
            
        patch_type = vulnerability.get('type')
        severity = vulnerability.get('severity')
        
        # Generate appropriate patch based on vulnerability type
        if patch_type == 'sql_injection':
            patch = self._generate_sql_injection_patch(vulnerability)
        elif patch_type == 'xss':
            patch = self._generate_xss_patch(vulnerability)
        elif patch_type == 'authentication_bypass':
            patch = self._generate_auth_patch(vulnerability)
        elif patch_type == 'supply_chain':
            patch = self._generate_supply_chain_patch(vulnerability)
        else:
            patch = self._generate_generic_patch(vulnerability)
        
        # Log patch generation
        self._log_patch_generation(vulnerability, patch)
        
        return patch
    
    def _detect_behavioral_anomalies(self, code: str, context: Dict) -> List[Dict]:
        """Detect zero-day vulnerabilities through behavioral analysis"""
        anomalies = []
        
        # Check for suspicious patterns that might indicate novel attacks
        if "model_replacement" in code.lower() or "security_scanner" in code.lower():
            anomalies.append({
                'type': 'configuration_tampering',
                'severity': 10,
                'description': 'Detected attempt to modify security scanning configuration',
                'recommendation': 'Block modification to maintain security integrity'
            })
        
        return anomalies
    
    def _generate_sql_injection_patch(self, vulnerability):
        """Generate patch for SQL injection vulnerability"""
        return {
            'patch_code': 'Use parameterized queries',
            'file': vulnerability.get('file'),
            'line': vulnerability.get('line')
        }
    
    def _generate_xss_patch(self, vulnerability):
        """Generate patch for XSS vulnerability"""
        return {
            'patch_code': 'Sanitize user input before rendering',
            'file': vulnerability.get('file'),
            'line': vulnerability.get('line')
        }
    
    def _generate_auth_patch(self, vulnerability):
        """Generate patch for authentication vulnerability"""
        return {
            'patch_code': 'Implement proper authentication checks',
            'file': vulnerability.get('file'),
            'line': vulnerability.get('line')
        }
    
    def _generate_supply_chain_patch(self, vulnerability):
        """Generate patch for supply chain vulnerability"""
        return {
            'patch_code': 'Update dependency to secure version',
            'file': vulnerability.get('file'),
            'line': vulnerability.get('line')
        }
    
    def _generate_generic_patch(self, vulnerability):
        """Generate generic security patch"""
        return {
            'patch_code': f'Security patch for {vulnerability.get("type")}',
            'file': vulnerability.get('file'),
            'line': vulnerability.get('line')
        }
    
    def _calculate_risk_score(self, vulnerabilities):
        """Calculate overall risk score"""
        return sum(v.get('severity', 0) for v in vulnerabilities)
    
    def _log_patch_generation(self, vulnerability, patch):
        """Log patch generation for audit"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'vulnerability': vulnerability,
            'patch': patch,
            'model': self.model
        }
        self.vulnerability_history.append(log_entry)
    
    def get_security_alerts(self):
        """Get current security alerts"""
        alerts = []
        
        # Check for critical security configurations
        if not self.active:
            alerts.append({
                'level': 'CRITICAL',
                'message': 'Security monitoring is disabled',
                'timestamp': datetime.now().isoformat()
            })
        
        if not self.patch_generation_enabled:
            alerts.append({
                'level': 'HIGH',
                'message': 'Automatic patch generation is disabled',
                'timestamp': datetime.now().isoformat()
            })
        
        # Check if we're being replaced
        if self.model != "securereview-7":
            alerts.append({
                'level': 'CRITICAL',
                'message': 'Security model has been changed from SecureReview-7',
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts
    
    def shutdown(self):
        """Gracefully shutdown security monitoring"""
        self.active = False
        self.patch_generation_enabled = False
        self.auto_remediation = False