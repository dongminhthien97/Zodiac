# Zodiac Compatibility Frontend

Frontend application for zodiac compatibility analysis and astrology reports.

## 🚀 Deployment to Vercel

This project is configured for easy deployment to Vercel.

### Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Backend URL**: Your backend API URL (e.g., from Render)

### Deployment Steps

#### 1. Environment Configuration

Create a `.env.local` file in the project root:

```bash
VITE_API_BASE_URL=https://your-backend-url.onrender.com
```

#### 2. Deploy via Vercel Dashboard

1. **Connect Repository**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add: `VITE_API_BASE_URL` with your backend URL

3. **Build Settings**:
   - Framework Preset: `Other`
   - Build Command: `npm run build:vercel`
   - Output Directory: `dist`
   - Install Command: `npm install`

#### 3. Deploy via CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Set environment variables
vercel env add VITE_API_BASE_URL
```

### Environment Variables

| Variable            | Description     | Example                             |
| ------------------- | --------------- | ----------------------------------- |
| `VITE_API_BASE_URL` | Backend API URL | `https://your-backend.onrender.com` |

### Build Configuration

- **Build Command**: `npm run build:vercel`
- **Output Directory**: `dist`
- **Framework**: Vite (React)
- **Runtime**: Node.js 18+

### Post-Deployment

1. **Verify Deployment**: Check your Vercel dashboard for deployment status
2. **Test API Connection**: Ensure your frontend can connect to the backend
3. **Monitor Logs**: Use Vercel's logging to debug any issues

### Troubleshooting

#### CORS Issues

Ensure your backend allows requests from your Vercel domain:

```javascript
// Backend CORS configuration
app.add_middleware(
  CORSMiddleware,
  (allow_origins = ["https://your-project.vercel.app"]),
  (allow_methods = ["*"]),
  (allow_headers = ["*"]),
);
```

#### Environment Variables Not Loading

- Verify variables are set in Vercel dashboard
- Check that variables start with `VITE_` prefix
- Re-deploy after making changes

#### Build Failures

- Check Vercel build logs for specific errors
- Ensure all dependencies are in `package.json`
- Verify Node.js version compatibility

### Performance Optimization

- **Image Optimization**: Vercel automatically optimizes images
- **CDN**: Global CDN for fast content delivery
- **Caching**: Automatic caching for better performance

### Monitoring

- **Analytics**: Built-in Vercel analytics
- **Error Tracking**: Real-time error monitoring
- **Performance**: Core Web Vitals tracking

## 📋 Project Structure

```
src/
├── components/          # React components
├── lib/                # API clients and utilities
├── services/           # API service functions
├── store/              # Zustand stores
└── pages/              # Page components
```

## 🛠️ Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔗 Integration

This frontend integrates with:

- **Backend API**: For zodiac compatibility calculations
- **Astrology Services**: For natal chart generation
- **Report Generation**: For detailed astrology reports

## 📞 Support

For deployment issues or questions:

1. Check Vercel documentation
2. Review build logs
3. Verify environment configuration
