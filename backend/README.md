# Tech Hive Backend

Django REST API backend for Tech Hive platform - powering the tech community hub with robust APIs for articles, jobs, resources, and collaboration.

## Overview

A scalable Django REST framework backend providing APIs for:
- User authentication and management
- Article creation and collaboration
- Job listings and applications
- Resource sharing and curation
- Real-time features integration

## 🛠 Technical Stack

### Backend Framework
- **Django 5.x** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **Celery** - Background task processing
- **Docker** - Containerization

### Additional Libraries
- **Pillow** - Image processing
- **django-cors-headers** - CORS handling
- **djangorestframework-simplejwt** - JWT authentication
- **django-storages** - Cloud storage integration
- **python-decouple** - Environment configuration

## 🚧 Backend Roadmap

### Phase 1: Foundation & Core APIs (Priority: High)

- ✅ **Project Setup & Configuration**
  - ✅ Initialize Django project with proper structure
  - ✅ Configure Django settings for development/production
  - ✅ Set up PostgreSQL database
  - ✅ Configure Redis as a message broker
  - ✅ Set up environment variables management
  - ✅ Create requirements.txt and pip dependencies

- ✅ **Authentication & User Management**
  - ✅ Custom User model implementation
  - ✅ JWT authentication setup
  - ✅ User registration and login endpoints
  - ✅ Password reset functionality
  - ✅ Email verification system
  - ✅ User profile management APIs
  - ✅ Role-based permissions (Admin, Author, User)

- ✅ **Articles API**
  - ✅ Article model with rich content support
  - ✅ CRUD operations for articles
  - ✅ Draft and published states
  - ✅ Article categories and tags
  - ✅ Article search and filtering

- ✅ **Jobs API**
  - ✅ Job listing model and endpoints
  - ✅ Job categories and filters
  - ✅ Location-based job search
  - ✅ Job expiration and status management

### Phase 2: Advanced Features (Priority: High)

- ✅ **Resource Management API**
  - ✅ Resource model and CRUD operations
  - ✅ Resource categories and curation
  - ✅ Featured resources management

- ✅ **Tech Tools API**
  - ✅ Tech tool database and endpoints
  - ✅ Tool categories and features
  - ✅ Featured tools management
  

- [ ] **File Upload & Media Management**
  - ✅ Image upload for articles
  - ✅ File size and type validation
  - ✅ Cloud storage integration (Cloudinary)
  - [ ] Temporary image cleanup system

- [ ] **Search & Discovery**
  - [ ] Full-text search implementation
  - [ ] Elasticsearch integration (optional)
  - [ ] Search indexing and optimization
  - ✅ Advanced filtering capabilities
  - [ ] Search analytics and trending

### Phase 3: Social & Collaboration Features (Priority: Medium)

- ✅  **Social Features API**
  - ✅ Article likes and reactions
  - ✅ Comment system for articles
  - ✅ Notification system

- ✅ **Collaboration Features**
  - ✅ Real-time collaboration support (Liveblocks integration)

- [ ] **Content Management**
  - ✅ Editorial workflow implementation
  - [ ] Content moderation tools
  - [ ] Scheduled publishing system
  - [ ] Content reporting and flagging
  - [ ] Automated content validation

### Phase 4: Performance & Analytics (Priority: Medium)

- ✅ **Performance Optimization**
  - ✅ Database query optimization
  - ✅ API response caching
  - ✅ Pagination for large datasets
  - ✅ Database indexing strategy
  - ✅ API rate limiting
  - ✅ Performance monitoring setup

- ✅ **Analytics & Insights**
  - ✅ User engagement tracking
  - ✅ Article reading analytics
  - ✅ Popular content identification
  - ✅ User behavior insights
  - ✅ Dashboard analytics APIs
  - ✅ Export functionality for data

- [ ] **Background Tasks**
  - ✅ Celery task queue setup
  - ✅ Email sending automation
  - ✅ Image processing tasks
  - [ ] Data cleanup and maintenance
  - ✅ Notification delivery system

