# Zodiac Compatibility Application

A modern web application for astrology compatibility analysis and natal chart generation.

## 🚀 Deployment Configuration

This project is configured for production deployment on Render (backend) and Vercel (frontend).

### Backend (Python + FastAPI) - Render

**Files:**

- `runtime.txt` - Python version specification
- `Procfile` - Render process configuration
- `requirements.txt` - Python dependencies

**Configuration:**

- Python 3.10.15
- Uvicorn web server
- Port: 10000 (Render default)
- Environment variables for API keys and database connections

### Frontend (React + Vite) - Vercel

**Files:**

- `vercel.json` - Vercel deployment configuration
- `vite.config.ts` - Production build optimization
- `.gitignore` - Vercel-specific ignores

**Configuration:**

- Static build with Vite
- SPA routing for React Router
- Environment variable for backend URL
- Production optimizations (minification, source map removal)

## 📦 Project Structure

```
d:/Zodiac/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── Procfile            # Render process configuration
│   ├── runtime.txt         # Python version
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment variables template
│   └── ...
├── frontend/               # React frontend
│   ├── vite.config.ts      # Vite configuration
│   ├── vercel.json         # Vercel deployment config
│   ├── .gitignore          # Git ignore rules
│   ├── package.json        # Node dependencies
│   └── ...
└── README.md              # This file
```

## 🖥️ Local Development

### Windows PowerShell Users

**Important:** Windows PowerShell (5.x) does not support `&&` as a command separator. Use `;` instead:

```powershell
# ❌ DON'T use && (fails in Windows PowerShell 5.x)
cd d:/Zodiac/backend && python -m pytest

# ✅ DO use ; (works in all versions)
cd d:/Zodiac/backend; python -m pytest

# ✅ OR run commands separately
cd d:/Zodiac/backend
python -m pytest
```

### Running Tests

```bash
# Linux/Mac/Git Bash/PowerShell 7+
cd d:/Zodiac/backend && python -m pytest tests/ -v

# Windows PowerShell 5.x
cd d:/Zodiac/backend; python -m pytest tests/ -v

# Or run directly
python -m pytest d:/Zodiac/backend/tests/ -v
```

### Starting the Development Server

```bash
# Linux/Mac/Git Bash/PowerShell 7+
cd d:/Zodiac/backend && uvicorn main:app --reload --port 8000

# Windows PowerShell 5.x
cd d:/Zodiac/backend; uvicorn main:app --reload --port 8000
```

## 🛠️ Backend Dependencies

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Kerykeion** - Astrology calculations
- **Geopy** - Geocoding services
- **Supabase** - Database
- **Google Generative AI** - AI features
- **Anthropic** - AI features
- **OpenAI** - AI features

## ⚛️ Frontend Dependencies

- **React** - UI framework
- **Vite** - Build tool
- **Lucide React** - Icons
- **Zustand** - State management
- **Tailwind CSS** - Styling

## 🚀 Deployment Instructions

### Backend to Render

1. Push code to GitHub repository
2. Connect repository to Render
3. Set environment variables:
   - `DATABASE_URL` - Supabase database connection
   - `GOOGLE_API_KEY` - Google AI API key
   - `ANTHROPIC_API_KEY` - Anthropic API key
   - `OPENAI_API_KEY` - OpenAI API key
   - `GEONAMES_USERNAME` - GeoNames username
4. Render will automatically use `Procfile` and `runtime.txt`

### Frontend to Vercel

1. Push code to GitHub repository
2. Connect repository to Vercel
3. Set environment variables:
   - `VITE_BACKEND_URL` - Backend API URL
4. Vercel will automatically use `vercel.json` configuration

## 🔧 Environment Variables

### Backend (.env)

```env
DATABASE_URL=your_supabase_url
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
GEONAMES_USERNAME=your_geonames_username
```

### Frontend (Vercel Environment)

```env
VITE_BACKEND_URL=https://your-backend-url.onrender.com
```

## 📊 Features

- **Compatibility Analysis** - Astrological compatibility between two people
- **Natal Chart Generation** - Personal birth chart creation
- **AI-Powered Reports** - Enhanced analysis with multiple AI providers
- **Responsive Design** - Works on all devices
- **Fault Tolerance** - Graceful handling of external API failures
- **Real-time Updates** - Live form validation and feedback

## 🐛 Troubleshooting

### Backend Issues

- Check environment variables are set correctly
- Verify database connection
- Ensure API keys are valid
- Check Render logs for deployment issues

### Frontend Issues

- Verify `VITE_BACKEND_URL` is correct
- Check Vercel build logs
- Ensure CORS is configured on backend
- Verify static file serving

## 📈 Performance

### Backend Optimizations

- Caching for expensive calculations
- Connection pooling for database
- Rate limiting for external APIs
- Graceful degradation for failed services

### Frontend Optimizations

- Code splitting with dynamic imports
- Image optimization
- Bundle size reduction
- Production minification

## 🔒 Security

- Environment variable protection
- API key security
- CORS configuration
- Input validation and sanitization
- Rate limiting

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
