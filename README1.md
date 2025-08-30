Here’s a clean **prompt you can hand to another engineer** so they immediately understand **LuckyClubWins.com** and what you need them to help build. I’ve kept it straightforward, without UrVote (since that can come later), and focused on the **user accounts + points system**.

---

# 🧵 **Engineer Onboarding Prompt — LuckyClubWins.com**

We are building a new project called **LuckyClubWins.com**.

---

## 🎯 Project Overview

LuckyClubWins.com is a **subscription raffle platform** where members pay monthly and get a set number of entries (points) toward that month’s prize. Each month, we run a new raffle (e.g., a Dell laptop, iPhone, or other high-value item).

Every member has:

* A **user account** (login, password, profile).
* A **monthly points balance** (raffle entries).
* The ability to **earn extra points** through different actions (for now, just admin-awarded or file uploads as proof of action).

At the end of the month, the raffle is drawn based on the total points each user has.

---

## 🛠️ Tech Stack

* **FastAPI** backend (Python)
* **Uvicorn** (with systemd for service management)
* **PostgreSQL** database (async SQLAlchemy)
* **Nginx + SSL** for reverse proxy and HTTPS
* **Frontend**: simple HTML templates (Jinja2) for dashboard + forms

---

## 🔑 Core Features (MVP)

1. **User Accounts**

   * Registration, login, password reset.
   * Basic user table with email + password hash.

2. **Raffles**

   * Table of monthly raffles (title, prize, active flag).
   * Each raffle is tied to a specific month.

3. **Points System**

   * Base entries automatically given when a member subscribes (e.g., 15/month).
   * Extra entries added via admin approval (e.g., “+3 points for proof upload”).
   * Ledger table that tracks *all point sources*:

     * Source: base / bonus / proof / admin.
     * Amount: integer.
     * Linked to raffle + user.

4. **Proof Uploads**

   * Users can upload a screenshot or file as “proof of action.”
   * Admin reviews → approves → entries credited.

5. **Dashboard**

   * Users log in and see:

     * Base entries this month.
     * Bonus entries earned.
     * Total entries in the active raffle.
   * Simple file upload form for proof.

6. **Admin Panel (MVP)**

   * List of pending proofs.
   * Approve/reject buttons.
   * When approved, entries get added automatically.

---

## 📦 Database Structure (simplified)

* **users** (id, email, password\_hash, created\_at)
* **raffles** (id, title, prize, month\_key, is\_active)
* **entry\_ledger** (id, user\_id, raffle\_id, source, amount, created\_at)
* **proof\_uploads** (id, user\_id, raffle\_id, kind, file\_path, status, reviewed\_at)

---

## 🚀 Immediate Goals

* Stand up the MVP so members can:

  1. Register/login.
  2. Get base entries for the current raffle.
  3. Upload proof for bonus entries.
  4. See their total entries in a dashboard.
* Admin can approve/reject proofs and credit entries.

---

## ❓ Open Questions / Ideas

* Should points reset every month automatically, or do we want a **carry-over system** (e.g., unclaimed entries roll over)?
* Do we want to log a **raffle draw history** (who won what) right from MVP, or handle that later?
* Should we expose a **leaderboard** (optional gamification) so users see how many points others have?

---

👉 That’s the current state. Could you help us refine the **points tracking system** so it’s clean and scalable (base + bonus entries, multiple raffles, proof uploads, admin approvals), and recommend any improvements before we lock in the database design?

---

Would you like me to also prepare a **visual ERD (Entity Relationship Diagram)** for the DB schema so your engineer immediately sees how `users`, `raffles`, `entry_ledger`, and `proof_uploads` connect?
