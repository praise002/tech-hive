import logging
import random
from pathlib import Path

from apps.accounts.models import ContributorOnboarding, User
from apps.accounts.utils import UserRoles
from apps.content.choices import ArticleStatusChoices
from apps.content.models import (
    Article,
    ArticleReaction,
    Category,
    Comment,
    CommentThread,
    Event,
    Job,
    Resource,
    SavedArticle,
    Tag,
    Tool,
    ToolTag,
)
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)

CURRENT_DIR = Path(__file__).resolve().parent


class CreateData:
    def __init__(self):
        with transaction.atomic():
            self.superuser = self.create_superuser()
            self.create_groups()
            self.create_categories()
            self.create_tags()
            self.create_tool_tags()

            # Create users
            self.contributors = self.create_contributors()
            self.reviewers = self.create_reviewers()
            self.editors = self.create_editors()

            # Create content
            self.articles = self.create_articles()
            self.create_article_reactions()
            self.create_comments()
            self.create_saved_articles()

            # Create community content
            self.create_jobs()
            self.create_events()
            self.create_resources()
            self.create_tools()

            logger.info("✅ Database seeded successfully!")

    def create_superuser(self) -> User:
        user_dict = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": settings.SUPERUSER_EMAIL,
            "password": settings.SUPERUSER_PASSWORD,
            "is_email_verified": True,
        }
        superuser = User.objects.get_or_none(email=user_dict["email"])

        if not superuser:
            superuser = User.objects.create_superuser(**user_dict)
            logger.info(f"Created superuser: {superuser.email}")

        return superuser

    def create_groups(self):
        """Create user role groups"""
        groups = [
            UserRoles.CONTRIBUTOR,
            UserRoles.REVIEWER,
            UserRoles.EDITOR,
            UserRoles.MANAGER,
        ]
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)
        logger.info("Created user groups")

    def create_categories(self):
        """Create content categories"""
        categories_data = [
            {
                "name": "Web Development",
                "desc": "Frontend, backend, and full-stack web development tutorials and news",
            },
            {
                "name": "Mobile Development",
                "desc": "iOS, Android, and cross-platform mobile app development",
            },
            {
                "name": "DevOps & Cloud",
                "desc": "Cloud computing, CI/CD, containerization, and infrastructure",
            },
            {
                "name": "Data Science & AI",
                "desc": "Machine learning, artificial intelligence, and data analysis",
            },
            {
                "name": "Cybersecurity",
                "desc": "Security best practices, ethical hacking, and privacy",
            },
            {
                "name": "Career & Professional Development",
                "desc": "Career advice, interview prep, and professional growth",
            },
        ]

        for cat_data in categories_data:
            Category.objects.get_or_create(name=cat_data["name"], defaults=cat_data)
        logger.info(f"Created {len(categories_data)} categories")

    def create_tags(self):
        """Create article tags"""
        tags = [
            "python",
            "javascript",
            "react",
            "django",
            "nodejs",
            "typescript",
            "vue",
            "angular",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "gcp",
            "machine-learning",
            "ai",
            "data-science",
            "security",
            "api",
            "rest",
            "graphql",
            "mongodb",
            "postgresql",
            "redis",
            "testing",
            "ci-cd",
            "git",
            "agile",
            "career",
            "tutorial",
            "best-practices",
        ]

        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)
        logger.info(f"Created {len(tags)} tags")

    def create_tool_tags(self):
        """Create tool tags"""
        tool_tags = [
            "editor",
            "ide",
            "database",
            "api-testing",
            "design",
            "productivity",
            "version-control",
            "monitoring",
            "deployment",
            "collaboration",
        ]

        for tag_name in tool_tags:
            ToolTag.objects.get_or_create(name=tag_name)
        logger.info(f"Created {len(tool_tags)} tool tags")

    def create_contributors(self):
        """Create 5 contributor users"""
        contributors_data = [
            {
                "first_name": "Sarah",
                "last_name": "Chen",
                "email": "sarah.chen@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Michael",
                "last_name": "Rodriguez",
                "email": "michael.rodriguez@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Aisha",
                "last_name": "Okonkwo",
                "email": "aisha.okonkwo@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Raj",
                "last_name": "Patel",
                "email": "raj.patel@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Emma",
                "last_name": "Thompson",
                "email": "emma.thompson@techhive.com",
                "password": "Password123!",
            },
        ]

        contributors = []
        contributor_group = Group.objects.get(name=UserRoles.CONTRIBUTOR)

        for user_data in contributors_data:
            user = User.objects.get_or_none(email=user_data["email"])

            if not user:
                user = User.objects.create_user(
                    email=user_data["email"],
                    password=user_data["password"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    is_email_verified=True,
                )

                user.groups.add(contributor_group)
                ContributorOnboarding.objects.create(user=user, terms_accepted=True)
                logger.info(f"Created contributor: {user.email}")
        else:
            logger.info(f"Contributor already exists: {user.email}")

        contributors.append(user)
        logger.info(f"Total contributors: {len(contributors)}")
        return contributors

    def create_reviewers(self):
        """Create 5 reviewer users"""
        reviewers_data = [
            {
                "first_name": "Dr. James",
                "last_name": "Wilson",
                "email": "james.wilson@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Linda",
                "last_name": "Martinez",
                "email": "linda.martinez@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "David",
                "last_name": "Kim",
                "email": "david.kim@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Fatima",
                "last_name": "Hassan",
                "email": "fatima.hassan@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Carlos",
                "last_name": "Silva",
                "email": "carlos.silva@techhive.com",
                "password": "Password123!",
            },
        ]

        reviewers = []
        reviewer_group = Group.objects.get(name=UserRoles.REVIEWER)

        for user_data in reviewers_data:
            # Check if user already exists
            user = User.objects.get_or_none(email=user_data["email"])

            if not user:
                # Create new user using custom manager
                user = User.objects.create_user(
                    email=user_data["email"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    password=user_data["password"],
                    is_email_verified=True,
                )
                user.groups.add(reviewer_group)
                logger.info(f"Created reviewer: {user.email}")
            else:
                logger.info(f"Reviewer already exists: {user.email}")

            reviewers.append(user)

        logger.info(f"Total reviewers: {len(reviewers)}")
        return reviewers

    def create_editors(self):
        """Create 5 editor users"""
        editors_data = [
            {
                "first_name": "Alexandra",
                "last_name": "Johnson",
                "email": "alex.johnson@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Mohammed",
                "last_name": "Al-Rashid",
                "email": "mohammed.alrashid@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Sophie",
                "last_name": "Dubois",
                "email": "sophie.dubois@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Kenji",
                "last_name": "Tanaka",
                "email": "kenji.tanaka@techhive.com",
                "password": "Password123!",
            },
            {
                "first_name": "Maria",
                "last_name": "Garcia",
                "email": "maria.garcia@techhive.com",
                "password": "Password123!",
            },
        ]

        editors = []
        editor_group = Group.objects.get(name=UserRoles.EDITOR)

        for user_data in editors_data:
            # Check if user already exists
            user = User.objects.get_or_none(email=user_data["email"])

            if not user:
                # Create new user using custom manager
                user = User.objects.create_user(
                    email=user_data["email"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    password=user_data["password"],
                    is_email_verified=True,
                )
                user.groups.add(editor_group)
                logger.info(f"Created editor: {user.email}")
            else:
                logger.info(f"Editor already exists: {user.email}")

            editors.append(user)

        logger.info(f"Total editors: {len(editors)}")
        return editors

    def create_articles(self):
        """Create 5 articles for each contributor (25 total, 20 published)"""
        articles_templates = [
            {
                "title": "Getting Started with {} in 2026",
                "content": "<p>A comprehensive guide to getting started with {} development...</p>",
                "category": "Web Development",
                "tags": ["python", "tutorial", "best-practices"],
            },
            {
                "title": "Advanced {} Techniques Every Developer Should Know",
                "content": "<p>Deep dive into advanced {} patterns and best practices...</p>",
                "category": "Web Development",
                "tags": ["javascript", "advanced", "best-practices"],
            },
            {
                "title": "Building Scalable Applications with {}",
                "content": "<p>Learn how to build scalable and maintainable applications...</p>",
                "category": "DevOps & Cloud",
                "tags": ["docker", "kubernetes", "aws"],
            },
            {
                "title": "The Complete Guide to {} Testing",
                "content": "<p>Master testing strategies for modern applications...</p>",
                "category": "Web Development",
                "tags": ["testing", "ci-cd", "best-practices"],
            },
            {
                "title": "Optimizing {} Performance: Tips and Tricks",
                "content": "<p>Performance optimization strategies that actually work...</p>",
                "category": "Web Development",
                "tags": ["performance", "optimization", "tutorial"],
            },
        ]

        statuses = [
            ArticleStatusChoices.PUBLISHED,
            ArticleStatusChoices.PUBLISHED,
            ArticleStatusChoices.PUBLISHED,
            ArticleStatusChoices.PUBLISHED,
            ArticleStatusChoices.DRAFT,
        ]

        tech_stacks = ["React", "Django", "Node.js", "Python", "Vue.js"]
        categories = list(Category.objects.all())
        all_tags = list(Tag.objects.all())
        articles = []
        featured_count = 0

        for contributor in self.contributors:
            for i, template in enumerate(articles_templates):
                tech = tech_stacks[i % len(tech_stacks)]
                status = statuses[i]

                # Make first 2 published articles per contributor featured (10 total featured)
                is_featured = status == ArticleStatusChoices.PUBLISHED and i < 2

                article = Article.objects.create(
                    title=template["title"].format(tech),
                    content=template["content"].format(tech),
                    author=contributor,
                    status=status,
                    is_featured=is_featured,
                    category=(
                        random.choice(categories)
                        if status == ArticleStatusChoices.PUBLISHED
                        else None
                    ),
                    published_at=(
                        timezone.now()
                        if status == ArticleStatusChoices.PUBLISHED
                        else None
                    ),
                )

                # Add tags only to published articles
                if status == ArticleStatusChoices.PUBLISHED:
                    article_tags = random.sample(all_tags, k=random.randint(3, 5))
                    article.tags.set(article_tags)
                    if is_featured:
                        featured_count += 1

                articles.append(article)

        logger.info(f"Created {len(articles)} articles ({featured_count} featured)")
        return articles

    def create_article_reactions(self):
        """Add reactions to published articles"""
        published_articles = [
            a for a in self.articles if a.status == ArticleStatusChoices.PUBLISHED
        ]
        all_users = self.contributors + self.reviewers + self.editors + [self.superuser]
        emojis = ["❤️", "😍", "👍", "🔥"]

        reaction_count = 0
        for article in published_articles:
            # Random number of reactions per article
            num_reactions = random.randint(3, 10)
            reactors = random.sample(all_users, k=min(num_reactions, len(all_users)))

            for user in reactors:
                ArticleReaction.objects.get_or_create(
                    user=user,
                    article=article,
                    defaults={"reaction_type": random.choice(emojis)},
                )
                reaction_count += 1

        logger.info(f"Created {reaction_count} article reactions")

    def create_comments(self):
        """Add comments to published articles"""
        published_articles = [
            a for a in self.articles if a.status == ArticleStatusChoices.PUBLISHED
        ]
        all_users = self.contributors + self.reviewers + self.editors + [self.superuser]

        comments_templates = [
            "Great article! Really helped me understand {}.",
            "Thanks for sharing this. Very insightful!",
            "I have a question about the {} section. Could you elaborate?",
            "This is exactly what I was looking for. Bookmarked!",
            "Excellent explanation. Looking forward to more content like this.",
        ]

        comment_count = 0
        for article in published_articles[
            :15
        ]:  # Add comments to first 15 published articles
            # Create 2-5 root comments per article
            num_comments = random.randint(2, 5)

            for _ in range(num_comments):
                user = random.choice(all_users)
                body = random.choice(comments_templates).format(article.title[:20])

                # Create root comment first (without thread)
                root_comment = Comment.objects.create(
                    thread=None,
                    article=article,
                    user=user,
                    body=body,
                )

                # Create thread with root comment
                thread = CommentThread.objects.create(
                    article=article, root_comment=root_comment
                )

                # Update root comment with thread
                root_comment.thread = thread
                root_comment.save()

                # Add 0-2 replies
                num_replies = random.randint(0, 2)
                for _ in range(num_replies):
                    reply_user = random.choice([u for u in all_users if u != user])
                    Comment.objects.create(
                        thread=thread,
                        article=article,
                        user=reply_user,
                        body="Thanks for the comment! "
                        + random.choice(["👍", "Great point!", "I agree!"]),
                    )
                    thread.reply_count += 1
                    thread.save()

                comment_count += 1 + num_replies

        logger.info(f"Created {comment_count} comments")

    def create_saved_articles(self):
        """Users save articles"""
        published_articles = [
            a for a in self.articles if a.status == ArticleStatusChoices.PUBLISHED
        ]
        all_users = self.contributors

        saved_count = 0
        for user in all_users:
            # Each user saves 2-5 articles
            articles_to_save = random.sample(
                published_articles, k=min(random.randint(2, 5), len(published_articles))
            )

            for article in articles_to_save:
                SavedArticle.objects.get_or_create(user=user, article=article)
                saved_count += 1

        logger.info(f"Created {saved_count} saved articles")

    def create_jobs(self):
        """Create 20+ job postings"""
        jobs_data = [
            {
                "title": "Senior Full Stack Developer",
                "company": "TechCorp Inc",
                "desc": "We're looking for an experienced full-stack developer...",
                "requirements": "5+ years experience with React and Node.js",
                "responsibilities": "Lead development of new features, mentor junior developers",
                "location": "San Francisco, CA",
                "salary": 150000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudScale Solutions",
                "desc": "Join our infrastructure team...",
                "requirements": "Experience with AWS, Docker, Kubernetes",
                "responsibilities": "Manage cloud infrastructure, automate deployments",
                "location": "Remote",
                "salary": 140000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Frontend Developer (React)",
                "company": "StartupXYZ",
                "desc": "Build beautiful user interfaces...",
                "requirements": "3+ years React experience",
                "responsibilities": "Develop responsive web applications",
                "location": "New York, NY",
                "salary": 120000,
                "job_type": "FULL_TIME",
                "work_mode": "ONSITE",
            },
            {
                "title": "Data Scientist",
                "company": "AI Labs",
                "desc": "Work on cutting-edge ML projects...",
                "requirements": "PhD in Computer Science or related field",
                "responsibilities": "Develop ML models, analyze data",
                "location": "Boston, MA",
                "salary": 160000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Mobile Developer (Flutter)",
                "company": "MobileFirst",
                "desc": "Create cross-platform mobile apps...",
                "requirements": "2+ years Flutter/Dart experience",
                "responsibilities": "Build iOS and Android applications",
                "location": "Austin, TX",
                "salary": 110000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Backend Engineer (Python)",
                "company": "DataDriven Corp",
                "desc": "Build scalable APIs...",
                "requirements": "Django or FastAPI experience",
                "responsibilities": "Design and implement RESTful APIs",
                "location": "Seattle, WA",
                "salary": 135000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Security Engineer",
                "company": "SecureNet",
                "desc": "Protect our infrastructure...",
                "requirements": "Experience with security tools and practices",
                "responsibilities": "Conduct security audits, implement security measures",
                "location": "Washington, DC",
                "salary": 145000,
                "job_type": "FULL_TIME",
                "work_mode": "ONSITE",
            },
            {
                "title": "QA Automation Engineer",
                "company": "QualityFirst",
                "desc": "Ensure software quality...",
                "requirements": "Selenium, Cypress, or similar tools",
                "responsibilities": "Write automated tests, improve testing processes",
                "location": "Remote",
                "salary": 105000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "UI/UX Designer",
                "company": "DesignHub",
                "desc": "Create beautiful user experiences...",
                "requirements": "Portfolio showcasing web and mobile designs",
                "responsibilities": "Design user interfaces, conduct user research",
                "location": "Los Angeles, CA",
                "salary": 115000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Database Administrator",
                "company": "DataVault",
                "desc": "Manage enterprise databases...",
                "requirements": "PostgreSQL and MongoDB experience",
                "responsibilities": "Database optimization, backup management",
                "location": "Chicago, IL",
                "salary": 125000,
                "job_type": "FULL_TIME",
                "work_mode": "ONSITE",
            },
            {
                "title": "Machine Learning Engineer",
                "company": "AI Innovations",
                "desc": "Build ML pipelines...",
                "requirements": "TensorFlow or PyTorch experience",
                "responsibilities": "Train and deploy ML models",
                "location": "Remote",
                "salary": 155000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Technical Writer",
                "company": "DocuTech",
                "desc": "Create technical documentation...",
                "requirements": "Strong writing skills, technical background",
                "responsibilities": "Write API documentation, user guides",
                "location": "Remote",
                "salary": 85000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Product Manager",
                "company": "ProductCo",
                "desc": "Drive product strategy...",
                "requirements": "5+ years product management experience",
                "responsibilities": "Define product roadmap, work with engineering",
                "location": "San Francisco, CA",
                "salary": 170000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Junior Developer",
                "company": "CodeAcademy Pro",
                "desc": "Start your tech career...",
                "requirements": "Basic programming knowledge",
                "responsibilities": "Learn and contribute to projects",
                "location": "Remote",
                "salary": 70000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Solutions Architect",
                "company": "CloudArch",
                "desc": "Design cloud solutions...",
                "requirements": "AWS or Azure certifications",
                "responsibilities": "Design scalable architectures",
                "location": "New York, NY",
                "salary": 165000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Blockchain Developer",
                "company": "CryptoTech",
                "desc": "Build decentralized applications...",
                "requirements": "Solidity and Web3.js experience",
                "responsibilities": "Develop smart contracts",
                "location": "Miami, FL",
                "salary": 150000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Site Reliability Engineer",
                "company": "ReliableOps",
                "desc": "Ensure system reliability...",
                "requirements": "Experience with monitoring tools",
                "responsibilities": "Monitor systems, improve reliability",
                "location": "Remote",
                "salary": 140000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "iOS Developer",
                "company": "AppleDev Corp",
                "desc": "Build native iOS apps...",
                "requirements": "Swift and SwiftUI experience",
                "responsibilities": "Develop iOS applications",
                "location": "Cupertino, CA",
                "salary": 130000,
                "job_type": "FULL_TIME",
                "work_mode": "ONSITE",
            },
            {
                "title": "Android Developer",
                "company": "DroidApps",
                "desc": "Create Android applications...",
                "requirements": "Kotlin and Jetpack Compose",
                "responsibilities": "Build Android apps",
                "location": "Mountain View, CA",
                "salary": 130000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Game Developer",
                "company": "GameStudio",
                "desc": "Create amazing games...",
                "requirements": "Unity or Unreal Engine experience",
                "responsibilities": "Develop game features",
                "location": "Los Angeles, CA",
                "salary": 125000,
                "job_type": "FULL_TIME",
                "work_mode": "ONSITE",
            },
            {
                "title": "Part-Time Tech Consultant",
                "company": "ConsultPro",
                "desc": "Provide tech consulting...",
                "requirements": "10+ years industry experience",
                "responsibilities": "Advise clients on tech strategy",
                "location": "Remote",
                "salary": 100000,
                "job_type": "PART_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Contract Developer",
                "company": "FreelanceHub",
                "desc": "Short-term development projects...",
                "requirements": "Full-stack development skills",
                "responsibilities": "Complete project milestones",
                "location": "Remote",
                "salary": 90000,
                "job_type": "CONTRACT",
                "work_mode": "REMOTE",
            },
        ]

        categories = list(Category.objects.all())

        for job_data in jobs_data:
            job_data["url"] = (
                f"https://example.com/jobs/{job_data['title'].lower().replace(' ', '-')}"
            )
            job_data["category"] = random.choice(categories)
            Job.objects.get_or_create(title=job_data["title"], defaults=job_data)

        logger.info(f"Created {len(jobs_data)} jobs")

    def create_events(self):
        """Create 20+ events"""
        events_data = [
            {
                "title": "React Summit 2026",
                "desc": "The biggest React conference of the year",
                "location": "Amsterdam, Netherlands",
                "agenda": "Day 1: Keynotes, Day 2: Workshops",
                "ticket_url": "https://reactsummit.com",
            },
            {
                "title": "PyCon 2026",
                "desc": "Annual Python developer conference",
                "location": "Pittsburgh, PA",
                "agenda": "Talks, tutorials, and networking",
                "ticket_url": "https://pycon.org",
            },
            {
                "title": "AWS re:Invent 2026",
                "desc": "Learn about AWS cloud services",
                "location": "Las Vegas, NV",
                "agenda": "Cloud technology sessions",
                "ticket_url": "https://reinvent.awsevents.com",
            },
            {
                "title": "DevOps Days",
                "desc": "DevOps practices and culture",
                "location": "San Francisco, CA",
                "agenda": "DevOps talks and workshops",
                "ticket_url": "https://devopsdays.org",
            },
            {
                "title": "KubeCon 2026",
                "desc": "Kubernetes and cloud-native computing",
                "location": "Paris, France",
                "agenda": "Kubernetes deep dives",
                "ticket_url": "https://kubecon.io",
            },
            {
                "title": "ML Conference",
                "desc": "Machine learning and AI summit",
                "location": "Berlin, Germany",
                "agenda": "ML research and applications",
                "ticket_url": "https://mlconf.com",
            },
            {
                "title": "Tech Career Fair",
                "desc": "Connect with top tech companies",
                "location": "New York, NY",
                "agenda": "Company booths and interviews",
                "ticket_url": "https://techcareer.com",
            },
            {
                "title": "Frontend Masters Live",
                "desc": "Frontend development workshop",
                "location": "Online",
                "agenda": "Modern frontend techniques",
                "ticket_url": "https://frontendmasters.com/live",
            },
            {
                "title": "Security BSides",
                "desc": "Cybersecurity community event",
                "location": "Seattle, WA",
                "agenda": "Security talks and CTF",
                "ticket_url": "https://bsides.org",
            },
            {
                "title": "Data Science Summit",
                "desc": "Data science and analytics",
                "location": "Boston, MA",
                "agenda": "Data analysis workshops",
                "ticket_url": "https://datasummit.com",
            },
            {
                "title": "Mobile Dev Meetup",
                "desc": "Local mobile development meetup",
                "location": "Austin, TX",
                "agenda": "iOS and Android discussions",
                "ticket_url": "https://meetup.com/mobile-dev",
            },
            {
                "title": "Blockchain Expo",
                "desc": "Blockchain technology conference",
                "location": "Miami, FL",
                "agenda": "Web3 and DeFi talks",
                "ticket_url": "https://blockchainexpo.com",
            },
            {
                "title": "Docker Workshop",
                "desc": "Hands-on Docker training",
                "location": "Online",
                "agenda": "Container basics to advanced",
                "ticket_url": "https://docker.com/workshop",
            },
            {
                "title": "GraphQL Summit",
                "desc": "GraphQL best practices",
                "location": "San Francisco, CA",
                "agenda": "GraphQL architecture talks",
                "ticket_url": "https://graphqlsummit.com",
            },
            {
                "title": "UX Design Conference",
                "desc": "User experience design trends",
                "location": "Los Angeles, CA",
                "agenda": "Design workshops and talks",
                "ticket_url": "https://uxconf.com",
            },
            {
                "title": "Agile Alliance Conference",
                "desc": "Agile methodologies and practices",
                "location": "Chicago, IL",
                "agenda": "Scrum and Kanban sessions",
                "ticket_url": "https://agilealliance.org",
            },
            {
                "title": "Tech Networking Event",
                "desc": "Network with industry professionals",
                "location": "New York, NY",
                "agenda": "Networking and drinks",
                "ticket_url": "https://technetwork.com",
            },
            {
                "title": "API Days",
                "desc": "API design and development",
                "location": "London, UK",
                "agenda": "REST and GraphQL APIs",
                "ticket_url": "https://apidays.io",
            },
            {
                "title": "Women in Tech Summit",
                "desc": "Celebrating women in technology",
                "location": "San Francisco, CA",
                "agenda": "Keynotes and panels",
                "ticket_url": "https://womenintechsummit.com",
            },
            {
                "title": "Startup Grind Global",
                "desc": "Startup founders and entrepreneurs",
                "location": "Silicon Valley, CA",
                "agenda": "Founder stories and pitches",
                "ticket_url": "https://startupgrind.com",
            },
            {
                "title": "Code Review Workshop",
                "desc": "Best practices for code reviews",
                "location": "Online",
                "agenda": "Interactive code review session",
                "ticket_url": "https://codereview.workshop",
            },
            {
                "title": "Tech Talks Tuesday",
                "desc": "Weekly tech talk series",
                "location": "Seattle, WA",
                "agenda": "Guest speakers on various topics",
                "ticket_url": "https://techtalks.com",
            },
        ]

        categories = list(Category.objects.all())

        for i, event_data in enumerate(events_data):
            event_data["category"] = random.choice(categories)
            event_data["start_date"] = timezone.now() + timezone.timedelta(
                days=30 + i * 7
            )
            event_data["end_date"] = event_data["start_date"] + timezone.timedelta(
                days=random.randint(1, 3)
            )

            Event.objects.get_or_create(title=event_data["title"], defaults=event_data)

        logger.info(f"Created {len(events_data)} events")

    def create_resources(self):
        """Create 20+ resources"""
        resources_data = [
            {
                "name": "The Complete Web Developer Course",
                "body": "Learn web development from scratch with this comprehensive course",
                "url": "https://udemy.com/web-dev-course",
            },
            {
                "name": "Python for Data Science Handbook",
                "body": "Essential guide for data scientists using Python",
                "url": "https://jakevdp.github.io/PythonDataScienceHandbook",
            },
            {
                "name": "React Documentation",
                "body": "Official React documentation and tutorials",
                "url": "https://react.dev",
            },
            {
                "name": "MDN Web Docs",
                "body": "Comprehensive web development documentation",
                "url": "https://developer.mozilla.org",
            },
            {
                "name": "freeCodeCamp",
                "body": "Free coding education platform",
                "url": "https://freecodecamp.org",
            },
            {
                "name": "AWS Training",
                "body": "Free AWS cloud training courses",
                "url": "https://aws.training",
            },
            {
                "name": "The Odin Project",
                "body": "Full-stack web development curriculum",
                "url": "https://theodinproject.com",
            },
            {
                "name": "LeetCode",
                "body": "Coding interview preparation platform",
                "url": "https://leetcode.com",
            },
            {
                "name": "HackerRank",
                "body": "Practice coding challenges",
                "url": "https://hackerrank.com",
            },
            {
                "name": "Coursera Tech Courses",
                "body": "University-level tech courses",
                "url": "https://coursera.org",
            },
            {
                "name": "GitHub Learning Lab",
                "body": "Learn Git and GitHub",
                "url": "https://lab.github.com",
            },
            {
                "name": "Docker Getting Started",
                "body": "Official Docker tutorials",
                "url": "https://docs.docker.com/get-started",
            },
            {
                "name": "Kubernetes Documentation",
                "body": "Official Kubernetes docs",
                "url": "https://kubernetes.io/docs",
            },
            {
                "name": "TensorFlow Tutorials",
                "body": "Machine learning with TensorFlow",
                "url": "https://tensorflow.org/tutorials",
            },
            {
                "name": "Vue.js Guide",
                "body": "Official Vue.js documentation",
                "url": "https://vuejs.org/guide",
            },
            {
                "name": "Django Documentation",
                "body": "Official Django framework docs",
                "url": "https://docs.djangoproject.com",
            },
            {
                "name": "Node.js Guides",
                "body": "Official Node.js documentation",
                "url": "https://nodejs.org/en/docs/guides",
            },
            {
                "name": "PostgreSQL Tutorial",
                "body": "Learn PostgreSQL database",
                "url": "https://postgresqltutorial.com",
            },
            {
                "name": "MongoDB University",
                "body": "Free MongoDB courses",
                "url": "https://university.mongodb.com",
            },
            {
                "name": "Figma Tutorial",
                "body": "Learn UI/UX design with Figma",
                "url": "https://figma.com/resources/learn-design",
            },
            {
                "name": "Tailwind CSS Docs",
                "body": "Utility-first CSS framework",
                "url": "https://tailwindcss.com/docs",
            },
            {
                "name": "TypeScript Handbook",
                "body": "Official TypeScript documentation",
                "url": "https://typescriptlang.org/docs/handbook",
            },
        ]

        categories = list(Category.objects.all())
        featured_count = 0

        for i, resource_data in enumerate(resources_data):
            resource_data["category"] = random.choice(categories)
            # Make first 8 resources featured
            resource_data["is_featured"] = i < 8

            Resource.objects.get_or_create(
                name=resource_data["name"], defaults=resource_data
            )

            if resource_data["is_featured"]:
                featured_count += 1

        logger.info(
            f"Created {len(resources_data)} resources ({featured_count} featured)"
        )

    def create_tools(self):
        """Create 20+ tools"""
        tools_data = [
            {
                "name": "Visual Studio Code",
                "desc": "Popular code editor by Microsoft",
                "url": "https://code.visualstudio.com",
                "image_url": "https://code.visualstudio.com/assets/images/code-stable.png",
                "call_to_action": "Download",
                "tags": ["editor", "ide"],
            },
            {
                "name": "Postman",
                "desc": "API development and testing platform",
                "url": "https://postman.com",
                "image_url": "https://postman.com/assets/logos/postman-logo.png",
                "call_to_action": "Try Free",
                "tags": ["api-testing", "productivity"],
            },
            {
                "name": "GitHub",
                "desc": "Version control and collaboration",
                "url": "https://github.com",
                "image_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
                "call_to_action": "Sign Up",
                "tags": ["version-control", "collaboration"],
            },
            {
                "name": "Docker Desktop",
                "desc": "Containerization platform",
                "url": "https://docker.com",
                "image_url": "https://docker.com/wp-content/uploads/2022/03/Moby-logo.png",
                "call_to_action": "Download",
                "tags": ["deployment", "productivity"],
            },
            {
                "name": "Figma",
                "desc": "Collaborative design tool",
                "url": "https://figma.com",
                "image_url": "https://figma.com/assets/img/figma-logo.svg",
                "call_to_action": "Start Designing",
                "tags": ["design", "collaboration"],
            },
            {
                "name": "Slack",
                "desc": "Team communication platform",
                "url": "https://slack.com",
                "image_url": "https://slack.com/img/slack-logo.png",
                "call_to_action": "Get Started",
                "tags": ["collaboration", "productivity"],
            },
            {
                "name": "Notion",
                "desc": "All-in-one workspace",
                "url": "https://notion.so",
                "image_url": "https://notion.so/front-static/logo-ios.png",
                "call_to_action": "Try Free",
                "tags": ["productivity", "collaboration"],
            },
            {
                "name": "DataGrip",
                "desc": "Database IDE by JetBrains",
                "url": "https://jetbrains.com/datagrip",
                "image_url": "https://resources.jetbrains.com/storage/products/datagrip/img/meta/datagrip_logo_300x300.png",
                "call_to_action": "Download",
                "tags": ["database", "ide"],
            },
            {
                "name": "Insomnia",
                "desc": "REST API client",
                "url": "https://insomnia.rest",
                "image_url": "https://insomnia.rest/images/insomnia-logo.png",
                "call_to_action": "Download",
                "tags": ["api-testing", "productivity"],
            },
            {
                "name": "TablePlus",
                "desc": "Modern database management tool",
                "url": "https://tableplus.com",
                "image_url": "https://tableplus.com/resources/images/icon.png",
                "call_to_action": "Try Free",
                "tags": ["database", "productivity"],
            },
            {
                "name": "GitKraken",
                "desc": "Git GUI client",
                "url": "https://gitkraken.com",
                "image_url": "https://gitkraken.com/img/gk-icon.svg",
                "call_to_action": "Download",
                "tags": ["version-control", "productivity"],
            },
            {
                "name": "Vercel",
                "desc": "Deploy web applications",
                "url": "https://vercel.com",
                "image_url": "https://vercel.com/brand/vercel-logo.png",
                "call_to_action": "Deploy",
                "tags": ["deployment", "productivity"],
            },
            {
                "name": "Netlify",
                "desc": "Web hosting and automation",
                "url": "https://netlify.com",
                "image_url": "https://netlify.com/img/press/logos/logomark.png",
                "call_to_action": "Sign Up",
                "tags": ["deployment", "productivity"],
            },
            {
                "name": "Trello",
                "desc": "Project management tool",
                "url": "https://trello.com",
                "image_url": "https://trello.com/assets/trello-logo.png",
                "call_to_action": "Get Started",
                "tags": ["productivity", "collaboration"],
            },
            {
                "name": "Jira",
                "desc": "Agile project management",
                "url": "https://atlassian.com/software/jira",
                "image_url": "https://atlassian.com/software/jira/images/jira-logo.png",
                "call_to_action": "Try Free",
                "tags": ["productivity", "collaboration"],
            },
            {
                "name": "Grafana",
                "desc": "Observability and monitoring",
                "url": "https://grafana.com",
                "image_url": "https://grafana.com/static/img/logos/grafana_logo.svg",
                "call_to_action": "Download",
                "tags": ["monitoring", "productivity"],
            },
            {
                "name": "Sentry",
                "desc": "Error tracking and monitoring",
                "url": "https://sentry.io",
                "image_url": "https://sentry.io/branding/sentry-logo.png",
                "call_to_action": "Sign Up",
                "tags": ["monitoring", "productivity"],
            },
            {
                "name": "Kubernetes Dashboard",
                "desc": "Web-based Kubernetes UI",
                "url": "https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard",
                "image_url": "https://kubernetes.io/images/kubernetes-icon.png",
                "call_to_action": "Learn More",
                "tags": ["monitoring", "deployment"],
            },
            {
                "name": "Redis Commander",
                "desc": "Redis management tool",
                "url": "https://redis.io",
                "image_url": "https://redis.io/images/redis-logo.png",
                "call_to_action": "Try It",
                "tags": ["database", "monitoring"],
            },
            {
                "name": "pgAdmin",
                "desc": "PostgreSQL administration tool",
                "url": "https://pgadmin.org",
                "image_url": "https://pgadmin.org/static/img/logo.png",
                "call_to_action": "Download",
                "tags": ["database", "productivity"],
            },
            {
                "name": "Sublime Text",
                "desc": "Sophisticated text editor",
                "url": "https://sublimetext.com",
                "image_url": "https://sublimetext.com/images/logo.png",
                "call_to_action": "Download",
                "tags": ["editor", "productivity"],
            },
            {
                "name": "PyCharm",
                "desc": "Python IDE by JetBrains",
                "url": "https://jetbrains.com/pycharm",
                "image_url": "https://resources.jetbrains.com/storage/products/pycharm/img/meta/pycharm_logo_300x300.png",
                "call_to_action": "Download",
                "tags": ["ide", "editor"],
            },
        ]

        categories = list(Category.objects.all())
        _ = list(ToolTag.objects.all())
        featured_count = 0

        for i, tool_data in enumerate(tools_data):
            tool_data["category"] = random.choice(categories)
            tag_names = tool_data.pop("tags", [])
            # Make first 10 tools featured
            tool_data["is_featured"] = i < 10

            tool, created = Tool.objects.get_or_create(
                name=tool_data["name"], defaults=tool_data
            )

            if created:
                # Add tags
                for tag_name in tag_names:
                    tag = ToolTag.objects.filter(name=tag_name).first()
                    if tag:
                        tool.tags.add(tag)

                if tool_data["is_featured"]:
                    featured_count += 1

        logger.info(f"Created {len(tools_data)} tools ({featured_count} featured)")
