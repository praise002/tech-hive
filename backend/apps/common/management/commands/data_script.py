import logging
import random
import uuid
from pathlib import Path

import requests
from apps.accounts.models import ContributorOnboarding, User
from apps.accounts.utils import UserRoles
from apps.analytics.choices import DeviceTypeChoices, EventTypeChoices
from apps.analytics.models import SessionMetrics, UserActivity
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
from apps.general.models import SiteDetail
from apps.subscriptions.models import SubscriptionPlan
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)

CURRENT_DIR = Path(__file__).resolve().parent


class CreateData:
    def __init__(self):
        with transaction.atomic():
            self.superuser = self.create_superuser()
            # self.create_groups()
            self.create_categories()
            self.create_tags()
            self.create_tool_tags()
            self.create_site_details()

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

            # Create subscriptions & analytics
            self.create_plans()
            self.create_analytics_data()

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

    def create_site_details(self):
        """Create site specific details from About page"""
        body_text = (
            "Welcome to Tech Hive\n\n"
            "At Tech Hive, we are passionate about everything tech. Whether you're a budding developer, "
            "a seasoned professional, or a tech enthusiast exploring the latest innovations, our platform "
            "is your ultimate destination for insights, resources, and opportunities in the tech world.\n\n"
            "Our Mission\n\n"
            "To inspire and empower the global tech community by delivering high-quality content, tools, "
            "and resources that fuel innovation and drive progress.\n\n"
            "What We Offer\n\n"
            "- Featured Tech Tools: Discover innovative tools and software that can transform the way you work and create.\n"
            "- Tech Jobs: Explore exciting career opportunities and connect with top companies shaping the future.\n"
            "- Tech Articles: Dive into in-depth analyses, tutorials, and stories covering the latest trends and breakthroughs in technology.\n"
            "- Resource Spotlight: Access curated resources to help you learn, grow, and stay ahead in the tech industry.\n\n"
            "Why Tech Hive?\n\n"
            "Tech Hive is more than just a blog; it’s a thriving hub for tech enthusiasts and professionals. "
            "We’re dedicated to fostering a community where knowledge meets opportunity and ideas come to life.\n\n"
            "Join the Buzz\n\n"
            "Stay updated with the latest in tech by following us on our journey. Let's shape the future of technology together!"
        )

        detail_data = {
            "body": body_text,
            "fb": "https://facebook.com/techhive",
            "ln": "https://linkedin.com/company/techhive",
            "x": "https://twitter.com/techhive",
            "ig": "https://instagram.com/techhive",
        }

        # SiteDetail is likely a singleton or we just need one
        if not SiteDetail.objects.exists():
            SiteDetail.objects.create(**detail_data)
            logger.info("Created site details from About page static data")
        else:
            logger.info("Site details already exist")

    # def create_groups(self):
    #     """Create user role groups"""
    #     groups = [
    #         UserRoles.CONTRIBUTOR,
    #         UserRoles.REVIEWER,
    #         UserRoles.EDITOR,
    #         UserRoles.MANAGER,
    #     ]
    #     for group_name in groups:
    #         Group.objects.get_or_create(name=group_name)
    #     logger.info("Created user groups")

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
                "title": "Getting Started with React in 2026",
                "content": """
                <p>Developing with React has never been more exciting. As we move further into 2026, the ecosystem has matured significantly, offering developers unprecedented tools and performance optimizations.</p>
                <h3>Why Choose React?</h3>
                <p>The primary reason developers are flocking to React is its robust community and the seamless integration with modern cloud infrastructures. Whether you are building a small startup app or an enterprise-grade system, React provides the flexibility you need.</p>
                <h3>Core Concepts</h3>
                <ul>
                    <li><strong>Reactive Components</strong>: Building blocks for modern UIs.</li>
                    <li><strong>Efficient State Management</strong>: Keeping your data in sync effortlessly.</li>
                    <li><strong>Advanced Tooling</strong>: Vite and other bundlers making development faster than ever.</li>
                </ul>
                <p>In this guide, we will explore everything from setting up your development environment to deploying your first production-ready application.</p>
                """,
                "category": "Web Development",
                "tags": ["react", "tutorial", "best-practices"],
            },
            {
                "title": "Advanced Django Techniques Every Developer Should Know",
                "content": """
                <p>Deep dive into advanced Django patterns and best practices. If you've already mastered the basics, it's time to level up your skills with these sophisticated techinques.</p>
                <h3>Optimization Strategies</h3>
                <p>Performance is key in modern web applications. We'll look at how Django handles complex rendering cycles and how you can hook into these processes to minimize overhead.</p>
                <blockquote>"Code is like humor. When you have to explain it, it’s bad." – Cory House</blockquote>
                <h3>Advanced Features</h3>
                <p>We will cover topics such as:</p>
                <ul>
                    <li>High-order components and advanced patterns.</li>
                    <li>Custom hooks and middleware implementations.</li>
                    <li>Direct DOM manipulation when absolutely necessary.</li>
                </ul>
                <p>By the end of this article, you'll have a much deeper understanding of the inner workings of Django and how to leverage its full power.</p>
                """,
                "category": "Web Development",
                "tags": ["django", "advanced", "best-practices"],
            },
            {
                "title": "Building Scalable Applications with Node.js",
                "content": """
                <p>Learn how to build scalable and maintainable applications using Node.js. Scaling is not just about handling more traffic; it's about managing complexity as your features grow.</p>
                <h3>Architecture Matters</h3>
                <p>A well-thought-out architecture is the foundation of any scalable Node.js app. We'll discuss microservices, serverless functions, and distributed databases.</p>
                <div class="note">
                    <strong>Note:</strong> Always prioritize consistency and reliability when designing for scale.
                </div>
                <h3>Key Scaling Techniques</h3>
                <p>We'll explore:</p>
                <ul>
                    <li>Horizontal vs Vertical scaling.</li>
                    <li>Caching strategies with Redis and Memcached.</li>
                    <li>Load balancing across multiple instances.</li>
                </ul>
                <p>This article provides a roadmap for taking your Node.js knowledge to the next level in an enterprise environment.</p>
                """,
                "category": "DevOps & Cloud",
                "tags": ["node", "kubernetes", "aws"],
            },
            {
                "title": "The Complete Guide to Python Testing",
                "content": """
                <p>Master testing strategies for modern applications using Python. Reliability is non-negotiable, and a robust testing suite is your best defense against regressions.</p>
                <h3>Types of Tests</h3>
                <p>We'll categorize our testing efforts into three main areas:</p>
                <ol>
                    <li><strong>Unit Testing</strong>: Testing individual functions in isolation.</li>
                    <li><strong>Integration Testing</strong>: Ensuring different parts of Python work together correctly.</li>
                    <li><strong>E2E Testing</strong>: Simulating real user interactions in the browser.</li>
                </ol>
                <p>We will use industry-standard tools and frameworks to demonstrate these concepts in a hands-on way.</p>
                <h3>CI/CD Integration</h3>
                <p>A test suite is only useful if it's run regularly. We'll show you how to integrate your Python tests into GitHub Actions or GitLab CI.</p>
                """,
                "category": "Backend Development",
                "tags": ["python", "testing", "ci-cd"],
            },
            {
                "title": "Optimizing Vue.js Performance: Tips and Tricks",
                "content": """
                <p>Performance optimization strategies for Vue.js that actually work. Users expect instant interactions, and even a few milliseconds can affect your conversion rates.</p>
                <h3>Measuring Performance</h3>
                <p>You can't optimize what you don't measure. We'll start by looking at Lighthouse scores and browser profiling tools specifically for Vue.js apps.</p>
                <h3>Practical Tips</h3>
                <ul>
                    <li>Lazy loading components and assets.</li>
                    <li>Using web workers for heavy computations.</li>
                    <li>Optimizing core bundle sizes.</li>
                    <li>Leverage Vue performance best practices for rendering.</li>
                </ul>
                <p>Following these steps will ensure your Vue.js applications are lightning fast on any device.</p>
                """,
                "category": "Web Development",
                "tags": ["vue", "performance", "optimization"],
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
                    title=template["title"],
                    content=template["content"],
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

    def create_plans(self):
        """Create subscription plans"""
        plans_data = [
            {
                "name": "Free Plan",
                "description": "Access to basic content and features.",
                "price": 0.00,
                "currency": "NGN",
                "billing_cycle": "MONTHLY",
                "features": {
                    "ad_free": False,
                    "premium_content": False,
                    "download_resources": False,
                },
                "paystack_plan_code": "PLN_free123",
            },
            {
                "name": "Premium Monthly",
                "description": "Unlock all premium articles and resources.",
                "price": 5000.00,
                "currency": "NGN",
                "billing_cycle": "MONTHLY",
                "features": {
                    "ad_free": True,
                    "premium_content": True,
                    "download_resources": True,
                },
                "paystack_plan_code": "PLN_premium_monthly",
            },
            {
                "name": "Premium Yearly",
                "description": "Get 2 months free with annual billing.",
                "price": 50000.00,
                "currency": "NGN",
                "billing_cycle": "YEARLY",
                "features": {
                    "ad_free": True,
                    "premium_content": True,
                    "download_resources": True,
                },
                "paystack_plan_code": "PLN_premium_yearly",
            },
        ]

        for plan_data in plans_data:
            SubscriptionPlan.objects.get_or_create(
                paystack_plan_code=plan_data["paystack_plan_code"], defaults=plan_data
            )
        logger.info(f"Created {len(plans_data)} subscription plans")

    def create_analytics_data(self):
        """Generate dummy analytics data for users"""
        all_users = self.contributors + self.reviewers + self.editors + [self.superuser]
        device_types = [d[0] for d in DeviceTypeChoices.choices]
        event_types = [e[0] for e in EventTypeChoices.choices]

        # Generate sessions for the last 30 days
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=30)

        total_sessions = 0
        total_activities = 0

        for user in all_users:
            # Each user has 5-15 sessions
            num_sessions = random.randint(5, 15)

            for _ in range(num_sessions):
                # Random start time within last 30 days
                delta_days = random.randint(0, 30)
                session_start = end_date - timezone.timedelta(
                    days=delta_days,
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                )
                session_duration = random.randint(30, 1800)  # 30s to 30m
                session_end = session_start + timezone.timedelta(
                    seconds=session_duration
                )

                session_id = str(uuid.uuid4())
                device = random.choice(device_types)

                # Create Session
                session = SessionMetrics.objects.create(
                    session_id=session_id,
                    user=user,
                    start_time=session_start,
                    end_time=session_end,
                    page_count=random.randint(1, 10),
                    total_duration=session_duration,
                    device_type=device,
                    is_bounce=random.choice([True, False, False]),  # 33% bounce rate
                )
                total_sessions += 1

                # Create 3-10 activities per session if not bounce, else 1
                num_activities = 1 if session.is_bounce else random.randint(3, 10)

                current_time = session_start
                for _ in range(num_activities):
                    event = random.choice(event_types)
                    # Advance time slightly
                    current_time += timezone.timedelta(seconds=random.randint(5, 120))
                    if current_time > session_end:
                        current_time = session_end

                    UserActivity.objects.create(
                        session=session,
                        user=user,
                        event_type=event,
                        page_url=f"https://techhive.com/articles/{uuid.uuid4()}",
                        referrer="https://google.com",
                        device_type=device,
                        duration_seconds=random.randint(5, 300),
                        timestamp=current_time,
                        load_time_ms=random.randint(100, 2000),
                    )
                    total_activities += 1

        logger.info(
            f"Created {total_sessions} analytics sessions with {total_activities} activities"
        )

    def create_jobs(self):
        """Create 20+ job postings"""
        jobs_data = [
            {
                "title": "Senior Full Stack Developer",
                "company": "TechCorp Inc",
                "desc": (
                    "<p>TechCorp Inc is looking for a Senior Full Stack Developer to lead our core engineering team in building the next generation of enterprise-level software solutions. In this role, you will be responsible for architecting, developing, and deploying high-performance web applications that serve millions of users worldwide.</p>"
                    "<p>You will work closely with cross-functional teams, including product managers, UI/UX designers, and backend engineers, to translate complex requirements into scalable and maintainable code. We value innovation, collaboration, and a deep passion for clean engineering practices.</p>"
                    "<p>As a senior leader, you will also play a pivotal role in shaping our technical roadmap, selecting the latest technologies, and ensuring that our systems are built for long-term reliability and growth. If you thrive in a fast-paced environment and love solving difficult technical challenges, we want you on our team.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Expertise:</strong> 5+ years of professional experience with React, Node.js, and TypeScript.</li>"
                    "<li><strong>Architecture:</strong> Deep understanding of microservices, serverless functions, and distributed systems.</li>"
                    "<li><strong>Cloud:</strong> Hands-on experience with AWS services (EC2, S3, Lambda, RDS) and Infrastructure as Code (Terraform/CloudFormation).</li>"
                    "<li><strong>Database:</strong> Proficiency in both SQL (PostgreSQL, MySQL) and NoSQL (MongoDB, Redis) databases.</li>"
                    "<li><strong>Tooling:</strong> Strong command of Git, Docker, Kubernetes, and modern CI/CD pipelines.</li>"
                    "<li><strong>Soft Skills:</strong> Exceptional communication skills and a proven ability to lead and mentor junior engineering talent.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Leadership:</strong> Act as the primary technical lead for major product initiatives from conception to deployment.</li>"
                    "<li><strong>Development:</strong> Write clean, testable, and efficient code for both frontend and backend modules.</li>"
                    "<li><strong>Mentorship:</strong> Conduct detailed code reviews and provide constructive feedback to foster a culture of technical excellence.</li>"
                    "<li><strong>Architecture:</strong> Design and document system architectures, ensuring scalability, security, and performance.</li>"
                    "<li><strong>Collaboration:</strong> Partner with the product team to define feature scopes and technical specifications.</li>"
                    "<li><strong>Optimization:</strong> Continuously monitor and optimize application performance, identifying and resolving bottlenecks in real-time.</li>"
                    "</ul>"
                ),
                "location": "San Francisco, CA",
                "salary": 150000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudScale Solutions",
                "desc": (
                    "<p>CloudScale Solutions is seeking a DevOps Engineer to help us automate and scale our rapidly expanding infrastructure. Our platform handles petabytes of data, and we need an expert who can ensure that our deployment pipelines are seamless and our production environments are rock-solid.</p>"
                    "<p>You will be the bridge between development and operations, implementing Site Reliability Engineering (SRE) principles to improve system uptime and developer productivity. We are a remote-first team that values autonomy, transparency, and the pursuit of operational excellence.</p>"
                    "<p>Your mission will be to build a world-class observation and automation stack that allows our product teams to ship code faster and with higher confidence. If you dream in YAML and live for 99.99% uptime, you'll fit right in.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Experience:</strong> 3+ years of experience in DevOps, Linux administration, or Cloud Engineering.</li>"
                    "<li><strong>Automation:</strong> Mastery of CI/CD tools like GitLab CI, GitHub Actions, or Jenkins.</li>"
                    "<li><strong>Orchestration:</strong> Strong experience with Kubernetes (EKS/GKE) and Helm chart management.</li>"
                    "<li><strong>Monitoring:</strong> Proficiency with Prometheus, Grafana, and the ELK/Loki stack for observability.</li>"
                    "<li><strong>Scripting:</strong> Advanced knowledge of Python, Bash, or Go for automation tasks.</li>"
                    "<li><strong>Security:</strong> Familiarity with DevSecOps practices, including vulnerability scanning and secret management (HashiCorp Vault).</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Infrastructure:</strong> Design and maintain multi-region cloud infrastructure using Terraform.</li>"
                    "<li><strong>Automation:</strong> Build and optimize automated deployment pipelines for containerized applications.</li>"
                    "<li><strong>Reliability:</strong> Manage on-call rotations and participate in incident post-mortems to improve system resilience.</li>"
                    "<li><strong>Scaling:</strong> Implement auto-scaling strategies to handle traffic spikes and optimize cloud costs.</li>"
                    "<li><strong>Documentation:</strong> Maintain detailed documentation of infrastructure designs, runbooks, and security policies.</li>"
                    "<li><strong>Innovation:</strong> Constantly evaluate new tools and technologies to improve our deployment and monitoring ecosystem.</li>"
                    "</ul>"
                ),
                "location": "Remote",
                "salary": 140000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Frontend Developer (React)",
                "company": "StartupXYZ",
                "desc": (
                    "<p>StartupXYZ is on a mission to revolutionize user social interaction, and we need a Frontend Developer who is passionate about creating stunning and intuitive web experiences. You will work on a fast-paced team where your code will impact millions of users from day one.</p>"
                    "<p>We believe that frontend development is an art form. You'll be working with a highly talented design team to bring pixel-perfect mockups to life, ensuring that every animation is smooth and every interaction feels natural. We use a modern stack centered around React, Next.js, and Tailwind CSS.</p>"
                    "<p>As an early member of the team, you'll have a major say in our component library, state management strategies, and overall frontend architecture. If you love building the 'wow' factor into web apps, StartupXYZ is the place for you.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>React Mastery:</strong> 3+ years of experience building complex SPAs using React hooks and functional components.</li>"
                    "<li><strong>Style:</strong> Expertise in Tailwind CSS, Styled Components, or advanced CSS/SASS.</li>"
                    "<li><strong>State:</strong> Deep knowledge of Redux Toolkit, MobX, or React Query for data fetching.</li>"
                    "<li><strong>Testing:</strong> Experience with Jest, React Testing Library, and Cypress for E2E testing.</li>"
                    "<li><strong>Performance:</strong> Proven ability to optimize web vitals (LCP, FID, CLS) and minimize bundle sizes.</li>"
                    "<li><strong>Graphics:</strong> Familiarity with SVG animations, Framer Motion, or Three.js is a significant plus.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>UI Development:</strong> Build and maintain a library of reusable, accessible React components.</li>"
                    "<li><strong>Integration:</strong> Seamlessly integrate frontend components with RESTful and GraphQL APIs.</li>"
                    "<li><strong>Design:</strong> Collaborate with UI/UX designers to translate Figma mockups into functional code.</li>"
                    "<li><strong>Testing:</strong> Write unit and integration tests to ensure a bug-free user experience.</li>"
                    "<li><strong>SEO:</strong> Implement best practices for SEO and accessibility (A11Y) across the entire platform.</li>"
                    "<li><strong>Mentorship:</strong> Share knowledge with the team through workshops and internal documentation.</li>"
                    "</ul>"
                ),
                "location": "New York, NY",
                "salary": 120000,
                "job_type": "FULL_TIME",
                "work_mode": "ONSITE",
            },
            {
                "title": "Data Scientist",
                "company": "AI Labs",
                "desc": (
                    "<p>AI Labs is seeking a brilliant Data Scientist to join our research and development team. You will be working at the cutting edge of machine learning, designing algorithms that solve complex real-world problems. Our team is composed of PhDs and researchers from top universities, and we foster an environment of academic rigor and practical impact.</p>"
                    "<p>In this role, you will have access to massive compute resources and proprietary datasets. You will be responsible for the entire model lifecycle, from data preprocessing and feature engineering to model training, evaluation, and deployment. We value reproducibility and transparency in our research methods.</p>"
                    "<p>If you are passionate about pushing the boundaries of what AI can achieve and want to work on projects that have a measurable positive impact on society, AI Labs is the perfect home for your talents.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Education:</strong> MS or PhD in Computer Science, Statistics, Mathematics, or a related quantitative field.</li>"
                    "<li><strong>Machine Learning:</strong> Deep understanding of modern ML algorithms (Random Forest, XGBoost, Neural Networks).</li>"
                    "<li><strong>Frameworks:</strong> Proficiency in PyTorch, TensorFlow, or JAX.</li>"
                    "<li><strong>Data Processing:</strong> Expert-level skills in Python (Pandas, NumPy) and SQL.</li>"
                    "<li><strong>Communication:</strong> Ability to visualize complex data insights and present findings to non-technical stakeholders.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Research:</strong> Read and implement state-of-the-art papers to improve our core algorithms.</li>"
                    "<li><strong>Modeling:</strong> Develop, train, and validate predictive models for various business use cases.</li>"
                    "<li><strong>Collaboration:</strong> Work closely with backend engineers to deploy models into production environments.</li>"
                    "<li><strong>Analysis:</strong> Conduct deep-dive exploratory data analysis to uncover hidden patterns and trends.</li>"
                    "<li><strong>Strategy:</strong> Helps shape the company's data strategy and identify new opportunities for AI application.</li>"
                    "</ul>"
                ),
                "location": "Boston, MA",
                "salary": 160000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Mobile Developer (Flutter)",
                "company": "MobileFirst",
                "desc": (
                    "<p>MobileFirst is a boutique agency specializing in creating high-performance cross-platform mobile applications. We are looking for a Flutter Developer who treats mobile development as a craft, not just a job. You will be building beautiful, animation-rich apps for some of the world's leading brands.</p>"
                    "<p>Our team believes in the 'write once, run everywhere' philosophy without compromising on native-like performance. You will be working with the latest features of Dart and Flutter, implementing custom render objects, and optimizing apps for 60fps performance on even low-end devices.</p>"
                    "<p>Join us if you care about pixel perfection, smooth transitions, and delivering a user experience that delights customers on both iOS and Android platforms.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Experience:</strong> 2+ years of professional experience building and deploying Flutter applications.</li>"
                    "<li><strong>Dart:</strong> Deep knowledge of the Dart programming language, including async/await and streams.</li>"
                    "<li><strong>State Management:</strong> Proficiency with BLoC, Riverpod, or Provider patterns.</li>"
                    "<li><strong>Native:</strong> Experience writing platform channels (MethodChannel) for iOS (Swift) and Android (Kotlin) is a huge plus.</li>"
                    "<li><strong>UI/UX:</strong> Strong understanding of Material Design and Cupertino guidelines.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Development:</strong> Build robust, scalable, and maintainable mobile applications using Flutter.</li>"
                    "<li><strong>Animation:</strong> Create complex custom animations and transitions to enhance user engagement.</li>"
                    "<li><strong>Optimization:</strong> Profile and optimize app performance using Dart DevTools.</li>"
                    "<li><strong>Testing:</strong> Write widget and integration tests to ensure app stability across devices.</li>"
                    "<li><strong>Deployment:</strong> Manage the submission and release process for the App Store and Google Play Store.</li>"
                    "</ul>"
                ),
                "location": "Austin, TX",
                "salary": 110000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Backend Engineer (Python)",
                "company": "DataDriven Corp",
                "desc": (
                    "<p>DataDriven Corp is looking for a Backend Engineer to build the engine that powers our real-time analytics platform. You will process thousands of requests per second, ensuring data integrity and low-latency responses for our global customer base.</p>"
                    "<p>We primarily use Python (Django/FastAPI) and Go for our microservices. You will face challenges related to database locking, cache invalidation, and distributed consistency. This is a role for someone who enjoys digging into the internals of frameworks and databases.</p>"
                    "<p>If you are obsessive about API design, code purity, and system architecture, you will find a challenging and rewarding career path here at DataDriven Corp.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Backend:</strong> 4+ years of experience with Python (Django, FastAPI, or Flask).</li>"
                    "<li><strong>Databases:</strong> Advanced knowledge of SQL optimization, indexing, and query planning (PostgreSQL).</li>"
                    "<li><strong>Async:</strong> Experience with asynchronous programming (AsyncIO, Celery, Redis).</li>"
                    "<li><strong>Testing:</strong> Strong belief in TDD and experience with PyTest.</li>"
                    "<li><strong>Design:</strong> Proficiency in designing RESTful APIs and understanding GraphQL principles.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>API Design:</strong> Design and implement secure, versioned, and documented public APIs.</li>"
                    "<li><strong>Optimization:</strong> Refactor legacy code to improve performance and maintainability.</li>"
                    "<li><strong>Security:</strong> Implement robust authentication and authorization mechanisms (OAuth2, JWT).</li>"
                    "<li><strong>Integration:</strong> Connect internal services using message queues (RabbitMQ, Kafka).</li>"
                    "<li><strong>Review:</strong> Participate in rigorous code reviews to maintain high engineering standards.</li>"
                    "</ul>"
                ),
                "location": "Seattle, WA",
                "salary": 135000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Security Engineer",
                "company": "SecureNet",
                "desc": (
                    "<p>SecureNet is the industry leader in cybersecurity solutions, and we are hiring a Security Engineer to protect our infrastructure and our customers' data. In this role, you will be the first line of defense against sophisticated cyber threats.</p>"
                    "<p>You will work on both offensive and defensive security operations. This includes conducting penetration tests, vulnerability assessments, and designing secure network architectures. We value proactive thinking and a deep understanding of the threat landscape.</p>"
                    "<p>You will also collaborate with our development teams to integrate security into the SDLC (DevSecOps), ensuring that code is secure by design. If you live and breathe InfoSec, this is the job for you.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Security:</strong> 3+ years of experience in Information Security or Network Security.</li>"
                    "<li><strong>Tools:</strong> Proficiency with tools like Burp Suite, Metasploit, Nmap, and Wireshark.</li>"
                    "<li><strong>Cloud:</strong> Experience securing cloud environments (AWS/Azure) and containerized workloads.</li>"
                    "<li><strong>Coding:</strong> Ability to write scripts in Python, Bash, or Ruby to automate security tasks.</li>"
                    "<li><strong>Compliance:</strong> Knowledge of standards such as SOC2, ISO 27001, and GDPR.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Auditing:</strong> Conduct regular security audits and vulnerability scans of our infrastructure.</li>"
                    "<li><strong>Incident Response:</strong> Lead the investigation and remediation of security incidents.</li>"
                    "<li><strong>Training:</strong> developing and delivering security awareness training to employees.</li>"
                    "<li><strong>Architecture:</strong> Review and approve security architecture for new projects and features.</li>"
                    "<li><strong>Compliance:</strong> Ensure that all systems and processes meet regulatory compliance requirements.</li>"
                    "</ul>"
                ),
                "location": "Washington, DC",
                "salary": 145000,
                "job_type": "FULL_TIME",
                "work_mode": "ONSITE",
            },
            {
                "title": "QA Automation Engineer",
                "company": "QualityFirst",
                "desc": (
                    "<p>QualityFirst is dedicated to delivering bug-free software to our clients. We are seeking a QA Automation Engineer to build and maintain comprehensive test suites that ensure our releases are stable and reliable.</p>"
                    "<p>You will move beyond manual testing to create robust, automated frameworks that run on every commit. You will work closely with developers to understand feature requirements and edge cases, ensuring that quality is baked in from the start.</p>"
                    "<p>This role requires a blend of coding skills and a tester's mindset. You will be responsible for the health of our CI/CD pipelines and the confidence of our release process.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Automation:</strong> 3+ years of experience writing automated tests using Cypress, Playwright, or Selenium.</li>"
                    "<li><strong>Coding:</strong> solid programming skills in JavaScript/TypeScript or Python.</li>"
                    "<li><strong>API Testing:</strong> Experience testing REST and GraphQL APIs using tools like Postman or Supertest.</li>"
                    "<li><strong>CI/CD:</strong> Familiarity with integrating tests into Jenkins, GitHub Actions, or CircleCI.</li>"
                    "<li><strong>Process:</strong> Understanding of Agile/Scrum methodologies and bug tracking tools (Jira).</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Frameworks:</strong> Design and implement scalable test automation frameworks for web and mobile.</li>"
                    "<li><strong>Scripts:</strong> Write clear, concise, and maintainable test scripts for regression and smoke testing.</li>"
                    "<li><strong>Analysis:</strong> Analyze test results, report defects, and track them to closure.</li>"
                    "<li><strong>Collaboration:</strong> advocate for testability and quality during design and code reviews.</li>"
                    "<li><strong>Performance:</strong> Conduct performance and load testing using tools like k6 or JMeter.</li>"
                    "</ul>"
                ),
                "location": "Remote",
                "salary": 105000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "UI/UX Designer",
                "company": "DesignHub",
                "desc": (
                    "<p>DesignHub is looking for a UI/UX Designer to create intuitive and visually stunning user experiences for our suite of creative tools. You will be responsible for the entire design process, from user research and wireframing to high-fidelity prototyping and visual design.</p>"
                    "<p>We believe that good design is invisible. You should be passionate about solving user problems through elegant and simple interfaces. You will work in a collaborative environment where feedback is encouraged and design systems are cherished.</p>"
                    "<p>If you have a portfolio that demonstrates a strong understanding of typography, color theory, and interaction design, we would love to see your work.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Design:</strong> 3+ years of experience in product design, UI/UX, or interaction design.</li>"
                    "<li><strong>Tools:</strong> Mastery of Figma, Sketch, or Adobe XD.</li>"
                    "<li><strong>Prototyping:</strong> Ability to create interactive prototypes using Principle, Protopie, or Figma.</li>"
                    "<li><strong>Research:</strong> Experience conducting user interviews, usability testing, and heuristic evaluations.</li>"
                    "<li><strong>Systems:</strong> Experience building and maintaining comprehensive design systems.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Concepts:</strong> Translate high-level requirements into interaction flows and artifacts.</li>"
                    "<li><strong>Visuals:</strong> Create beautiful, pixel-perfect visual designs that align with our brand identity.</li>"
                    "<li><strong>Collaboration:</strong> Work closely with developers to ensure design intent is preserved in implementation.</li>"
                    "<li><strong>Research:</strong> Conduct user research to validate design decisions and identify areas for improvement.</li>"
                    "<li><strong>Evolution:</strong> Continuously iterate on the product based on user feedback and analytics data.</li>"
                    "</ul>"
                ),
                "location": "Los Angeles, CA",
                "salary": 115000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Database Administrator",
                "company": "DataVault",
                "desc": (
                    "<p>DataVault manages mission-critical data for Fortune 500 companies. We are seeking a Senior Database Administrator to ensure the performance, availability, and security of our massive database clusters.</p>"
                    "<p>You will deal with challenges related to high availability, disaster recovery, and database tuning at scale. You should be comfortable managing both relational and NoSQL databases in a hybrid cloud environment.</p>"
                    "<p>This is a high-responsibility role where your expertise will directly impact the stability of our clients' businesses. If you are a database wizard who loves optimizing query plans, come join us.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Databases:</strong> 5+ years of experience administering PostgreSQL, MySQL, or Oracle.</li>"
                    "<li><strong>NoSQL:</strong> Experience with MongoDB, Cassandra, or DynamoDB.</li>"
                    "<li><strong>Cloud:</strong> Proficiency with AWS RDS, Aurora, or Google Cloud SQL.</li>"
                    "<li><strong>Tuning:</strong> Deep understanding of query optimization, indexing strategies, and storage engines.</li>"
                    "<li><strong>Scripting:</strong> Ability to write complex scripts in Bash, Python, or PL/SQL.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Maintenance:</strong> Perform routine database maintenance, upgrades, and patches with minimal downtime.</li>"
                    "<li><strong>Backup:</strong> Design and implement robust backup and disaster recovery strategies.</li>"
                    "<li><strong>Monitoring:</strong> Set up comprehensive monitoring and alerting for database health and performance.</li>"
                    "<li><strong>Security:</strong> Manage database access controls and ensure data encryption at rest and in transit.</li>"
                    "<li><strong>Support:</strong> Provide 24/7 support for critical database issues and performance incidents.</li>"
                    "</ul>"
                ),
                "location": "Chicago, IL",
                "salary": 125000,
                "job_type": "FULL_TIME",
                "work_mode": "ONSITE",
            },
            {
                "title": "Machine Learning Engineer",
                "company": "AI Innovations",
                "desc": (
                    "<p>AI Innovations is a startup focused on democratizing access to state-of-the-art machine learning models. We are looking for an ML Engineer who can bridge the gap between research and production.</p>"
                    "<p>Your main responsibility will be building and maintaining the pipelines that train, evaluate, and deploy our models. You should be comfortable working with large datasets and dealing with the challenges of distributed training.</p>"
                    "<p>If you are excited about the practical applications of AI and want to build systems that scale to millions of users, this is the place for you.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>ML Frameworks:</strong> Proficiency in TensorFlow or PyTorch.</li>"
                    "<li><strong>Data Engineering:</strong> Experience with Spark, Beam, or similar data processing frameworks.</li>"
                    "<li><strong>Cloud:</strong> Familiarity with Google Cloud AI Platform or AWS SageMaker.</li>"
                    "<li><strong>DevOps:</strong> Experience with Docker and Kubernetes for model serving.</li>"
                    "<li><strong>Languages:</strong> Strong Python and C++ skills.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Pipelines:</strong> Build end-to-end ML pipelines for data ingestion, training, and deployment.</li>"
                    "<li><strong>Optimization:</strong> Optimize model inference latency and throughput.</li>"
                    "<li><strong>Monitoring:</strong> Implement monitoring for model drift and data quality issues.</li>"
                    "<li><strong>Collaboration:</strong> Work with data scientists to productize experimental models.</li>"
                    "<li><strong>Infrastructure:</strong> Manage and scale our GPU cluster infrastructure.</li>"
                    "</ul>"
                ),
                "location": "Remote",
                "salary": 155000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Technical Writer",
                "company": "DocuTech",
                "desc": (
                    "<p>DocuTech is seeking a Technical Writer who is passionate about making complex technology easy to understand. You will work closely with our engineering teams to create documentation that delights our users.</p>"
                    "<p>We believe that documentation is a key part of the user experience. You will be responsible for creating API references, tutorials, and conceptual guides that help developers integrate our products.</p>"
                    "<p>If you have a knack for storytelling and a technical background, we want to hear from you.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Writing:</strong> Excellent written communication skills and attention to detail.</li>"
                    "<li><strong>Technical:</strong> Ability to read code in languages like Python, JavaScript, or Java.</li>"
                    "<li><strong>Tools:</strong> Experience with docs-as-code tools like Sphinx, Jekyll, or Docusaurus.</li>"
                    "<li><strong>Process:</strong> Familiarity with Git and the software development lifecycle.</li>"
                    "<li><strong>Portfolio:</strong> A portfolio of technical writing samples is required.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Documentation:</strong> Write and maintain developer documentation for our APIs and SDKs.</li>"
                    "<li><strong>Tutorials:</strong> Create step-by-step tutorials and code samples to help users get started.</li>"
                    "<li><strong>Review:</strong> Edit and review content produced by engineers and other contributors.</li>"
                    "<li><strong>Strategy:</strong> Help define the information architecture and content strategy for our docs site.</li>"
                    "<li><strong>Feedback:</strong> Gather feedback from users to improve the quality and clarity of our documentation.</li>"
                    "</ul>"
                ),
                "location": "Remote",
                "salary": 85000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Product Manager",
                "company": "ProductCo",
                "desc": (
                    "<p>ProductCo is looking for a Product Manager to lead the development of our flagship product. You will be responsible for defining the product vision, strategy, and roadmap.</p>"
                    "<p>You will work cross-functionally with engineering, design, and marketing to deliver features that solve real user problems. You should be data-driven but also have a strong product intuition.</p>"
                    "<p>We are looking for someone who is comfortable navigating ambiguity and can align stakeholders around a shared goal.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Experience:</strong> 5+ years of product management experience in B2B SaaS.</li>"
                    "<li><strong>Analysis:</strong> Strong analytical skills and experience with tools like Amplitude or Mixpanel.</li>"
                    "<li><strong>Communication:</strong> Excellent verbal and written communication skills.</li>"
                    "<li><strong>Leadership:</strong> Proven ability to lead cross-functional teams without formal authority.</li>"
                    "<li><strong>Technical:</strong> Sufficient technical understanding to credible discussions with engineers.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Strategy:</strong> Define the product vision and strategy based on market research and user feedback.</li>"
                    "<li><strong>Roadmap:</strong> precise maintain a prioritized product roadmap that aligns with company goals.</li>"
                    "<li><strong>Execution:</strong> Drive the product development process from concept to launch.</li>"
                    "<li><strong>Launch:</strong> Coordinate with marketing and sales to ensure successful product launches.</li>"
                    "<li><strong>Metrics:</strong> Define and track key product metrics to measure success.</li>"
                    "</ul>"
                ),
                "location": "San Francisco, CA",
                "salary": 170000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Junior Developer",
                "company": "CodeAcademy Pro",
                "desc": (
                    "<p>CodeAcademy Pro is hiring Junior Developers to join our apprenticeship program. This is a unique opportunity to learn from experienced mentors while working on real production code.</p>"
                    "<p>We don't expect you to know everything. We are looking for potential, curiosity, and a willingness to learn. You will be paired with a senior engineer who will guide you through your first year.</p>"
                    "<p>If you are a recent bootcamp grad or self-taught developer looking for your first break, applying to CodeAcademy Pro is the best decision you can make.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Basics:</strong> Solid understanding of HTML, CSS, and JavaScript.</li>"
                    "<li><strong>Backend:</strong> Some exposure to a backend language like Python, Ruby, or Node.js.</li>"
                    "<li><strong>Growth Mindset:</strong> A strong desire to learn and improve your skills.</li>"
                    "<li><strong>Projects:</strong> Personal projects or a portfolio that demonstrates your coding ability.</li>"
                    "<li><strong>Communication:</strong> Ability to ask good questions and communicate your thought process.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Learning:</strong> Dedicate time to learning new technologies and best practices.</li>"
                    "<li><strong>Coding:</strong> Contribute to bug fixes and small features under supervision.</li>"
                    "<li><strong>Testing:</strong> Write unit tests to ensure the quality of your code.</li>"
                    "<li><strong>Review:</strong> Participate in code reviews to learn from others and improve your code style.</li>"
                    "<li><strong>Documentation:</strong> Help improve our internal documentation and onboarding guides.</li>"
                    "</ul>"
                ),
                "location": "Remote",
                "salary": 70000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Solutions Architect",
                "company": "CloudArch",
                "desc": (
                    "<p>CloudArch helps enterprises migrate their legacy workloads to the cloud. We are looking for a Solutions Architect to design scalable and secure cloud architectures for our clients.</p>"
                    "<p>You will work with clients to understand their business requirements and technical constraints. You will then design a migration plan and help them implement it using best practices.</p>"
                    "<p>This role requires a deep understanding of cloud services and the ability to communicate technical concepts to both technical and non-technical audiences.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Certifications:</strong> AWS Certified Solutions Architect or Azure Solutions Architect Expert.</li>"
                    "<li><strong>Experience:</strong> 5+ years of experience designing and deploying cloud solutions.</li>"
                    "<li><strong>Architecture:</strong> Deep knowledge of microservices, serverless, and event-driven architectures.</li>"
                    "<li><strong>Consulting:</strong> Experience working in a customer-facing role.</li>"
                    "<li><strong>Migration:</strong> Experience with large-scale cloud migrations.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Design:</strong> Create detailed architectural diagrams and design documents.</li>"
                    "<li><strong>Advisory:</strong> Advise clients on cloud best practices, cost optimization, and security.</li>"
                    "<li><strong>POCs:</strong> Build proofs of concept to demonstrate the feasibility of your designs.</li>"
                    "<li><strong>Leadership:</strong> Lead technical workshops and design reviews with client teams.</li>"
                    "<li><strong>Mentorship:</strong> Mentor junior engineers and architects on the team.</li>"
                    "</ul>"
                ),
                "location": "New York, NY",
                "salary": 165000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Blockchain Developer",
                "company": "CryptoTech",
                "desc": (
                    "<p>CryptoTech is building the next generation of decentralized finance (DeFi) applications. We are looking for a Blockchain Developer to help us build secure and efficient smart contracts.</p>"
                    "<p>You will work with Solidity and the Ethereum Virtual Machine (EVM) to develop complex financial protocols. You should have a deep understanding of blockchain security and gas optimization.</p>"
                    "<p>If you are passionate about Web3 and want to build the future of finance, we want to talk to you.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Smart Contracts:</strong> expert proficiency in Solidity and development tools like Hardhat or Foundry.</li>"
                    "<li><strong>Web3:</strong> Experience with Web3.js, Ethers.js, and interacting with nodes.</li>"
                    "<li><strong>Security:</strong> Understanding of common smart contract vulnerabilities (reentrancy, etc.).</li>"
                    "<li><strong>DeFi:</strong> Familiarity with major DeFi protocols (Uniswap, Aave, Compound).</li>"
                    "<li><strong>Cryptography:</strong> Basic understanding of public-key cryptography and hashing algorithms.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Development:</strong> Write, test, and deploy secure smart contracts.</li>"
                    "<li><strong>Auditing:</strong> Participate in internal audits and coordinate with external audit firms.</li>"
                    "<li><strong>Integration:</strong> Build frontend interfaces to interact with your smart contracts.</li>"
                    "<li><strong>Research:</strong> Keep up with the latest developments in the blockchain ecosystem (L2s, ZK-rollups).</li>"
                    "<li><strong>Innovation:</strong> Propose and prototype new DeFi mechanisms and products.</li>"
                    "</ul>"
                ),
                "location": "Miami, FL",
                "salary": 150000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Site Reliability Engineer",
                "company": "ReliableOps",
                "desc": (
                    "<p>ReliableOps helps fast-growing companies scale their infrastructure. We are looking for an SRE who cares deeply about reliability, observability, and automation.</p>"
                    "<p>You will work with our clients to improve their system uptime and performance. You will implement monitoring dashboards, set up alerting rules, and help them adopt SRE practices like SLIs and SLOs.</p>"
                    "<p>This is a hands-on role where you will be writing code to automate operations and debugging complex production issues.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Linux:</strong> Deep understanding of Linux internals and networking.</li>"
                    "<li><strong>Cloud:</strong> Expertise in AWS, GCP, or Azure.</li>"
                    "<li><strong>IaC:</strong> Proficiency with Terraform or Ansible.</li>"
                    "<li><strong>Observability:</strong> Experience with Prometheus, Grafana, Datadog or honeycomb.</li>"
                    "<li><strong>Coding:</strong> Ability to code in Go or Python.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Reliability:</strong> Identify and fix single points of failure in client infrastructures.</li>"
                    "<li><strong>Automation:</strong> Automate manual runbooks and operational tasks.</li>"
                    "<li><strong>Monitoring:</strong> Build comprehensive monitoring and alerting systems.</li>"
                    "<li><strong>Incident Management:</strong> Help clients manage and learn from incidents.</li>"
                    "<li><strong>Capacity Planning:</strong> assist with capacity planning and performance tuning.</li>"
                    "</ul>"
                ),
                "location": "Remote",
                "salary": 140000,
                "job_type": "FULL_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "iOS Developer",
                "company": "AppleDev Corp",
                "desc": (
                    "<p>AppleDev Corp creates award-winning iOS applications that are featured on the App Store. We are looking for an iOS Developer who takes pride in building polished native experiences.</p>"
                    "<p>You will work with Swift and SwiftUI to build apps that feel at home on the latest iPhones and iPads. We push the boundaries of what is possible on iOS, using the latest APIs as soon as they are announced.</p>"
                    "<p>If you care about smooth animations, accessibility, and clean architecture, you will fit right in.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>iOS:</strong> 3+ years of experience with iOS development using Swift.</li>"
                    "<li><strong>UI:</strong> strong experience with SwiftUI and Auto Layout (UIKit).</li>"
                    "<li><strong>Architecture:</strong> Familiarity with MVVM, Coordinator pattern, and Clean Architecture.</li>"
                    "<li><strong>Concurrency:</strong> Understanding of GCD and Swift Concurrency (async/await).</li>"
                    "<li><strong>Tools:</strong> Proficiency with Xcode, Instruments, and CocoaPods/SPM.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Development:</strong> Build high-quality iOS apps from concept to submission.</li>"
                    "<li><strong>UI/UX:</strong> Implement complex custom UI components and animations.</li>"
                    "<li><strong>Performance:</strong> Optimize app startup time, memory usage, and battery life.</li>"
                    "<li><strong>Testing:</strong> Write unit and UI tests to ensure regression-free releases.</li>"
                    "<li><strong>Maintenance:</strong> Keep apps updated with the latest iOS versions and features.</li>"
                    "</ul>"
                ),
                "location": "Cupertino, CA",
                "salary": 130000,
                "job_type": "FULL_TIME",
                "work_mode": "ONSITE",
            },
            {
                "title": "Android Developer",
                "company": "DroidApps",
                "desc": (
                    "<p>DroidApps is a leading Android development shop. We are looking for an Android Developer who loves the diversity and scale of the Android ecosystem.</p>"
                    "<p>You will write modern Kotlin code using Jetpack libraries. You will advocate for Material Design principles and ensure our apps look great on everything from a Pixel phone to a Samsung tablet.</p>"
                    "<p>We value clean code, automated testing, and a user-centric mindset.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Android:</strong> 3+ years of experience with Android development.</li>"
                    "<li><strong>Kotlin:</strong> Expert knowledge of Kotlin and coroutines.</li>"
                    "<li><strong>Jetpack:</strong> Experience with Jetpack Compose, ViewModel, Room, and Navigation.</li>"
                    "<li><strong>Architecture:</strong> Understanding of MVI or MVVM architectures.</li>"
                    "<li><strong>Tools:</strong> Proficiency with Android Studio and Gradle.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Development:</strong> Architect and build advanced Android applications.</li>"
                    "<li><strong>UI:</strong> Create responsive UIs that adapt to different screen sizes and form factors.</li>"
                    "<li><strong>Integration:</strong> Integrate with backend APIs and third-party SDKs.</li>"
                    "<li><strong>Quality:</strong> Ensure code quality through code reviews and static analysis tools.</li>"
                    "<li><strong>Release:</strong> Manage the rollout of updates via the Google Play Console.</li>"
                    "</ul>"
                ),
                "location": "Mountain View, CA",
                "salary": 130000,
                "job_type": "FULL_TIME",
                "work_mode": "HYBRID",
            },
            {
                "title": "Game Developer",
                "company": "GameStudio",
                "desc": (
                    "<p>GameStudio is working on the next big indie hit. We are looking for a Game Developer who is passionate about gameplay programming and game mechanics.</p>"
                    "<p>You will work with Unity or Unreal Engine to bring our game designers' vision to life. You will be tuning character movement, implementing combat systems, and optimizing rendering performance.</p>"
                    "<p>We are a small, tight-knit team where everyone wears multiple hats. Your creative input will be valued just as much as your code.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Engine:</strong> Strong experience with Unity (C#) or Unreal Engine (C++/Blueprints).</li>"
                    "<li><strong>Math:</strong> Solid 3D math skills (vectors, matrices, quaternions).</li>"
                    "<li><strong>Graphics:</strong> Understanding of the rendering pipeline and shader development (HLSL/GLSL).</li>"
                    "<li><strong>Optimization:</strong> Experience profiling and optimizing games for target platforms.</li>"
                    "<li><strong>Passion:</strong> A deep love for video games and game development.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Gameplay:</strong> Implement core game loops, player controls, and AI behaviors.</li>"
                    "<li><strong>Systems:</strong> Architect scalable systems for inventory, quests, and dialogue.</li>"
                    "<li><strong>Tools:</strong> Build custom editor tools to improve the workflow for artists and designers.</li>"
                    "<li><strong>Debugging:</strong> Troubleshoot and fix complex gameplay bugs and crashes.</li>"
                    "<li><strong>Polish:</strong> Collaborate with artists to add juice and polish to the game feel.</li>"
                    "</ul>"
                ),
                "location": "Los Angeles, CA",
                "salary": 125000,
                "job_type": "FULL_TIME",
                "work_mode": "ONSITE",
            },
            {
                "title": "Part-Time Tech Consultant",
                "company": "ConsultPro",
                "desc": (
                    "<p>ConsultPro connects experienced tech professionals with businesses that need expert advice. We are looking for part-time consultants to join our network.</p>"
                    "<p>You will work on short-term engagements, helping clients solve specific technical problems or make strategic decisions. This is a great way to monetize your expertise and expand your professional network.</p>"
                    "<p>We handle the sales and billing so you can focus on delivering value.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Experience:</strong> 10+ years of industry experience in software engineering or IT.</li>"
                    "<li><strong>Expertise:</strong> Deep expertise in a specific domain (e.g., Cloud, Security, AI, Legacy Modernization).</li>"
                    "<li><strong>Communication:</strong> Ability to explain complex technical concepts to business leaders.</li>"
                    "<li><strong>Flexibility:</strong> Ability to work flexible hours to accommodate client schedules.</li>"
                    "<li><strong>Professionalism:</strong> High standard of professionalism and integrity.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Assessment:</strong> Assess client technology stacks and identify areas for improvement.</li>"
                    "<li><strong>Strategy:</strong> Develop technology strategies aligned with business goals.</li>"
                    "<li><strong>Mentorship:</strong> Mentor client teams and help them adopt best practices.</li>"
                    "<li><strong>Reports:</strong> deliver written reports and presentations summarizing your findings.</li>"
                    "<li><strong>Guidance:</strong> Provide ongoing guidance during the implementation of your recommendations.</li>"
                    "</ul>"
                ),
                "location": "Remote",
                "salary": 100000,
                "job_type": "PART_TIME",
                "work_mode": "REMOTE",
            },
            {
                "title": "Contract Developer",
                "company": "FreelanceHub",
                "desc": (
                    "<p>FreelanceHub is a platform for vetted freelance developers. We are seeing a high demand for contract developers to augment our clients' teams.</p>"
                    "<p>You will work on projects ranging from 3 to 12 months, with the possibility of extension. We have clients in various industries, from fintech to healthcare.</p>"
                    "<p>You set your own rates and choose the projects that interest you. We take care of the paperwork.</p>"
                ),
                "requirements": (
                    "<ul>"
                    "<li><strong>Skills:</strong> Full-stack development skills (React, Node, Python, Java, etc.).</li>"
                    "<li><strong>Autonomy:</strong> Ability to hit the ground running and work independently.</li>"
                    "<li><strong>Communication:</strong> Proactive communication and reliability.</li>"
                    "<li><strong>Remote:</strong> Experience working effectively in distributed teams.</li>"
                    "<li><strong>Portfolio:</strong> A track record of successful project delivery.</li>"
                    "</ul>"
                ),
                "responsibilities": (
                    "<ul>"
                    "<li><strong>Delivery:</strong> Deliver high-quality code on time and within budget.</li>"
                    "<li><strong>Collaboration:</strong> Integrate seamlessly with client engineering teams.</li>"
                    "<li><strong>Agile:</strong> Participate in daily standups and sprint planning sessions.</li>"
                    "<li><strong>Handover:</strong> Ensure proper handover and documentation at the end of the contract.</li>"
                    "<li><strong>Problem Solving:</strong> Proactively identify and solve technical blockers.</li>"
                    "</ul>"
                ),
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
                "desc": (
                    "<p>The biggest React conference of the year returns in 2026, bringing together thousands of frontend engineers from around the globe. This year, our focus is on 'The New Frontier of Frontend', exploring the massive seismic shifts in the ecosystem brought about by React 19, RSC, and the integration of AI-driven developer tools.</p>"
                    "<p>Attendees will have the opportunity to learn directly from the core React team and industry leaders who are pushing the boundaries of what's possible on the web. Whether you're interested in performance optimization, advanced state management, or the latest in UI/UX design, React Summit 2026 has something for you.</p>"
                    "<p>With three tracks of technical talks, full-day deep-dive workshops, and legendary after-parties, this is more than just a conference—it's a celebration of the vibrant and innovative React community. Don't miss your chance to be part of the future of the web.</p>"
                ),
                "location": "Amsterdam, Netherlands",
                "agenda": (
                    "<ul>"
                    "<li><strong>09:00 AM - 10:00 AM:</strong> Opening Keynote: The Future of React 19 and Beyond</li>"
                    "<li><strong>10:15 AM - 11:30 AM:</strong> Mastering React Server Components for High-Performance Enterprise Apps</li>"
                    "<li><strong>11:30 AM - 12:30 PM:</strong> Lunch Break & Networking in the Expo Hall</li>"
                    "<li><strong>12:45 PM - 02:00 PM:</strong> Track A: Next-Gen State Management | Track B: Accessible UI Components</li>"
                    "<li><strong>02:15 PM - 03:30 PM:</strong> Panel Discussion: Is the 'Frontend Developer' Role Evolving into 'Product Engineer'?</li>"
                    "<li><strong>03:45 PM - 05:00 PM:</strong> Technical Deep Dive: Optimizing Web Vitals with React Compiler</li>"
                    "<li><strong>05:30 PM onwards:</strong> Cocktail Mixer and Community Lightning Talks</li>"
                    ""
                    "</ul>"
                ),
                "ticket_url": "https://reactsummit.com",
            },
            {
                "title": "PyCon 2026",
                "desc": (
                    "<p>PyCon US 2026 is the premier annual gathering for the global community using and developing the open-source Python programming language. As Python continues to dominate the fields of Data Science, AI, and Backend Web Development, this year's conference is slated to be our largest and most impactful yet.</p>"
                    "<p>Our mission is to foster a diverse and inclusive community by providing a platform for developers of all skill levels to share their knowledge and passion. The 2026 program features over 100 talks, tutorials, and poster sessions covering everything from beginner basics to the most advanced 'under the hood' internals of the Python interpreter.</p>"
                    "<p>Beyond the technical sessions, PyCon is famous for its 'Hallway Track'—the spontaneous conversations and connections that happen between sessions. Join us in Pittsburgh for a week of learning, sprinting, and contributing to the language that powers the world.</p>"
                ),
                "location": "Pittsburgh, PA",
                "agenda": (
                    "<ul>"
                    "<li><strong>Day 1 & 2:</strong> Intensive Tutorials on AsyncIO, Django 6.0, and Scalable Data Pipelines</li>"
                    "<li><strong>Day 3:</strong> Main Stage Keynotes and Python Software Foundation Excellence Awards</li>"
                    "<li><strong>Day 4:</strong> Specialized Tracks: AI & Machine Learning, Web Frameworks, and DevOps</li>"
                    "<li><strong>Day 5:</strong> The Job Fair and Professional Networking Brunch</li>"
                    "<li><strong>Post-Conf:</strong> Community Development Sprints (Open to all contributors)</li>"
                    "</ul>"
                ),
                "ticket_url": "https://pycon.org",
            },
            {
                "title": "AWS re:Invent 2026",
                "desc": (
                    "<p>AWS re:Invent is the definitive learning conference for the global cloud computing community. Held annually in Las Vegas, this event is where Amazon Web Services unveils its most significant innovations and announcements for the coming year.</p>"
                    "<p>With over 2,000 technical sessions, multiple keynotes from AWS leadership, and hands-on labs hosted by AWS experts, re:Invent is designed to give you the skills and inspiration to transform your business and career in the cloud.</p>"
                    "<p>This year, we're putting a massive spotlight on Generative AI, Sustainability in the Cloud, and the next generation of Serverless computing. Whether you're a developer, architect, or IT decision-maker, re:Invent is the one event you can't afford to miss if you want to stay ahead of the curve.</p>"
                ),
                "location": "Las Vegas, NV",
                "agenda": (
                    "<ul>"
                    "<li><strong>Monday:</strong> Midnight Madness - Kickoff Party and First Announcements</li>"
                    "<li><strong>Tuesday:</strong> CEO Keynote: The Vision for the Global Cloud in 2026</li>"
                    "<li><strong>Wednesday:</strong> Technical Tracks: Advanced Serverless Design & AI Model Fine-tuning</li>"
                    "<li><strong>Thursday:</strong> CTO Keynote: Architecting for Resiliency at Scale</li>"
                    "<li><strong>Friday:</strong> Certification Day and Career Development Workshops</li>"
                    "</ul>"
                ),
                "ticket_url": "https://reinvent.awsevents.com",
            },
            {
                "title": "DevOps Days",
                "desc": (
                    "<p>DevOpsDays is a worldwide series of technical conferences covering topics of software development, IT infrastructure operations, and the intersection between them. Each event is run by volunteers from the local area, and this year's San Francisco edition promises to be the biggest yet.</p>"
                    "<p>The conference features a unique blend of curated talks and self-organized 'Open Space' content. This format allows attendees to drive the agenda, discussing real-world challenges and solutions that matter most to them. Expect deep dives into culture, automation, measurement, and sharing.</p>"
                    "<p>Whether you're a developer, sysadmin, or manager, DevOpsDays offers a friendly and inclusive environment to learn, network, and improve your craft. Come help us bridge the gap between silos!</p>"
                ),
                "location": "San Francisco, CA",
                "agenda": (
                    "<ul>"
                    "<li><strong>Day 1: Platform Engineering</strong> - Keynotes on building internal developer platforms (IDPs).</li>"
                    "<li><strong>Day 1 Afternoon:</strong> Open Spaces - Proposed topics include 'Terraform vs Pulumi' and 'Incidents as Learning Opportunities'.</li>"
                    "<li><strong>Day 2: Culture & Humans</strong> - Talks on psychological safety, burnout, and effective leadership.</li>"
                    "<li><strong>Day 2 Afternoon:</strong> Workshops - Hands-on sessions with ArgoCD, Prometheus, and Kubernetes.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://devopsdays.org",
            },
            {
                "title": "KubeCon 2026",
                "desc": (
                    "<p>The Cloud Native Computing Foundation's flagship conference gathers leading technologists from open source and cloud native communities in Paris, France. KubeCon + CloudNativeCon brings together thousands of attendees to further the education and advancement of cloud native computing.</p>"
                    "<p>This four-day immersive event will showcase the latest advancements in Kubernetes, Prometheus, Envoy, and other CNCF-hosted projects. Maintainers and end-users alike will share insights on deploying and managing scale-out applications in production.</p>"
                    "<p>Join us to explore the future of infrastructure, from edge computing and service meshes to GitOps and observability. It's the ultimate destination for anyone building the cloud native web.</p>"
                ),
                "location": "Paris, France",
                "agenda": (
                    "<ul>"
                    "<li><strong>Keynotes:</strong> Updates from the CNCF TOC and visionary talks from industry leaders.</li>"
                    "<li><strong>Maintainer Track:</strong> Deep dives into the internals of Kubernetes scheduler, networking, and storage.</li>"
                    "<li><strong>End User Track:</strong> Case studies from global enterprises like Spotify, CERN, and Bloomberg.</li>"
                    "<li><strong>Solutions Showcase:</strong> Connect with vendors providing the latest tooling and services for the ecosystem.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://kubecon.io",
            },
            {
                "title": "ML Conference",
                "desc": (
                    "<p>The Machine Learning Conference (MLconf) is dedicated to the specific challenges of gathering, organizing, and analyzing big data. We bring together Machine Learning professionals and researchers to share their latest findings and techniques.</p>"
                    "<p>This year in Berlin, the focus will be on 'Responsible AI' and 'ML Ops'. We will explore how to build models that are not only accurate but also fair, explainable, and robust. We will also cover the engineering aspects of deploying and maintaining ML systems at scale.</p>"
                    "<p>Expect a single-track day filled with high-density talks, no sales pitches, and plenty of opportunities to network with the brightest minds in the field.</p>"
                ),
                "location": "Berlin, Germany",
                "agenda": (
                    "<ul>"
                    "<li><strong>09:00 AM:</strong> The State of Deep Learning in 2026.</li>"
                    "<li><strong>10:30 AM:</strong> Bias and Fairness in Large Language Models.</li>"
                    "<li><strong>01:00 PM:</strong> Graph Neural Networks for Recommendation Systems.</li>"
                    "<li><strong>02:30 PM:</strong> Panel: The Future of AI Regulation in the EU.</li>"
                    "<li><strong>04:00 PM:</strong> Poster Sessions and Research Showcase.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://mlconf.com",
            },
            {
                "title": "Tech Career Fair",
                "desc": (
                    "<p>Are you ready to take the next step in your career? The NY Tech Career Fair connects talented developers, designers, and data scientists with the city's top technology companies. From fast-growing startups to established Fortune 500 giants, everyone is hiring.</p>"
                    "<p>This is not your average job fair. We offer resume reviews, mock interviews, and career coaching sessions throughout the day. Bring your laptop and your portfolio—some companies will be conducting on-the-spot coding challenges and interviews.</p>"
                    "<p>Whether you're looking for your first internship or a VP of Engineering role, this is the most efficient way to get face-to-face with hiring managers.</p>"
                ),
                "location": "New York, NY",
                "agenda": (
                    "<ul>"
                    "<li><strong>10:00 AM:</strong> Doors Open & Registration.</li>"
                    "<li><strong>11:00 AM:</strong> Workshop: 'Negotiating Your Salary in 2026'.</li>"
                    "<li><strong>01:00 PM:</strong> Lighting Talks from Platinum Sponsors.</li>"
                    "<li><strong>02:00 PM:</strong> Speed Networking Sessions.</li>"
                    "<li><strong>04:00 PM:</strong> Keynote: 'Navigating the Tech Job Market'.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://techcareer.com",
            },
            {
                "title": "Frontend Masters Live",
                "desc": (
                    "<p>Join us online for an exclusive live workshop series presented by Frontend Masters. This two-day event focuses on advanced JavaScript patterns and modern browser APIs. It's an interactive learning experience where you can code along with the instructors in real-time.</p>"
                    "<p>We have gathered some of the most respected teachers in the industry to demystify complex topics like the Event Loop, Service Workers, and WebAssembly. You will leave with a deep understanding of how the web platform truly works.</p>"
                    "<p>All sessions will be recorded and available for replay. Ticket holders also get a free month of access to the entire Frontend Masters library.</p>"
                ),
                "location": "Online",
                "agenda": (
                    "<ul>"
                    "<li><strong>Session 1:</strong> Deep JavaScript Foundations v4.</li>"
                    "<li><strong>Session 2:</strong> Hardware Access with Web Bluetooth and WebUSB.</li>"
                    "<li><strong>Session 3:</strong> Building Progressive Web Apps (PWAs) from Scratch.</li>"
                    "<li><strong>Session 4:</strong> Q&A with the Instructors.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://frontendmasters.com/live",
            },
            {
                "title": "Security BSides",
                "desc": (
                    "<p>BSides Seattle is a community-driven framework for building events for and by information security community members. The goal is to expand the spectrum of conversation beyond the traditional confines of space and time.</p>"
                    "<p>This is an event where you can learn about the latest exploits, defense mechanisms, and privacy issues in an informal and collaborative atmosphere. We encourage new speakers and experimental topics that might not fit into mainstream conferences.</p>"
                    "<p>Don't miss the famous Capture The Flag (CTF) competition, lockpicking village, and the wireless hacking sandbox!</p>"
                ),
                "location": "Seattle, WA",
                "agenda": (
                    "<ul>"
                    "<li><strong>Track 1:</strong> Defensive Ops & Blue Teaming.</li>"
                    "<li><strong>Track 2:</strong> Offensive Security & Red Teaming.</li>"
                    "<li><strong>Workshops:</strong> Malware Analysis and Reverse Engineering.</li>"
                    "<li><strong>Village:</strong> Hardware Hacking and IoT Security.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://bsides.org",
            },
            {
                "title": "Data Science Summit",
                "desc": (
                    "<p>The Boston Data Science Summit is the premier event for data practitioners in the Northeast. We focus on the practical application of data science in industries such as Biotech, Finance, and Robotics.</p>"
                    "<p>Hear from Chief Data Officers and Lead Data Scientists about how they are structuring their teams, managing data governance, and driving ROI from their AI investments. This is a strategic conference for leaders and individual contributors alike.</p>"
                    "<p>Topics include Causal Inference, Time Series Analysis, and the latest in Natural Language Processing (NLP).</p>"
                ),
                "location": "Boston, MA",
                "agenda": (
                    "<ul>"
                    "<li><strong>Morning:</strong> Executive Panels on AI Strategy.</li>"
                    "<li><strong>Lunch:</strong> Roundtable Discussions by Industry.</li>"
                    "<li><strong>Afternoon:</strong> Technical Deep Dives into MLOps and Data Engineering.</li>"
                    "<li><strong>Closing:</strong> The Future of Data Science in Healthcare.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://datasummit.com",
            },
            {
                "title": "Mobile Dev Meetup",
                "desc": (
                    "<p>Join local mobile developers for an evening of networking and tech talks. We are a community of iOS, Android, and cross-platform developers who meet monthly to share knowledge and pizza.</p>"
                    "<p>This month's theme is 'Mobile DevOps'. We will discuss CI/CD pipelines, automated testing on device farms, and over-the-air updates. Whether you are an indie dev or working at a large enterprise, there is something for you to learn.</p>"
                    "<p>Thanks to our sponsors, food and drinks will be provided!</p>"
                ),
                "location": "Austin, TX",
                "agenda": (
                    "<ul>"
                    "<li><strong>6:00 PM:</strong> Doors Open & Networking.</li>"
                    "<li><strong>6:30 PM:</strong> Talk 1: 'Fastlane from Zero to Hero'.</li>"
                    "<li><strong>7:15 PM:</strong> Break & Pizza.</li>"
                    "<li><strong>7:30 PM:</strong> Talk 2: 'Distributing Beta Builds with Firebase'.</li>"
                    "<li><strong>8:15 PM:</strong> Lightning Talks (Sign up at the door).</li>"
                    "</ul>"
                ),
                "ticket_url": "https://meetup.com/mobile-dev",
            },
            {
                "title": "Blockchain Expo",
                "desc": (
                    "<p>Blockchain Expo North America will explore the latest innovations within the Blockchain ecosystem. This conference covers key industries including Manufacturing, Transport, Health, Logistics, Government, Energy, and more.</p>"
                    "<p>This is not just for crypto traders. We focus on enterprise blockchain applications, digital identity, provenance, and smart contracts. Come see real-world use cases of blockchain technology solving business problems.</p>"
                    "<p>The event is co-located with the IoT Tech Expo, AI & Big Data Expo, and Cyber Security & Cloud Expo, so you can explore the convergence of these technologies.</p>"
                ),
                "location": "Miami, FL",
                "agenda": (
                    "<ul>"
                    "<li><strong>Day 1:</strong> Crypto & Digital Asset Strategy.</li>"
                    "<li><strong>Day 2 Morning:</strong> Blockchain for Enterprise (Supply Chain & Identity).</li>"
                    "<li><strong>Day 2 Afternoon:</strong> Tokenization & Digital Assets.</li>"
                    "<li><strong>Day 2 Evening:</strong> Networking Party at South Beach.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://blockchainexpo.com",
            },
            {
                "title": "Docker Workshop",
                "desc": (
                    "<p>Kickstart your journey into containerization with this hands-on Docker workshop. In just 4 hours, you will go from installing Docker to deploying a multi-container application.</p>"
                    "<p>This workshop is designed for developers and sysadmins who have heard about Docker but haven't had the chance to dive in. We will cover images, containers, volumes, networks, and Docker Compose.</p>"
                    "<p>Prerequisites: Basic familiarity with the command line.</p>"
                ),
                "location": "Online",
                "agenda": (
                    "<ul>"
                    "<li><strong>Module 1:</strong> Containers vs Virtual Machines.</li>"
                    "<li><strong>Module 2:</strong> Running and Managing Containers.</li>"
                    "<li><strong>Module 3:</strong> Building Custom Images with Dockerfiles.</li>"
                    "<li><strong>Module 4:</strong> Orchestration with Docker Compose.</li>"
                    "<li><strong>Q&A:</strong> Ask the experts anything about containers.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://docker.com/workshop",
            },
            {
                "title": "GraphQL Summit",
                "desc": (
                    "<p>GraphQL Summit is the world's largest conference dedicated to GraphQL. Join us in San Francisco to hear from the creators of GraphQL and the engineers who have implemented it at scale at companies like Facebook, Netflix, and Airbnb.</p>"
                    "<p>We will cover the entire GraphQL lifecycle: schema design, resolver implementation, client-side caching, and federation. You will learn best practices for security, performance, and governence.</p>"
                    "<p>Don't just build APIs—build a data graph that empowers your product teams.</p>"
                ),
                "location": "San Francisco, CA",
                "agenda": (
                    "<ul>"
                    "<li><strong>Keynote:</strong> The State of GraphQL in 2026.</li>"
                    "<li><strong>Track 1:</strong> GraphQL Federation & Microservices.</li>"
                    "<li><strong>Track 2:</strong> GraphQL Clients (Apollo, Relay, Urql).</li>"
                    "<li><strong>Track 3:</strong> GraphQL Security & Authorization.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://graphqlsummit.com",
            },
            {
                "title": "UX Design Conference",
                "desc": (
                    "<p>The UX Design Conference gathers the world's leading designers to share their insights on creating human-centered products. We look beyond the pixels to understand the psychology and strategy behind great design.</p>"
                    "<p>Topics this year include inclusive design, design ethics, and the role of AI in the creative process. You will walk away with practical tools and frameworks you can apply to your own work immediately.</p>"
                    "<p>Get inspired by case studies from award-winning design teams.</p>"
                ),
                "location": "Los Angeles, CA",
                "agenda": (
                    "<ul>"
                    "<li><strong>Talks:</strong> 'Design is Storytelling', 'Accessibility First', 'Designing for Trust'.</li>"
                    "<li><strong>Workshops:</strong> Rapid Prototyping, User Research Methods, Design Systems.</li>"
                    "<li><strong>Portfolio Reviews:</strong> Get feedback on your work from senior designers.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://uxconf.com",
            },
            {
                "title": "Agile Alliance Conference",
                "desc": (
                    "<p>Agile2026 is the premier conference for Agile practitioners. It's a place to explore the latest ideas and practices in Agile software development. We welcome everyone from Scrum Masters and Product Owners to executives and developers.</p>"
                    "<p>Our program covers the full spectrum of Agile: Scrum, Kanban, XP, SAFe, and LeSS. We also delve into the cultural and organizational changes needed to make Agile work at scale.</p>"
                    "<p>Come recharge your Agile batteries and connect with the community.</p>"
                ),
                "location": "Chicago, IL",
                "agenda": (
                    "<ul>"
                    "<li><strong>Monday:</strong> Executive Summit (Invitation Only).</li>"
                    "<li><strong>Tuesday-Thursday:</strong> Main Conference Sessions (100+ talks).</li>"
                    "<li><strong>Friday:</strong> Open Space & Closing Keynote.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://agilealliance.org",
            },
            {
                "title": "Tech Networking Event",
                "desc": (
                    "<p>Expand your professional network at our monthly Tech Networking Event. We bring together a diverse mix of founders, investors, engineers, and designers in a casual setting.</p>"
                    "<p>There are no speakers and no agenda—just good conversation and great connections. Whether you are looking for a co-founder, a new job, or just some advice, you will find it here.</p>"
                    "<p>Venue: The Rooftop at TechHub NY. Complimentary drinks and hors d'oeuvres served until 8 PM.</p>"
                ),
                "location": "New York, NY",
                "agenda": (
                    "<ul>"
                    "<li><strong>6:00 PM:</strong> Check-in and Nametags.</li>"
                    "<li><strong>6:30 PM:</strong> Icebreaker Bingo (Optional).</li>"
                    "<li><strong>7:00 PM:</strong> Facilitated Introductions by Industry.</li>"
                    "<li><strong>9:00 PM:</strong> Event Ends.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://technetwork.com",
            },
            {
                "title": "API Days",
                "desc": (
                    "<p>API Days London is part of the world's leading API conference series. We explore how APIs are programmable assets that allow businesses to innovate faster and create new revenue streams.</p>"
                    "<p>This year's theme is 'The API Economy'. We will discuss API monetization, developer experience (DX), and the rise of API-first companies.</p>"
                    "<p>Join 1,000+ API practitioners for two days of insights and networking.</p>"
                ),
                "location": "London, UK",
                "agenda": (
                    "<ul>"
                    "<li><strong>Business Track:</strong> API Strategy, Monetization, Governance.</li>"
                    "<li><strong>Technical Track:</strong> OpenAPI, gRPC, AsyncAPI, Security.</li>"
                    "<li><strong>Workshop:</strong> Designing Great DX.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://apidays.io",
            },
            {
                "title": "Women in Tech Summit",
                "desc": (
                    "<p>The Women in Tech Summit works to inspire, educate, and connect women in the technology industry. Our goal is to support women at every stage of their careers, from students to C-level executives.</p>"
                    "<p>The event features inspirational keynotes, technical workshops, and career development sessions. We also have a mentorship zone where you can get one-on-one advice from industry veterans.</p>"
                    "<p>Everyone is welcome to attend and support our mission of diversity and inclusion.</p>"
                ),
                "location": "San Francisco, CA",
                "agenda": (
                    "<ul>"
                    "<li><strong>Morning:</strong> Keynotes from Women Leaders in Tech.</li>"
                    "<li><strong>Mid-Day:</strong> Coding Workshops (Python, JS) & Soft Skills Training (Negotiation, Public Speaking).</li>"
                    "<li><strong>Afternoon:</strong> Panel: Breaking the Glass Ceiling.</li>"
                    "<li><strong>Evening:</strong> Networking Reception.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://womenintechsummit.com",
            },
            {
                "title": "Startup Grind Global",
                "desc": (
                    "<p>Startup Grind Global Conference is the event for startups. We bring together thousands of founders, investors, and innovators for two days of non-stop content and connection.</p>"
                    "<p>Learn from the founders of unicorns like Airbnb, Stripe, and Slack. Pitch your startup to top VCs. Find your next co-founder or key hire.</p>"
                    "<p>If you are building a company, you need to be here.</p>"
                ),
                "location": "Silicon Valley, CA",
                "agenda": (
                    "<ul>"
                    "<li><strong>Main Stage:</strong> Fireside chats with legendary founders.</li>"
                    "<li><strong>VC Stage:</strong> 'Reverse Pitches' - VCs pitch to founders.</li>"
                    "<li><strong>Growth Stage:</strong> Tactics for scaling sales, marketing, and product.</li>"
                    "<li><strong>Exhibition:</strong> Startup Showcase (100+ startups).</li>"
                    "</ul>"
                ),
                "ticket_url": "https://startupgrind.com",
            },
            {
                "title": "Code Review Workshop",
                "desc": (
                    "<p>Code review is one of the most effective ways to improve code quality and share knowledge, but few teams do it well. This workshop teaches the art and science of constructive code review.</p>"
                    "<p>You will learn what to look for (and what to ignore), how to give feedback that is actionable and kind, and how to handle disagreements.</p>"
                    "<p>We will practice reviewing real pull requests in various languages.</p>"
                ),
                "location": "Online",
                "agenda": (
                    "<ul>"
                    "<li><strong>Part 1:</strong> The Psychology of Code Review.</li>"
                    "<li><strong>Part 2:</strong> Checklist: Security, Performance, Readability.</li>"
                    "<li><strong>Part 3:</strong> Tools and Automation (Linters, CI).</li>"
                    "<li><strong>Part 4:</strong> Role-playing Review Scenarios.</li>"
                    "</ul>"
                ),
                "ticket_url": "https://codereview.workshop",
            },
            {
                "title": "Tech Talks Tuesday",
                "desc": (
                    "<p>Tech Talks Tuesday is a weekly series hosted by the Seattle Tech Hub. Each week, we invite a speaker to give a deep-dive talk on a specific technology or engineering problem.</p>"
                    "<p>It's a great way to keep up with industry trends without committing to a full conference. The talks are technical, practical, and devoid of marketing fluff.</p>"
                    "<p>Open to the public. Live stream available for remote attendees.</p>"
                ),
                "location": "Seattle, WA",
                "agenda": (
                    "<ul>"
                    "<li><strong>7:00 PM:</strong> Announcements.</li>"
                    "<li><strong>7:05 PM:</strong> Main Presentation (45 mins).</li>"
                    "<li><strong>7:50 PM:</strong> Q&A (15 mins).</li>"
                    "<li><strong>8:05 PM:</strong> Socializing.</li>"
                    "</ul>"
                ),
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
                "body": (
                    "<h3>Professional Web Development Mastery</h3>"
                    "<p>GitHub Learning Lab is an educational platform offering interactive, project-based courses to improve your skills in software development, version control, and open-source collaboration. This curriculum is designed to take you from a curious beginner to a job-ready full stack engineer.</p>"
                    "<h4>Popular Courses</h4>"
                    "<ul>"
                    "<li><strong>Introduction to Git and GitHub:</strong> Master the essentials of version control and collaboration on the world's leading platform.</li>"
                    "<li><strong>Building RESTful APIs:</strong> Learn to design and implement robust, scalable backends using Node.js and Express.</li>"
                    "<li><strong>Full-Stack React Patterns:</strong> Dive deep into modern React, including custom hooks, context API, and performance optimization.</li>"
                    "<li><strong>Cloud Deployment 101:</strong> Understand how to ship your code to the world using Vercel, Netlify, and AWS.</li>"
                    "</ul>"
                    "<h4>Why Learn Here?</h4>"
                    "<ul>"
                    "<li><strong>Hands-on Exercises:</strong> Work with real-world applications and solve practical coding challenges.</li>"
                    "<li><strong>Earn Certificates:</strong> Receive industry-recognized certificates of completion to showcase on your LinkedIn profile.</li>"
                    "<li><strong>Supportive Community:</strong> Access a curated community of learners and mentors who are always ready to help.</li>"
                    "</ul>"
                    "<h4>How to Access</h4>"
                    "<p>Ready to start your journey? Click the link below to enroll in your first course today!</p>"
                ),
                "url": "https://udemy.com/web-dev-course",
            },
            {
                "name": "Python for Data Science Handbook",
                "body": (
                    "<h3>Unlock the Power of Data with Python</h3>"
                    "<p>Data is the new oil, and Python is the ultimate tool for refining it. This resource provides a deep dive into the libraries and techniques that make Python the #1 language for data scientists and analysts worldwide.</p>"
                    "<h4>Key Learning Objectives</h4>"
                    "<ul>"
                    "<li><strong>Data Manipulation:</strong> Master the 'Pandas' library to clean, transform, and analyze complex datasets with ease.</li>"
                    "<li><strong>Statistical Analysis:</strong> Learn to perform rigorous statistical tests and build predictive models using SciPy and Statsmodels.</li>"
                    "<li><strong>Visual Storytelling:</strong> Create breathtaking data visualizations with Matplotlib, Seaborn, and Plotly to drive business insights.</li>"
                    "<li><strong>Machine Learning Fundamentals:</strong> Get hands-on with Scikit-Learn to implement regression, classification, and clustering algorithms.</li>"
                    "</ul>"
                    "<h4>Essential Features</h4>"
                    "<ul>"
                    "<li><strong>Jupyter Notebooks:</strong> Includes dozens of interactive notebooks for a true 'code-along' learning experience.</li>"
                    "<li><strong>Real-World Datasets:</strong> Practice on actual data from finance, healthcare, and social media ecosystems.</li>"
                    "<li><strong>Scalability Best Practices:</strong> Understand how to optimize your code for large-scale data processing inproduction.</li>"
                    "</ul>"
                ),
                "url": "https://jakevdp.github.io/PythonDataScienceHandbook",
            },
            {
                "name": "React Documentation",
                "body": (
                    "<h3>The Definitive Guide to React</h3>"
                    "<p>The new React documentation is a masterpiece of technical writing. It doesn't just explain the 'how', but also the 'why'. Whether you are learning about components, hooks, or the new server-side paradigms, this is your primary source of truth.</p>"
                    "<h4>What You Will Learn</h4>"
                    "<ul>"
                    "<li><strong>Thinking in React:</strong> Understand the mental model of building user interfaces with components and state.</li>"
                    "<li><strong>Describing the UI:</strong> Learn how to use JSX to write markup and logic together.</li>"
                    "<li><strong>Managing State:</strong> Master useState, useReducer, and Context to handle complex data flows.</li>"
                    "<li><strong>Escape Hatches:</strong> Know when and how to use refs and effects to interface with external systems.</li>"
                    "</ul>"
                    "<h4>Interactive Examples</h4>"
                    "<p>The docs feature hundreds of interactive sandboxes where you can edit logic and CSS live in the browser. It's the best way to develop intuition for the framework.</p>"
                ),
                "url": "https://react.dev",
            },
            {
                "name": "MDN Web Docs",
                "body": (
                    "<h3>Resources for Developers, by Developers</h3>"
                    "<p>MDN Web Docs (formerly Mozilla Developer Network) is the single most comprehensive resource for web documentation. From the basics of HTML to the complexities of WebAssembly and modern CSS APIs, MDN covers it all.</p>"
                    "<h4>Core Technologies</h4>"
                    "<ul>"
                    "<li><strong>HTML:</strong> The structural foundation of the web, detailed in every element and attribute.</li>"
                    "<li><strong>CSS:</strong> Extensive guides on layout (Flexbox, Grid), animations, typography, and responsive design.</li>"
                    "<li><strong>JavaScript:</strong> Complete reference for the language, including the DOM API and newer features like Async/Await.</li>"
                    "<li><strong>Web APIs:</strong> Documentation for Geolocation, Notifications, Canvas, and hundreds of other browser interfaces.</li>"
                    "</ul>"
                    "<h4>Browser Compatibility</h4>"
                    "<p>Every article includes detailed compatibility tables, so you know exactly which features are safe to use in production across Chrome, Firefox, Safari, and Edge.</p>"
                ),
                "url": "https://developer.mozilla.org",
            },
            {
                "name": "freeCodeCamp",
                "body": (
                    "<h3>Learn to Code for Free</h3>"
                    "<p>freeCodeCamp is a global community of millions of people learning to code together. They offer a completely free, self-paced curriculum that covers the full stack of web development technologies.</p>"
                    "<h4>Curriculum Highlights</h4>"
                    "<ul>"
                    "<li><strong>Responsive Web Design:</strong> HTML5, CSS3, and Accessibility.</li>"
                    "<li><strong>JavaScript Algorithms:</strong> Data structures, functional programming, and algorithmic thinking.</li>"
                    "<li><strong>Front End Development Libraries:</strong> Bootstrap, jQuery, SASS, React, and Redux.</li>"
                    "<li><strong>Data Visualization:</strong> Building charts and graphs with D3.js.</li>"
                    "<li><strong>Back End Development:</strong> APIs and Microservices with Node.js and Express.</li>"
                    "</ul>"
                    "<h4>Certifications</h4>"
                    "<p>Upon completing each 300-hour section, you earn a verified certification. Millions of alumni have used these to land jobs at companies like Google, Microsoft, and Amazon.</p>"
                ),
                "url": "https://freecodecamp.org",
            },
            {
                "name": "AWS Training",
                "body": (
                    "<h3>Build Your Future in the Cloud</h3>"
                    "<p>Official training from the source. AWS Training and Certification offers free digital courses, classroom training, and certifications to help you build your cloud skills and advance your career.</p>"
                    "<h4>Learning Paths</h4>"
                    "<ul>"
                    "<li><strong>Cloud Practitioner:</strong> For individuals who want a high-level understanding of AWS Cloud concepts.</li>"
                    "<li><strong>Solutions Architect:</strong> For those who design available, cost-efficient, fault-tolerant, and scalable distributed systems.</li>"
                    "<li><strong>Developer:</strong> For those who write code and develop applications for the cloud.</li>"
                    "<li><strong>SysOps Administrator:</strong> For those who deploy, manage, and operate scalable, highly available, and fault-tolerant systems.</li>"
                    "</ul>"
                    "<h4>Skill Builder</h4>"
                    "<p>Access 500+ free digital courses, learning plans, and interactive labs. Whether you are a beginner or a pro, there is something here for you.</p>"
                ),
                "url": "https://aws.training",
            },
            {
                "name": "The Odin Project",
                "body": (
                    "<h3>Your Career in Web Development Starts Here</h3>"
                    "<p>The Odin Project is one of the most highly regarded free bootcamps on the internet. It provides a full-stack curriculum that is open source and community-driven, focusing on real-world skills and projects.</p>"
                    "<h4>Pathways</h4>"
                    "<ul>"
                    "<li><strong>Foundations:</strong> Learn the basics of how the web works, Git, HTML, CSS, and JavaScript.</li>"
                    "<li><strong>Full Stack Ruby on Rails:</strong> Master Ruby, the Rails framework, SQL databases, and advanced frontend.</li>"
                    "<li><strong>Full Stack JavaScript:</strong> Deep dive into Node.js, Express, MongoDB, and React.</li>"
                    "</ul>"
                    "<h4>Project-Based</h4>"
                    "<p>You won't just watch videos. You will build dozens of portfolio-worthy projects, from a simple calculator to a full social media clone. This hands-on approach ensures you actually learn by doing.</p>"
                ),
                "url": "https://theodinproject.com",
            },
            {
                "name": "LeetCode",
                "body": (
                    "<h3>The World's Leading Online Programming Platform</h3>"
                    "<p>LeetCode is the gold standard for technical interview preparation. It supports over 14 popular programming languages and offers thousands of coding challenges categorized by difficulty and topic.</p>"
                    "<h4>Key Features</h4>"
                    "<ul>"
                    "<li><strong>Question Bank:</strong> Over 2,500 questions covering Arrays, Trees, Graphs, Dynamic Programming, and System Design.</li>"
                    "<li><strong>Contests:</strong> Weekly and bi-weekly global coding contests to test your speed and accuracy against the community.</li>"
                    "<li><strong>Discussion:</strong> A vibrant community where users share optimal solutions and explain their thought processes.</li>"
                    "<li><strong>Company Tags:</strong> See which companies are asking which questions right now (Premium feature).</li>"
                    "</ul>"
                    "<h4>Interview Crash Course</h4>"
                    "<p>Structured learning paths designed to get you interview-ready in weeks, not months. Master the patterns behind the problems.</p>"
                ),
                "url": "https://leetcode.com",
            },
            {
                "name": "HackerRank",
                "body": (
                    "<h3>Match Your Skills to the Right Job</h3>"
                    "<p>HackerRank is a technology hiring platform that is the standard for assessing developer skills for over 2,000 companies around the world. For developers, it is a place to practice coding and get noticed.</p>"
                    "<h4>Practice Areas</h4>"
                    "<ul>"
                    "<li><strong>Algorithms:</strong> Solve algorithmic challenges to sharpen your problem-solving skills.</li>"
                    "<li><strong>Data Structures:</strong> Master the fundamentals of storage and organization of data.</li>"
                    "<li><strong>Mathematics:</strong> Solve math problems using code (Number Theory, Combinatorics, Algebra).</li>"
                    "<li><strong>AI:</strong> Build bots to play games and solve puzzles using Artificial Intelligence.</li>"
                    "</ul>"
                    "<h4>Certification</h4>"
                    "<p>Take the HackerRank Skills Certification test—a standardized assessment to prove your proficiency in languages like Python, Java, and React. Add the certificate to your LinkedIn profile.</p>"
                ),
                "url": "https://hackerrank.com",
            },
            {
                "name": "Coursera Tech Courses",
                "body": (
                    "<h3>Learn Without Limits</h3>"
                    "<p>Coursera partners with more than 275 leading universities and companies to bring flexible, affordable, job-relevant online learning to individuals and organizations worldwide.</p>"
                    "<h4>Offerings</h4>"
                    "<ul>"
                    "<li><strong>Guided Projects:</strong> Learn a job-relevant skill in under 2 hours with step-by-step guidance.</li>"
                    "<li><strong>Courses:</strong> Deep dive into a subject with video lectures, readings, and quizzes.</li>"
                    "<li><strong>Specializations:</strong> Master a specific career skill through a series of rigorous courses.</li>"
                    "<li><strong>Professional Certificates:</strong> get job-ready for an in-demand career from Google, IBM, or Meta.</li>"
                    "</ul>"
                    "<h4>Academic Credit</h4>"
                    "<p>Many courses offer university credit that can be applied towards a full degree. It's the highest quality education available online.</p>"
                ),
                "url": "https://coursera.org",
            },
            {
                "name": "GitHub Learning Lab",
                "body": (
                    "<h3>Learn by Doing on GitHub</h3>"
                    "<p>GitHub Learning Lab takes you through realistic projects with a bot as your mentor. It operates directly within your GitHub repositories, giving you instant feedback as you push code and open pull requests.</p>"
                    "<h4>Popular Courses</h4>"
                    "<ul>"
                    "<li><strong>Introduction to GitHub:</strong> A fun and friendly intro to the world's most popular version control platform.</li>"
                    "<li><strong>Reviewing Pull Requests:</strong> Learn the etiquette and best practices for collaborative code review.</li>"
                    "<li><strong>Managing Merge Conflicts:</strong> A stress-free environment to practice solving gnarly merge conflicts.</li>"
                    "<li><strong>GitHub Actions:</strong> Automate your workflow with CI/CD right from your repo.</li>"
                    "</ul>"
                    "<h4>Why It Works</h4>"
                    "<p>You are learning in the actual environment you will use daily. No simulations—just real Git commands and real repositories.</p>"
                ),
                "url": "https://lab.github.com",
            },
            {
                "name": "Docker Getting Started",
                "body": (
                    "<h3>Your First Step into Containers</h3>"
                    "<p>The official Docker documentation provides one of the best getting-started guides in the industry. It walks you through the fundamental concepts of containerization without overwhelming you with jargon.</p>"
                    "<h4>What You Will Build</h4>"
                    "<ul>"
                    "<li><strong>Installation:</strong> Setting up Docker Desktop on Mac, Windows, or Linux.</li>"
                    "<li><strong>Running Containers:</strong> pulling images from Docker Hub and starting your first container.</li>"
                    "<li><strong>Building Images:</strong> Writing Dockerfiles to package your own applications.</li>"
                    "<li><strong>Data Persistence:</strong> Using volumes to keep data safe when containers restart.</li>"
                    "<li><strong>Networking:</strong> Connecting multiple containers to create a 3-tier application.</li>"
                    "</ul>"
                    "<h4>Reference Architecture</h4>"
                    "<p>Includes best practices for security and image optimization that are applicable to production environments.</p>"
                ),
                "url": "https://docs.docker.com/get-started",
            },
            {
                "name": "Kubernetes Documentation",
                "body": (
                    "<h3>Orchestration at Scale</h3>"
                    "<p>Kubernetes (K8s) is the de facto operating system of the cloud. The official documentation is vast, authoritative, and constantly updated by the open-source community. It's the only reference you need.</p>"
                    "<h4>Key Concepts</h4>"
                    "<ul>"
                    "<li><strong>Pods & Nodes:</strong> The atomic units of Kubernetes.</li>"
                    "<li><strong>Deployments & Sets:</strong> Managing stateless applications and ensuring availability.</li>"
                    "<li><strong>Services & Ingress:</strong> Exposing your applications to the outside world.</li>"
                    "<li><strong>ConfigMaps & Secrets:</strong> Managing configuration and sensitive data.</li>"
                    "</ul>"
                    "<h4>Tasks & Tutorials</h4>"
                    "<p>Step-by-step guides for common operations like performing rolling updates, scaling a cluster, and debugging a crashing pod.</p>"
                ),
                "url": "https://kubernetes.io/docs",
            },
            {
                "name": "TensorFlow Tutorials",
                "body": (
                    "<h3>Machine Learning for Everyone</h3>"
                    "<p>The TensorFlow tutorials are designed to be accessible to beginners while providing depth for experts. Many tutorials run directly in Google Colab, so you can start training models on a GPU instantly without any setup.</p>"
                    "<h4>Tutorial Categories</h4>"
                    "<ul>"
                    "<li><strong>Keras Quickstart:</strong> Build and train a neural network in 15 minutes.</li>"
                    "<li><strong>Computer Vision:</strong> Image classification, object detection, and segmentation.</li>"
                    "<li><strong>NLP:</strong> Text generation, sentiment analysis, and translation with Transformers.</li>"
                    "<li><strong>Generative AI:</strong> Create art and music using GANs and VAEs.</li>"
                    "</ul>"
                    "<h4>Production Ready</h4>"
                    "<p>Learn how to save your models and deploy them to mobile devices (TF Lite), the web (TF.js), or the server (TF Serving).</p>"
                ),
                "url": "https://tensorflow.org/tutorials",
            },
            {
                "name": "Vue.js Guide",
                "body": (
                    "<h3>The Progressive JavaScript Framework</h3>"
                    "<p>Vue.js is known for its gentle learning curve and excellent documentation. The guide takes you from a simple 'Hello World' to complex single-page applications.</p>"
                    "<h4>Core Concepts</h4>"
                    "<ul>"
                    "<li><strong>Declarative Rendering:</strong> Binding data to the DOM with simple template syntax.</li>"
                    "<li><strong>Reactivity:</strong> Understanding Vue's deep reactivity system (ref vs reactive).</li>"
                    "<li><strong>Components:</strong> Building reusable UI elements with props and events.</li>"
                    "<li><strong>Composition API:</strong> The modern way to organize logic in Vue 3.</li>"
                    "</ul>"
                    "<h4>Ecosystem</h4>"
                    "<p>Deep dives into the official router (Vue Router) and state management library (Pinia).</p>"
                ),
                "url": "https://vuejs.org/guide",
            },
            {
                "name": "Django Documentation",
                "body": (
                    "<h3>The Web Framework for Perfectionists with Deadlines</h3>"
                    "<p>Django's documentation is legendary for its quality and completeness. It covers everything from the initial project scaffolding to advanced security topics.</p>"
                    "<h4>The Polls Tutorial</h4>"
                    "<p>The famous introductory tutorial that walks you through creating a polling app, touching on models, views, templates, and admin.</p>"
                    "<h4>Topic Guides</h4>"
                    "<ul>"
                    "<li><strong>The ORM:</strong> Making database queries without writing SQL.</li>"
                    "<li><strong>Authentication:</strong> Managing users, groups, and permissions.</li>"
                    "<li><strong>Forms:</strong> Handling user input and validation securely.</li>"
                    "<li><strong>Deployment:</strong> Best practices for WSGI, static files, and security headers.</li>"
                    "</ul>"
                ),
                "url": "https://docs.djangoproject.com",
            },
            {
                "name": "Node.js Guides",
                "body": (
                    "<h3>Server-side JavaScript</h3>"
                    "<p>The official Node.js guides provide a comprehensive overview of the runtime's capabilities. It focuses on the asynchronous nature of Node and its standard library.</p>"
                    "<h4>Essential Topics</h4>"
                    "<ul>"
                    "<li><strong>Event Loop:</strong> Understanding the heart of Node.js concurrency.</li>"
                    "<li><strong>Modules:</strong> CommonJS vs ES Modules.</li>"
                    "<li><strong>File System:</strong> Reading and writing files with the fs API.</li>"
                    "<li><strong>HTTP:</strong> Creating a web server without a framework.</li>"
                    "</ul>"
                    "<h4>Debugging & Profiling</h4>"
                    "<p>Learn how to use the built-in debugger and profit tools to find memory leaks and performance bottlenecks.</p>"
                ),
                "url": "https://nodejs.org/en/docs/guides",
            },
            {
                "name": "PostgreSQL Tutorial",
                "body": (
                    "<h3>Master the World's Most Advanced Open Source Relational Database</h3>"
                    "<p>This tutorial covers PostgreSQL from the basics to advanced features. It's a great resource for developers who want to understand the database they are using.</p>"
                    "<h4>Section Breakdown</h4>"
                    "<ul>"
                    "<li><strong>Basic SQL:</strong> SELECT, INSERT, UPDATE, DELETE fundamentals.</li>"
                    "<li><strong>Filtering & Joining:</strong> Retrieving complex data relationships.</li>"
                    "<li><strong>Database Administration:</strong> Managing roles, databases, and schemas.</li>"
                    "<li><strong>Advanced Features:</strong> JSONB support, Full Text Search, and Stored Procedures.</li>"
                    "</ul>"
                    "<h4>Interactive</h4>"
                    "<p>Many examples include live SQL editors where you can try the queries yourself.</p>"
                ),
                "url": "https://postgresqltutorial.com",
            },
            {
                "name": "MongoDB University",
                "body": (
                    "<h3>The Official MongoDB Education Platform</h3>"
                    "<p>MongoDB University offers free courses taught by MongoDB engineers. Whether you are a DBA or a developer, there is a path for you to become a MongoDB expert.</p>"
                    "<h4>Course Highlights</h4>"
                    "<ul>"
                    "<li><strong>MongoDB Basics:</strong> NoSQL concepts, documents, and collections.</li>"
                    "<li><strong>The Aggregation Framework:</strong> Performing complex data analysis pipelines.</li>"
                    "<li><strong>Data Modeling:</strong> Schema design patterns for performance and scalability.</li>"
                    "<li><strong>Atlas:</strong> Deploying and managing clusters in the cloud.</li>"
                    "</ul>"
                    "<h4>Certification</h4>"
                    "<p>Prepare for the official MongoDB Developer or DBA Associate exam.</p>"
                ),
                "url": "https://university.mongodb.com",
            },
            {
                "name": "Figma Tutorial",
                "body": (
                    "<h3>Design for the Web</h3>"
                    "<p>Figma's learning resources are visually stunning and highly practical. They cover not just the tool, but design principles in general.</p>"
                    "<h4>What to Learn</h4>"
                    "<ul>"
                    "<li><strong>Interface Design:</strong> Frames, constraints, and auto-layout.</li>"
                    "<li><strong>Vector Networks:</strong> Drawing icons and illustrations.</li>"
                    "<li><strong>Prototyping:</strong> Creating interactive flows with transitions.</li>"
                    "<li><strong>Collaboration:</strong> Working with developers using Dev Mode.</li>"
                    "</ul>"
                    "<h4>Community Files</h4>"
                    "<p>Learn by dissecting thousands of open-source design files provided by the community.</p>"
                ),
                "url": "https://figma.com/resources/learn-design",
            },
            {
                "name": "Tailwind CSS Docs",
                "body": (
                    "<h3>Rapidly Build Modern Websites</h3>"
                    "<p>Tailwind's documentation is widely cited as the gold standard for developer experience. It features a powerful search and copy-paste examples for every utility class.</p>"
                    "<h4>Key Sections</h4>"
                    "<ul>"
                    "<li><strong>Utility-First Fundamentals:</strong> Why not just write CSS?</li>"
                    "<li><strong>Core Concepts:</strong> Hover, focus, and other states.</li>"
                    "<li><strong>Customization:</strong> Configuring the theme in tailwind.config.js.</li>"
                    "<li><strong>Layout:</strong> Flexbox and Grid utilities explained visually.</li>"
                    "</ul>"
                    "<h4>Component Examples</h4>"
                    "<p>See how to build common UI patterns like cards, navbars, and forms using only utility classes.</p>"
                ),
                "url": "https://tailwindcss.com/docs",
            },
            {
                "name": "TypeScript Handbook",
                "body": (
                    "<h3>JavaScript with Syntax for Types</h3>"
                    "<p>The TypeScript Handbook is the official guide to the language. It assumes you know JavaScript and builds on top of it, explaining how to add type safety to your code.</p>"
                    "<h4>Language Features</h4>"
                    "<ul>"
                    "<li><strong>Everyday Types:</strong> Primitives, arrays, and objects.</li>"
                    "<li><strong>Narrowing:</strong> How TypeScript understands type guards.</li>"
                    "<li><strong>Functions & Generics:</strong> Writing reusable, type-safe code.</li>"
                    "<li><strong>Object Types:</strong> Interfaces vs Type Aliases.</li>"
                    "</ul>"
                    "<h4>Configuration</h4>"
                    "<p>Deep dive into tsconfig.json options to tailor the compiler to your project's needs.</p>"
                ),
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
            resource = Resource.objects.filter(name=resource_data["name"]).first()

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

            tool, created = Tool.objects.update_or_create(
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