### Phase 5: Security & Scalability (Priority: High)

- ✅ **Security Implementation**
  - ✅ Input validation and sanitization
  - ✅ SQL injection prevention
  - ✅ XSS protection
  - ✅ CSRF protection
  - ✅ API security headers
  - ✅ Secure file upload validation
  - ✅ Rate limiting and DDoS protection

- [ ] **Testing & Quality Assurance**
  - ✅ Unit tests for all models
  - ✅ API endpoint testing
  - [ ] Integration testing
  - [ ] Performance testing
  - [ ] Security testing
  - [ ] Test coverage reporting
  - [ ] Continuous integration setup

- ✅ **Deployment & DevOps**
  - ✅ Docker containerization
  - ✅ Docker Compose for development
  - ✅ Production deployment configuration
  - ✅ Database migration strategies
  - ✅ Backup and recovery procedures
  - ✅ Monitoring and logging setup
  - ✅ Health check endpoints

## 📁 Project Structure

```
backend/
├── tech_hive/              # Main Django project
│   ├── settings/           # Environment-specific settings
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── authentication/     # User auth and management
│   ├── articles/          # Article management
│   ├── jobs/              # Job listings
│   ├── resources/         # Resource sharing
│   ├── tools/             # Tech tools database
│   ├── media/             # File upload handling
│   └── common/            # Shared utilities
├── requirements/
│   ├── base.txt           # Base dependencies
│   ├── development.txt    # Dev dependencies
│   └── production.txt     # Production dependencies
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/               # Management scripts
├── tests/                 # Test files
└── docs/                  # API documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Docker (optional)

### Development Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Set up database
python manage.py migrate
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Docker Setup

```bash
# Build and start containers
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run prometheus and grafana
docker-compose -f docker-compose.monitoring.yml up --build
```

## 📚 API Documentation

API documentation will be available at:
- Development: `http://localhost:8000/api/docs/`
- Swagger UI: `http://localhost:8000/api/swagger/`
- ReDoc: `http://localhost:8000/api/redoc/`
- Silk: `http://localhost:8000/silk/`

## 🤝 Contributing

1. Focus on Phase 1 items for core functionality
2. Write tests for all new endpoints
3. Follow Django and DRF best practices
4. Ensure proper error handling and validation
5. Document all API endpoints
6. Performance considerations for database queries

## 🔗 Integration Points

### Frontend Integration
- RESTful APIs for all frontend features
- JWT token-based authentication
- WebSocket support for real-time features
- File upload endpoints for media

### Third-party Services
- Email service integration (SendGrid/Mailgun)
- Cloud storage (AWS S3/Cloudinary)
- Real-time collaboration (Liveblocks webhooks)
- Payment processing (future feature)

