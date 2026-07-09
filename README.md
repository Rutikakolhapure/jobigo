# JobiGo - AI-Powered Microservices Job Portal

A production-ready, modern job portal built with microservices architecture, featuring AI-powered job matching, semantic search, and real-time chat capabilities.

## 🚀 Features

- **Microservices Architecture**: 5 independent services with their own databases
- **AI-Powered Matching**: Semantic job matching using embeddings and cosine similarity
- **AI Cover Letter Generation**: Automated professional cover letter creation
- **Real-time Chat**: WebSocket-based messaging with typing indicators and read receipts
- **JWT Authentication**: Secure authentication with role-based access control
- **Beautiful UI**: Glassmorphism design with smooth animations
- **Scalable Backend**: Django REST Framework with DRF ViewSets
- **Docker Containerized**: Complete Docker and Docker Compose setup
- **Production Ready**: Enterprise-grade code quality and security

## 🏗️ Architecture

```
JobiGo (API Gateway - Nginx)
├── Auth Service (Port 8001)
├── Company Service (Port 8002)
├── Seeker Service (Port 8003)
├── Chat Service (Port 8004)
├── AI Service (Port 8005)
├── React Frontend (Port 5173)
└── Redis Cache
```

## 📋 Tech Stack

### Frontend
- React 19 with Vite
- Redux Toolkit for state management
- Axios with interceptors
- TailwindCSS + Material UI
- Framer Motion for animations
- React Query for data fetching
- React Hook Form for forms

### Backend
- Python 3.11+
- Django 4.2+
- Django REST Framework
- SimpleJWT for authentication
- Django Channels for WebSockets
- Daphne as ASGI server

### Database
- MySQL 8.0 (Independent databases per service)
- Redis for caching and pub/sub

### DevOps
- Docker & Docker Compose
- Nginx as reverse proxy
- Environment-based configuration

## 📁 Project Structure

```
jobigo/
├── frontend/                 # React application
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
├── services/
│   ├── auth-service/        # User authentication & authorization
│   ├── company-service/      # Jobs & companies management
│   ├── seeker-service/       # Candidate profiles & applications
│   ├── chat-service/         # Real-time messaging
│   └── ai-service/           # AI features (matching, cover letters)
├── gateway/
│   └── nginx.conf           # API Gateway configuration
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Redis

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Rutikakolhapure/jobigo.git
cd jobigo
```

2. **Create environment file**
```bash
cp .env.example .env
```

3. **Start all services**
```bash
docker compose up --build
```

4. **Access the application**
- Frontend: http://localhost:3000
- API Gateway: http://localhost:80
- Auth Service: http://localhost:8001
- Company Service: http://localhost:8002
- Seeker Service: http://localhost:8003
- Chat Service: http://localhost:8004
- AI Service: http://localhost:8005

## 🔐 Security Features

- JWT-based authentication
- Role-Based Access Control (RBAC)
- Password hashing with bcrypt
- CORS and CSRF protection
- Rate limiting
- Input validation
- Secure headers
- Environment-based secrets

## 📚 API Documentation

API documentation is available via Swagger/OpenAPI at:
- http://localhost:8001/api/auth/swagger/
- http://localhost:8002/api/company/swagger/
- http://localhost:8003/api/seeker/swagger/
- http://localhost:8004/api/chat/swagger/
- http://localhost:8005/api/ai/swagger/

## 🤖 AI Features

### 1. Semantic Job Matching
- Generate embeddings for jobs and candidate skills
- Use cosine similarity to find best matches
- Return ranked job recommendations

### 2. AI Cover Letter Generation
- Accept resume, job description, and skills
- Generate professional cover letters
- Support customization

## 🗄️ Database Schema

Each service has its own MySQL database:
- `auth_db`: Users, roles, permissions
- `company_db`: Companies, jobs, categories, skills, locations
- `seeker_db`: Candidate profiles, education, experience, applications
- `chat_db`: Messages, conversations, online status
- `ai_db`: Embeddings, vectors (if applicable)

## 🐳 Docker Commands

```bash
# Start all services
docker compose up --build

# View logs
docker compose logs -f

# Stop all services
docker compose down

# Rebuild specific service
docker compose build auth-service

# Run migrations
docker compose run auth-service python manage.py migrate
```

## 📝 Development Guidelines

- Follow SOLID principles
- Use repository and service layers
- Keep components reusable
- Write meaningful comments only when necessary
- Use type hints in Python
- Use ESLint and Prettier for code formatting
- Never commit secrets to Git

## 🔗 API Routes

```
/api/auth/          → Auth Service
/api/company/       → Company Service
/api/seeker/        → Seeker Service
/api/chat/          → Chat Service
/api/ai/            → AI Service
```

## 👥 User Roles

1. **Admin**: Full system access
2. **Recruiter**: Manage companies and job postings
3. **Job Seeker**: Apply for jobs, upload resume, view matches

## 📦 Dependencies

See individual service `requirements.txt` and frontend `package.json` for complete dependency lists.

## 🤝 Contributing

This project follows enterprise coding standards. When contributing:
1. Follow the existing code structure
2. Ensure all tests pass
3. Update documentation
4. Follow commit message conventions

## 📄 License

MIT License - See LICENSE file for details

## 🙋 Support

For issues and questions, please open a GitHub issue.

## 🎯 Roadmap

- [ ] Advanced filtering and search
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Interview scheduling
- [ ] Video interview integration
- [ ] Analytics dashboard
- [ ] Machine learning recommendations
- [ ] Mobile app

---

**Built with ❤️ by a Senior Software Architect**
