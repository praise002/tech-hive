# Tech Hive - Role-Based Permissions Matrix

---
- `POST /articles/summary/` → Summarize an article 
  
## 🎯 Contributor Role
**Article Management:**

- `GET /feedback/{id}/` → View feedback on draft
---


## 👀 Reviewer Role

**Review Management:**
- GET    /api/reviews/assigned/                 # List reviews assigned to me
- GET    /api/reviews/{review_id}/        # Get specific review details
- PATCH  /api/reviews/{review_id}/        # Update review (status, feedback etc.)

POST /api/articles/review/{id}/start/          # Start review
POST /api/articles/review/{id}/request-changes/ # Request changes
POST /api/articles/review/{id}/approve/        # Approve (mark ready)
POST /api/articles/review/{id}/reject/         # Reject

---

"""
Permission for Editors:
- Can publish articles x
- Can add tags to articles x
- Can assign reviewers to articles x
# - Can view articles ready for publishing x
- Can view articles
- Can add published articles to categories x
 """

"""
Permission for Managers:
- Create reviewer account
- Create editor account
- View platform statistics (only this will be handled in the views)
"""
## ✏️ Editor Role

**Publishing Management:**
- `GET /articles/ready/` → View articles ready for publishing
- `PUT /articles/{id}/publish` → Publish article
- `PUT /articles/{id}/assign_reviewer` → Assign reviewer to article

---

## 👔 Manager Role
**Has access to Django admin panel:**

**User Management:**
- `POST /users/reviewer/` → Create reviewer account
- `POST /users/editor/` → Create editor account
- `GET /stats/` → View platform statistics

---

## 🔧 Admin Role

**System Administration:**
- `GET /admin/` → Django admin panel with full control
- Complete system access and configuration

---

## 💳 Premium Subscription

**Subscription Management:**
- `POST /subscriptions/premium/` → Subscribe to premium plan
- `GET /subscriptions/` → Get current subscription details
- `DELETE /subscriptions/premium/` → Cancel premium subscription
- `PATCH /subscriptions/premium/reactivate/` → Reactivate cancelled subscription
- `PATCH /subscriptions/premium/` → Update subscription plan
- `GET /subscriptions/history/` → View subscription and billing history

**Permissions:** Any authenticated user can manage their own subscription

No Subscription → Subscribe → Active → Cancel → Cancelled
      ↑                                    ↓
      └─────────── Reactivate ←────────────┘
                        ↓
                   Expired (if not reactivated)

---

## 🔄 Article Workflow

```
Draft →  Submit draft → Under Review → Changes Requested ↴
  ↓                                       ↓
Published ← Ready for Publishing ← Review Completed
  ↓
Rejected (end state)
```

## 👥 Role Hierarchy

```
Admin (highest authority)
  ↓
Manager
  ↓
Editor
  ↓
Reviewer
  ↓
Contributor
  ↓
User (lowest - read-only)
```

TODO: USING HTTP-ONLY-COOKIE

---

# API Endpoint Documentation

This document provides a comprehensive overview of all available API endpoints.

## 1. Authentication (`/api/v1/auth/`)

Handles user registration, login, logout, and password management.

| Method | Endpoint                       | Description                                         | Permissions      |
| :----- | :----------------------------- | :-------------------------------------------------- | :--------------- |
| `POST` | `/register/`                   | Register a new user.                                | Public           |
| `POST` | `/token/`                      | Log in a user and obtain JWT tokens.                | Public           |
| `POST` | `/token/refresh/`              | Refresh an expired access token.                    | Authenticated    |
| `POST` | `/sessions/`                   | Log out the current user (blacklist refresh token). | Authenticated    |
| `POST` | `/sessions/all/`               | Log out from all devices.                           | Authenticated    |
| `POST` | `/verification/`               | Resend the email verification OTP.                  | Authenticated    |
| `POST` | `/verification/verify/`        | Verify a user's email with the provided OTP.        | Authenticated    |
| `POST` | `/passwords/change/`           | Change the password for an authenticated user.      | Authenticated    |
| `POST` | `/passwords/reset/`            | Request a password reset email.                     | Public           |
| `POST` | `/passwords/reset/verify/`     | Verify the password reset OTP.                      | Public           |
| `POST` | `/passwords/reset/complete/`   | Set a new password after verification.              | Public           |
| `GET`  | `/signup/google/`              | Initiate Google OAuth2 registration.                | Public           |
| `GET`  | `/login/google/`               | Initiate Google OAuth2 login.                       | Public           |

