# 📚 Library & Event Booking Management System

A role-based full-stack web application that allows clients and admins to manage books, events, study room reservations, and payment tracking. 

---

## 🔧 Tech Stack
### Frontend:
- **React.js** – SPA architecture
- **React Router DOM** – Client-side routing
- **Context API** – Auth & session management
- **Chart.js / Recharts** – Dashboard visualizations
- **HTML5 / CSS3** – UI styling

### Backend:
- **phpMyAdmin + MySQL** – Relational database
- **SQL** – Queries, joins, constraints

---

## 🧑‍💼 Features by Role

### 🧑‍💻 Admin:
- Manage clients, books, events, and invoices
- View interactive dashboard charts
- View rental and reservation history
- Create/edit/delete entities
- Secure login with RBAC

### 👤 Customer:
- Login and view personal dashboard
- Book study rooms
- Borrow physical or eBooks
- View invoices and payment status
- Attend or host events

---

## 🗃️ Key Tables

- `ps_client` – Client master
- `ps_book`, `ps_author`, `ps_topic` – Book management
- `ps_rental`, `ps_copy` – Rental tracking
- `ps_invoice`, `ps_payment` – Payment management
- `ps_event`, `ps_exp`, `ps_spon`, `ps_se` – Event management
- `ps_study_room`, `ps_reserve` – Room booking system

---

## 🔐 Security

- Role-based access control (RBAC)
- Route protection using React + Context
- Frontend form validation (required, password match)
- Session persistence using `localStorage`

---

## 📊 Dashboard Graphs

Admins see:
- Book rental trends
- Revenue over time
- Event bookings

Customers see:
- Personal booking history
- Payment summaries