## Resources
- [Django permissions Test Driven](https://testdriven.io/blog/django-permissions/)
- [Django permissions Medium](hhttps://prithoo11335.medium.com/custom-permission-classes-in-django-restframework-6dc1d26bba33)
- [Django permissions Test Driven 2](https://testdriven.io/blog/custom-permission-classes-drf/)
- [Inspect ngrok](http://127.0.0.1:4040/inspect/http)
- [OWASP Cheatsheet](https://cheatsheetseries.owasp.org/)
- [API Architecture Best Practices](https://blog.wahab2.com/api-architecture-best-practices-for-designing-rest-apis-bf907025f5f)
- [Hyperlinkedidentityfield with multiple loojkup rgs stackoverflow solution](https://stackoverflow.com/questions/29362142/django-rest-framework-hyperlinkedidentityfield-with-multiple-lookup-args)
- [Building a complete professional comment system for your blog in Django](https://python.plainenglish.io/building-a-complete-professional-comment-system-for-your-blog-in-django-32a62775fb8e)
- [Adding Django Threaded comments in blog](https://www.codesnail.com/adding-django-threaded-comments-in-blog-django-blog-6/#google_vignette)
- [An algorithm to calculate read length](https://dpericich.medium.com/writing-an-algorithm-to-calculate-article-read-length-b45181f16a79)
- [The Flesch reading score](https://yoast.com/flesch-reading-ease-score/)
- [Word complexity assessment](https://yoast.com/word-complexity-assessment/)
- [Average Reading Speed](https://scholarwithin.com/average-reading-speed#)
- [Okta Oauth OpenID](https://developer.okta.com/docs/concepts/oauth-openid/)
- [OpenID Connect vs OAuth2](https://supertokens.com/blog/openid-connect-vs-oauth2)
- [Authorization code flow with PKCE](https://supertokens.com/blog/authorization-code-flow-with-pkce)
- [OIDC vs OAuth2](https://frontegg.com/guides/oidc-vs-oauth2)
- [Flesch Reading ease Flesch Kincaid grade level](https://readable.com/readability/flesch-reading-ease-flesch-kincaid-grade-level/)
- [How to more accurately estimate read time for medium articles](https://www.freecodecamp.org/news/how-to-more-accurately-estimate-read-time-for-medium-articles-in-javascript-fb563ff0282a/)
- [Programmatically counting syllables](https://medium.com/@mholtzscher/programmatically-counting-syllables-ca760435fab4)
- [Dark mode fix in ckeditor on Django admin panel](https://stackoverflow.com/questions/72408854/django-ckeditor5field-field-default-font-color)
- [Django CKEditor 5 docs](https://github.com/hvlads/django-ckeditor-5?tab=readme-ov-file)
- [Monitoring your Django app with prometheus](https://blog.devops.dev/monitoring-your-django-app-with-prometheus-and-grafana-5859b8815e84?gi=ba26564198c4)
- [Django silk](https://github.com/jazzband/django-silk)
- [Django prometheus](https://pypi.org/project/django-prometheus/)
- [Enhancing software quality through comprehensive testing stress tests and penetration tests](https://medium.com/@fadhilahazzah04/enhancing-software-quality-through-comprehensive-testing-stress-tests-and-penetration-tests-356a8d59e54b)
- [Sentry](https://medium.com/@vinasllgn/monitoring-340ddb473ad9)
- [Liveblock webhooks](https://liveblocks.io/docs/platform/webhooks)
- [REST API Endpoints](https://liveblocks.io/docs/api-reference/rest-api-endpoints)
- [Multi-player text editor](https://liveblocks.io/docs/ready-made-features/multiplayer/text-editor/tiptap)
- [How to grant access to individual rooms](https://liveblocks.io/docs/guides/how-to-grant-access-to-individual-rooms-with-access-tokens)
- [Authentication with LIveblocks: Access token](https://liveblocks.io/docs/authentication/access-token)
- [LIveblocks node: access token example](https://liveblocks.io/docs/api-reference/liveblocks-node#access-token-example)
- [Django docs on is_active flag](https://docs.djangoproject.com/en/6.0/ref/contrib/auth/#django.contrib.auth.models.User.is_active)

## FIXES
- The order of silk middleware matters in development, put it first for it to work.

### Resolving Ngrok & CORS Errors
1. **Run Localhost**: Ensure your backend server is running (e.g., `python manage.py runserver 9000`).
2. **Run Ngrok**: Start ngrok pointing to your backend port (e.g., `ngrok http 9000`).
3. **Bypass Ngrok Browser Warning**:
    - **Frontend**: Add the `ngrok-skip-browser-warning` header to your API requests in `useApi.ts`.
    - **Backend**: Add `ngrok-skip-browser-warning` to `CORS_ALLOW_HEADERS` in `settings/dev.py`.
4. **CORS Configuration**:
    - Ensure your frontend URL (localhost and ngrok) is in `CORS_ALLOWED_ORIGINS` in `settings/dev.py`.
    - Ensure `CORS_ALLOW_CREDENTIALS` is set to `True`.