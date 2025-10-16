# Tech Hive - Role-Based Permissions Matrix

---

- `POST /articles/like/` → Like/unlike an article - any authenticated user
- `POST /articles/summary/` → Summarize an article 
- `GET /articles/notification/` → Get notified of events
  
## 🎯 Contributor Role
**Article Management:**
- `GET /articles/drafts/` → View own drafts
- `POST /articles/drafts/` → Create new draft
- `PATCH /articles/drafts/{id}/` → Edit own draft
- `GET /feedback/{id}/` → View feedback on draft

**Onboarding:**
- `POST /contribute/accept/` → Accept guidelines → become Contributor

---

## 👀 Reviewer Role

**Review Management:**
- `GET /articles/review/assigned/` → View assigned articles
- `PUT /articles/review/{id}/status/under_review` → Mark as under review
- `PUT /articles/review/{id}/status/changes_requested` → Request changes
- `PUT /articles/review/{id}/status/review_completed` → Complete review
- 
- `PUT /articles/review/{id}/status/ready_for_publishing` → Mark ready to publish
- `POST /articles/review/{id}/reject` → Reject article

---

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