## 2. Profiles (`/api/v1/profiles/`)

Manages user profiles and user-specific content like articles, comments, and saved items.

| Method | Endpoint                       | Description                                                              | Permissions      |
| :----- | :----------------------------- | :----------------------------------------------------------------------- | :--------------- |
| `GET`  | `/me/`                         | Retrieve the profile of the authenticated user.                          | Authenticated    |
| `PATCH`| `/me/`                         | Update the profile of the authenticated user.                            | Authenticated    |
| `PATCH`| `/avatar/`                     | Upload or update the user's avatar.                                      | Authenticated    |
| `POST` | `/onboarding/`                 | Submit contributor onboarding application.                               | Authenticated    |
| `GET`  | `/usernames/`                  | Get a list of usernames for comment mentions.                            | Authenticated    |
| `GET`  | `/me/articles/`                | List all articles created by the authenticated user.                     | Contributor      |
| `POST` | `/me/articles/`                | Create a new article draft.                                              | Contributor      |
| `GET`  | `/me/articles/<slug>/`         | Retrieve a specific article owned by the user.                           | Contributor      |
| `PATCH`| `/me/articles/<slug>/`         | Update a specific article owned by the user.                             | Contributor      |
| `GET`  | `/me/saved/`                   | List all articles saved by the user.                                     | Authenticated    |
| `POST` | `/me/saved/`                   | Save or unsave an article.                                               | Authenticated    |
| `GET`  | `/me/comments/`                | List all comments made by the user.                                      | Authenticated    |
| `GET`  | `/<username>/`                 | Retrieve the public profile of any user.                                 | Public           |

## 3. Content (`/api/v1/`)

Endpoints for accessing public content like articles, categories, jobs, and more.

| Method | Endpoint                               | Description                                                              | Permissions      |
| :----- | :------------------------------------- | :----------------------------------------------------------------------- | :--------------- |
| `GET`  | `/articles/`                           | List all published articles.                                             | Public           |
| `GET`  | `/articles/<username>/<slug>/`         | Retrieve a single published article by author and slug.                  | Public           |
| `POST` | `/comments/`                           | Create a top-level comment on an article.                                | Authenticated    |
| `GET`  | `/comments/<comment_id>/replies/`      | Retrieve the replies for a specific comment.                             | Public           |
| `GET`  | `/categories/`                         | List all content categories.                                             | Public           |
| `GET`  | `/tags/`                               | List all article tags.                                                   | Public           |
| `GET`  | `/jobs/`                               | List all job postings.                                                   | Public           |
| `GET`  | `/events/`                             | List all tech events.                                                    | Public           |
| `GET`  | `/resources/`                          | List all learning resources.                                             | Public           |
| `GET`  | `/tools/`                              | List all tech tools.                                                     | Public           |
| `POST` | `/contribute/`                         | Accept contributor guidelines to become a contributor.                   | Authenticated    |
| `GET`  | `/articles/feed/`                      | Get an RSS feed of the latest articles.                                  | Public           |

## 4. Notifications (`/api/v1/`)

| Method | Endpoint            | Description                               | Permissions   |
| :----- | :------------------ | :---------------------------------------- | :------------ |
| `GET`  | `/notifications/`   | Retrieve notifications for the user.      | Authenticated |

## 5. General (`/api/v1/`)

General-purpose endpoints for site details and user engagement.

| Method | Endpoint         | Description                               | Permissions |
| :----- | :--------------- | :---------------------------------------- | :---------- |
| `GET`  | `/site-detail/`  | Get general site details.                 | Public      |
| `POST` | `/newsletter/`   | Subscribe a user to the newsletter.       | Public      |
| `POST` | `/contact/`      | Submit a contact form entry.              | Public      |

## 6. System & Docs

Endpoints for system health, API schema, and documentation.

| Method | Endpoint             | Description                               |
| :----- | :------------------- | :---------------------------------------- |
| `GET`  | `/api/v1/healthcheck/` | Check the health status of the API.       |
| `GET`  | `/api/schema/`       | Retrieve the OpenAPI schema.              |
| `GET`  | `/`                  | View the API documentation (Swagger UI).  |
| `GET`  | `/api/schema/redoc/` | View the API documentation (ReDoc).       |
| `GET`  | `/sitemap.xml`       | Get the site's XML sitemap.               |