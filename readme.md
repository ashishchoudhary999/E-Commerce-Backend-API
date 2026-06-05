# 🛒 E-Commerce Backend API

A production-ready, role-aware REST API for a full online shopping experience. Built with **FastAPI**, **PostgreSQL**, and **JWT authentication**, featuring a complete cart-to-checkout flow with real-time stock management, frozen order pricing, and background-task readiness.

🔗 **Live API Docs:** [https://your-live-url.onrender.com/docs](https://e-commerce-backend-api-58ws.onrender.com//docs)  
⚠️ *Hosted on a free tier — the first request after inactivity may take ~50 seconds to wake the server.*

---

## ✨ Features

- 🔐 **Role-Based Access Control (RBAC)** — secure `admin` vs `customer` roles with JWT authentication
- 📦 **Product Catalog** — public browsing + admin-only CRUD
- 🛒 **Smart Shopping Cart** — quantity merging, live price calculation, per-user isolation
- 📦 **Order Checkout** — atomic order creation, stock reduction, price freezing (`price_at_purchase`)
- 📜 **Order History & Cancellation** — business-rule enforcement (only `pending` orders can be cancelled)
- 🛡️ **Protected Routes** — endpoints secured via `get_current_user` and `require_admin` dependencies
- ☁️ **Cloud Deployed** — running on Render with managed Neon PostgreSQL
- 🔄 **Ready for Async Tasks** — structured for Celery + Redis integration (background emails, inventory sync, etc.)

---

## 🛠️ Tech Stack

| Layer             | Technology                          |
|-------------------|-------------------------------------|
| Language          | Python                              |
| Framework         | FastAPI                             |
| Database          | PostgreSQL (Neon)                   |
| ORM               | SQLAlchemy                          |
| Validation        | Pydantic                            |
| Auth              | JWT (python-jose), Passlib + Bcrypt |
| Server            | Uvicorn                             |
| Deployment        | Render                              |

---

## 📚 API Endpoints

### 🔑 Authentication
| Method | Endpoint          | Description                     | Auth Required |
|--------|-------------------|---------------------------------|---------------|
| POST   | `/users/register` | Register a new user             | No            |
| POST   | `/users/login`    | Login and receive JWT token     | No            |

### 📦 Products (Public Browse + Admin CRUD)
| Method | Endpoint             | Description                     | Auth Required      |
|--------|----------------------|---------------------------------|--------------------|
| GET    | `/products/`         | List all products               | No                 |
| GET    | `/products/{id}`     | Get single product              | No                 |
| POST   | `/products/`         | Create product                  | ✅ Admin Only      |
| PUT    | `/products/{id}`     | Update product                  | ✅ Admin Only      |
| DELETE | `/products/{id}`     | Delete product                  | ✅ Admin Only      |

### 🛒 Cart (Per-User)
| Method | Endpoint               | Description                     | Auth Required |
|--------|------------------------|---------------------------------|---------------|
| POST   | `/cart/`               | Add item to cart                | Yes           |
| GET    | `/cart/`               | View cart with totals           | Yes           |
| PUT    | `/cart/{product_id}`   | Update item quantity            | Yes           |
| DELETE | `/cart/{product_id}`   | Remove item from cart           | Yes           |

### 📜 Orders (Checkout & History)
| Method | Endpoint                      | Description                     | Auth Required |
|--------|-------------------------------|---------------------------------|---------------|
| POST   | `/orders/`                    | Place order (checkout)          | Yes           |
| GET    | `/orders/`                    | View order history              | Yes           |
| PUT    | `/orders/{id}/cancel`         | Cancel pending order            | Yes           |

---

## 🏗️ Project Structure

```text
ecommerce-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point + OpenAPI override
│   ├── database.py          # DB engine, session, connection pooling
│   ├── models.py            # SQLAlchemy models (User, Product, CartItem, Order, OrderItem)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── crud.py              # Database operations & business logic
│   ├── auth.py              # Password hashing, JWT, get_current_user, require_admin
│   └── routes/
│       ├── __init__.py
│       ├── user.py          # Register & login endpoints
│       ├── product.py       # Product CRUD + public browsing
│       ├── cart.py          # Cart management (per-user)
│       └── order.py         # Order placement, history, cancellation
├── requirements.txt
├── .env
├── .gitignore
└── README.md

🚀 Local Setup
1. Clone the repository
Bash

git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api
2. Create and activate a virtual environment
Bash

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
Bash

pip install -r requirements.txt
4. Configure environment variables
Create a .env file in the project root:

env

DATABASE_URL=postgresql://user:password@host/dbname
SECRET_KEY=your_long_random_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
💡 Generate a strong SECRET_KEY with:

Bash

python -c "import secrets; print(secrets.token_hex(32))"
5. Run the server
Bash

uvicorn app.main:app --reload
Visit http://127.0.0.1:8000/docs to explore the interactive API.

🔑 Environment Variables
Variable	Description
DATABASE_URL	Full PostgreSQL connection string
SECRET_KEY	Secret used to sign JWT tokens
ALGORITHM	JWT signing algorithm (e.g. HS256)
ACCESS_TOKEN_EXPIRE_MINUTES	Token lifetime in minutes
🧠 How Authentication & Roles Work
User registers → password is hashed with bcrypt and stored (never in plain text).
User logs in → server verifies the password and returns a signed JWT access token.
For protected routes, the client sends the token in the header:
Authorization: Bearer <token>
The server decodes and verifies the token, identifies the user, and checks their role:
customer → can browse, manage cart, place orders
admin → full product CRUD access
Business rules are enforced at checkout: stock validation, price freezing, cart clearing, and order history tracking.

👤 Author
Ashish Choudhary
GitHub: @ashishchoudhary999

📄 License
This project is licensed under the MIT License — see below.

MIT License

Copyright (c) 2026 Ashish Choudhary

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.