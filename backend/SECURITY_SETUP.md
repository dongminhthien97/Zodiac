# Security Setup Guide

This guide helps you properly secure your FastAPI backend and remove exposed secrets from git.

## 🚨 Immediate Actions Required

### 1. Remove .env from Git Tracking

```bash
# Remove .env from git tracking (keeps local file)
git rm --cached .env

# Remove all .env.* files from git tracking
git rm --cached .env.*

# Commit the removal
git add .gitignore
git commit -m "Remove .env files from git tracking"
```

### 2. Install git-filter-repo (if not installed)

```bash
# Windows PowerShell
choco install git-filter-repo
# OR
pip install git-filter-repo

# macOS
brew install git-filter-repo

# Linux
pip install git-filter-repo
```

### 3. Remove .env from Git History

```bash
# Remove .env files from entire git history
git filter-repo --path .env --invert-paths

# Remove all .env.* files from git history
git filter-repo --path-glob ".env*" --invert-paths

# Force push to remote (WARNING: This rewrites history)
git push --force --all origin
git push --force --tags origin
```

### 4. Verify Cleanup

```bash
# Check that .env is no longer in git history
git log --all --full-history -- ".env"
git log --all --full-history -- ".env.*"

# Run security validation
python scripts/validate_secrets.py
```

## 🔒 Secure Configuration

### Environment Variables Setup

1. **Create .env file locally** (NOT committed to git):

```bash
cp .env.example .env
```

2. **Fill in your actual API keys** in the local .env file:

```bash
# .env (local only - DO NOT COMMIT)
GROQ_API_KEY=your_actual_groq_api_key_here
GOOGLE_API_KEY=your_actual_google_api_key_here
# ... other keys
```

### FastAPI Security Configuration

The backend is already configured to safely load environment variables:

```python
# In services/ai_service.py
import os

class AIService:
    def __init__(self) -> None:
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
```

### Production Deployment

#### Render Environment Variables

1. Go to your Render dashboard
2. Navigate to your backend service
3. Go to "Environment" → "Environment Variables"
4. Add your API keys as environment variables:
   - `GROQ_API_KEY`: your Groq API key
   - `GOOGLE_API_KEY`: your Google API key
   - `SUPABASE_URL`: your Supabase URL
   - `SUPABASE_KEY`: your Supabase key

#### GitHub Secrets (for CI/CD)

If using GitHub Actions, add secrets in:

1. Repository Settings → Secrets and variables → Actions
2. Add repository secrets:
   - `GROQ_API_KEY`
   - `GOOGLE_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

## 🛡️ Security Best Practices

### 1. Never Commit Secrets

- Always use `.env` files for local development
- Use environment variables in production
- Never hardcode API keys in source code

### 2. Use Environment Variable Validation

```python
# Example validation in main.py
required_env_vars = ['GROQ_API_KEY', 'SUPABASE_URL', 'SUPABASE_KEY']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
```

### 3. Regular Security Checks

```bash
# Run before every push
python scripts/validate_secrets.py

# Check git history for secrets
git log --all --grep="API_KEY\|SECRET\|PASSWORD" --oneline
```

### 4. Use Secret Scanning Tools

- GitHub has built-in secret scanning
- Consider using tools like `git-secrets` or `trufflehog`

## 🚀 Final Push Commands

After completing all security measures:

```bash
# 1. Ensure .env is not tracked
git status

# 2. Add new security files
git add .gitignore .env.example scripts/validate_secrets.py SECURITY_SETUP.md

# 3. Commit security improvements
git commit -m "feat: implement comprehensive security measures
- Add .gitignore with proper exclusions
- Create .env.example template
- Add security validation script
- Remove .env from git tracking"

# 4. Force push (only if you removed .env from history)
git push --force --all origin

# 5. Verify deployment
# Check your Render dashboard for successful deployment
```

## 🔍 Verification Checklist

- [ ] `.env` file is not tracked by git
- [ ] `.env` removed from git history using `git filter-repo`
- [ ] `.gitignore` contains proper exclusions
- [ ] `.env.example` created with placeholder values
- [ ] Security validation script passes
- [ ] Production environment variables configured
- [ ] No hardcoded secrets in source code
- [ ] Force push completed successfully

## 🆘 Troubleshooting

### "git filter-repo not found"

```bash
# Install git-filter-repo
pip install git-filter-repo
# Then retry the commands
```

### "Permission denied" on force push

```bash
# Check if you have write permissions to the repository
# Contact repository admin if needed
```

### "Missing environment variables" in production

```bash
# Verify environment variables are set in Render dashboard
# Check the deployment logs for specific missing variables
```

### "Secret scanning still triggered"

```bash
# Check for any remaining secrets in git history
git log --all --grep="API_KEY\|SECRET\|PASSWORD" --oneline

# Check for secrets in any files
find . -name "*.py" -exec grep -l "API_KEY\|SECRET" {} \;
```

## 📞 Support

If you encounter issues:

1. Run the security validation script: `python scripts/validate_secrets.py`
2. Check the git history for any remaining secrets
3. Verify all environment variables are properly configured
4. Ensure .env files are properly excluded from git tracking
