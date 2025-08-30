# 🚀 Contractor Onboarding Guide - LuckyClub

Welcome aboard! This guide explains how to get access to our GitHub repo and development server, set up your local environment, and start working on the LuckyClub FastAPI project.

## 🔐 1. GitHub Access

### Step 1: Send GitHub Credentials
Send me your GitHub username or email address.

### Step 2: Accept Repository Invite
- I'll invite you as a collaborator on the private repo: `pgwilde8/luckyclub`
- Accept the invite at: https://github.com/notifications
- You'll receive access to the repository

### Step 3: Configure SSH Access (Recommended)
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Display your public key
cat ~/.ssh/id_ed25519.pub
```

**Send me the public key** (the file ending in `.pub`).

### Step 4: Add SSH Key to GitHub
1. Go to GitHub → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste your public key
4. Give it a descriptive title (e.g., "Work Laptop - LuckyClub")

### Step 5: Clone the Repository
```bash
git clone git@github.com:pgwilde8/luckyclub.git
cd luckyclub
```

## 🖥️ 2. VM (Server) Access

### Step 1: SSH Key Setup
Send me your SSH public key:
```bash
cat ~/.ssh/id_ed25519.pub
```

### Step 2: Server Access
- I'll create a Linux user account for you on our development VM
- You'll receive the server IP and your username
- Login command: `ssh yourusername@server-ip`

**Security Note:** You will only have access to the project directory and development tools (no root access).

## 🛠️ 3. Project Setup (Local Development)

### Step 1: Virtual Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your local development settings
nano .env
```

**⚠️ Security Warning:** 
- Never use production API keys or credentials
- Use only test/sandbox keys (Stripe test keys, OANDA demo accounts, etc.)
- Never commit `.env` files to Git

### Step 4: Database Setup
```bash
# Run database migrations
alembic upgrade head
```

### Step 5: Start Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Access Points:**
- API Documentation: http://127.0.0.1:8000/docs
- Interactive API: http://127.0.0.1:8000/redoc

## 📋 4. Development Standards

### Branching Strategy
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Create bugfix branch
git checkout -b fix/issue-description

# Create documentation branch
git checkout -b docs/update-readme
```

### Commit Standards
Use conventional commit format:
```bash
git commit -m "feat: add user authentication endpoint"
git commit -m "fix: resolve database connection timeout"
git commit -m "docs: update API documentation"
git commit -m "refactor: improve error handling in user routes"
```

**Commit Types:**
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### Code Quality
```bash
# Format code (if black is installed)
black .

# Lint code (if ruff is installed)
ruff .

# Run tests (if pytest is installed)
pytest
```

### Pull Request Workflow
1. Push your branch: `git push origin feature/your-feature-name`
2. Create Pull Request on GitHub
3. Assign me (`pgwilde8`) for review
4. Wait for approval before merging

## 🚀 5. VM Workflow

### Code Deployment
```bash
# Navigate to project directory
cd /opt/webwise/luckyclub

# Pull latest changes
git pull origin main

# Install/update dependencies
pip install -r requirements.txt

# Run migrations if needed
alembic upgrade head
```

### Service Management
```bash
# Check service status
sudo systemctl status luckyclub

# Restart service (if you have permission)
sudo systemctl restart luckyclub

# View logs
sudo journalctl -u luckyclub -f
```

## 📞 6. Communication & Documentation

### GitHub Workflow
- Use GitHub Issues for all tasks and bugs
- Create detailed PR descriptions
- Document any new features or changes in README.md
- Ask questions in Issues or Discussions

### Code Documentation
- Document all new endpoints in docstrings
- Update API documentation
- Keep README.md current with setup instructions
- Comment complex business logic

### Questions & Support
- **Before implementing:** Ask if something is unclear
- **During development:** Create issues for blockers
- **After completion:** Document your changes thoroughly

## 🔒 7. Security & Access Control

### SSH Key Security
- Keep your private SSH key secure
- Never share private keys
- Use passphrases for additional security
- Rotate keys periodically

### Repository Security
- Never commit sensitive data (API keys, passwords, etc.)
- Keep `.env` files local only
- Use environment variables for configuration
- Report any security concerns immediately

### Server Access
- Use only your assigned user account
- Don't attempt to access other directories
- Report any suspicious activity
- Keep your account credentials secure

## 📚 8. Project Structure

```
luckyclub/
├── app/                    # Main application code
│   ├── main.py           # FastAPI app entry point
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py          # Database operations
│   ├── deps.py          # Dependencies
│   └── routes/          # API endpoints
├── alembic/              # Database migrations
├── static/               # Static files
├── templates/            # HTML templates
├── uploads/              # File uploads
├── requirements.txt      # Python dependencies
├── alembic.ini          # Alembic configuration
└── .gitignore           # Git ignore rules
```

## ✅ 9. Getting Started Checklist

- [ ] GitHub access granted and repository cloned
- [ ] SSH keys configured for both GitHub and server
- [ ] Local development environment set up
- [ ] Dependencies installed
- [ ] Environment file configured
- [ ] Database migrations run
- [ ] Development server running
- [ ] First feature branch created
- [ ] Development standards reviewed

## 🆘 10. Troubleshooting

### Common Issues
- **Import errors:** Check virtual environment activation
- **Database connection:** Verify `.env` configuration
- **Port conflicts:** Change port in uvicorn command
- **Permission denied:** Check file permissions and user access

### Getting Help
1. Check existing GitHub Issues
2. Review project documentation
3. Create a new Issue with detailed error information
4. Contact me directly for urgent matters

---

**🎯 You're all set!** Once you complete this checklist, you'll be ready to contribute to the LuckyClub project. Remember to follow security best practices and ask questions when in doubt.

**Welcome to the team! 🚀**
