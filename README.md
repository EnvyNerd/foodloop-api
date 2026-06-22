# FoodLoop API

Flask backend for FoodLoop mobile app.

## Quick Start

```bash
pip install -r requirements.txt
python seed.py  # Optional: seed test data
python app.py   # Starts on http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login, returns JWT |
| GET | /bags | List bags (filters: category, halal, search, vendor_id) |
| GET | /bags/:id | Bag detail |
| POST | /vendor/bags | Create bag (vendor auth) |
| PUT | /vendor/bags/:id | Update bag (vendor auth) |
| DELETE | /vendor/bags/:id | Delete bag (vendor auth) |
| GET | /vendor/products | List vendor's products |
| POST | /orders | Create order (buyer auth) |
| GET | /orders | List buyer's orders |
| GET | /orders/:id | Order detail |
| PATCH | /orders/:id/status | Update order status |
| GET | /vendor/orders | List vendor's orders |
| GET | /vendor/stats | Vendor dashboard stats |
| GET/PUT | /vendor/profile | Vendor profile |
| GET | /vendor/payouts | Payout history |
| POST | /vendor/payouts/request | Request payout |
| GET | /notifications | List notifications |
| PATCH | /notifications/:id/read | Mark as read |
| GET | /user/profile | Buyer profile |

## Deployment

### Render.com
1. Push to GitHub
2. Create new Web Service on Render
3. Connect GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python app.py`
6. Add environment variables: SECRET_KEY, PLATFORM_FEE_PCT

### Docker
```bash
docker build -t foodloop-api .
docker run -p 5000:5000 foodloop-api
```
