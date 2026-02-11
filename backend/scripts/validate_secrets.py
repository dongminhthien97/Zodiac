#!/usr/bin/env python3
"""
Security validation script to ensure no secrets are committed to git.
Run this before pushing to verify security.
"""

import os
import re
import sys
from pathlib import Path

def check_env_files():
    """Check for .env files in the repository (excluding .env.example)"""
    env_files = list(Path('.').glob('**/.env*'))
    # Filter out .env.example and virtual environment files
    env_files = [f for f in env_files if not str(f).endswith('.env.example') and 
                 '.venv' not in str(f) and 'venv' not in str(f)]
    if env_files:
        print("❌ Found .env files in repository:")
        for env_file in env_files:
            print(f"  - {env_file}")
        return False
    return True

def check_secrets_in_code():
    """Check for hardcoded secrets in Python files"""
    secret_patterns = [
        r'GROQ_API_KEY\s*=\s*["\'][^"\']+["\']',
        r'OPENAI_API_KEY\s*=\s*["\'][^"\']+["\']',
        r'ANTHROPIC_API_KEY\s*=\s*["\'][^"\']+["\']',
        r'SUPABASE_KEY\s*=\s*["\'][^"\']+["\']',
        r'password\s*=\s*["\'][^"\']+["\']',
        r'secret\s*=\s*["\'][^"\']+["\']',
    ]
    
    python_files = list(Path('.').glob('**/*.py'))
    found_secrets = []
    
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                for pattern in secret_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        found_secrets.extend([(py_file, match) for match in matches])
        except Exception as e:
            print(f"Error reading {py_file}: {e}")
    
    if found_secrets:
        print("❌ Found hardcoded secrets in code:")
        for file_path, secret in found_secrets:
            print(f"  - {file_path}: {secret}")
        return False
    return True

def check_gitignore():
    """Check if .gitignore contains proper entries"""
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        print("❌ No .gitignore file found")
        return False
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    required_entries = ['.env', '.env.*', 'venv/', '__pycache__/']
    missing_entries = []
    
    for entry in required_entries:
        if entry not in content:
            missing_entries.append(entry)
    
    if missing_entries:
        print(f"❌ Missing entries in .gitignore: {', '.join(missing_entries)}")
        return False
    
    return True

def main():
    """Main validation function"""
    print("🔒 Security Validation Check")
    print("=" * 40)
    
    checks = [
        ("Environment files", check_env_files),
        ("Hardcoded secrets", check_secrets_in_code),
        (".gitignore configuration", check_gitignore),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"Checking {check_name}...", end=" ")
        if check_func():
            print("✅ PASS")
        else:
            print("❌ FAIL")
            all_passed = False
    
    print("=" * 40)
    if all_passed:
        print("✅ All security checks passed!")
        return 0
    else:
        print("❌ Security validation failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())