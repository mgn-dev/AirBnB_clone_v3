# HBnB — Phase 3: REST API

**AirBnB Clone · Phase 3 of 4**

Phase 3 transforms HBnB from a server-rendered site into a **RESTful JSON API**. Clients—whether a browser, mobile app, or curl—interact with resources through HTTP verbs while Flask blueprints keep the codebase organized.

| Phase | Project | Focus |
|-------|------------|-------|
| 1 | [AirBnB_clone](https://github.com/mgn-dev/AirBnB_clone) | Python OOP, console, JSON storage, static HTML/CSS |
| 2 | [AirBnB_clone_v2](https://github.com/mgn-dev/AirBnB_clone_v2) | Flask routes and Jinja2 templates |
| **3 — current phase** | `AirBnB_clone_v3` | REST API and CRUD endpoints |
| 4 | [AirBnB_clone_v4](https://github.com/mgn-dev/AirBnB_clone_v4) | MySQL, SQLAlchemy, Swagger, dynamic JS, auth |

---

## Skills covered


- Structure a Flask app with **Blueprints** and a versioned URL prefix (`/api/v1`)
- Build **CRUD endpoints** (GET, POST, PUT, DELETE) for every HBnB resource
- Return proper **HTTP status codes** (200, 201, 400, 404) and JSON error bodies
- Enable **Cross-Origin Resource Sharing (CORS)** for browser-based API consumers
- Manage request lifecycle with **teardown handlers** that close storage sessions
- Continue serving **Jinja2 pages** alongside the API in the same project
- Deploy static assets with automated Fabric scripts

---

## Project Structure

```
AirBnB_clone_v3/
├── api/
│   └── v1/
│       ├── app.py              # Flask entry point, CORS, error handlers
│       └── views/
│           ├── __init__.py     # Blueprint: app_views (/api/v1)
│           ├── index.py        # /status, /stats
│           ├── states.py       # State CRUD
│           ├── cities.py       # City CRUD + cities by state
│           ├── amenities.py    # Amenity CRUD
│           ├── users.py        # User CRUD
│           ├── places.py       # Place CRUD
│           ├── places_reviews.py
│           └── places_amenities.py
├── models/                     # Domain model + FileStorage
├── web_flask/                  # Jinja2 routes (Phase 2, extended)
├── web_static/                 # Static HTML/CSS
├── console.py                  # Data seeding via command interpreter
└── tests/
```

---

## Running the API

```bash
export HBNB_API_HOST=0.0.0.0
export HBNB_API_PORT=5000
python3 -m api.v1.app
```

Quick health check:

```bash
curl http://0.0.0.0:5000/api/v1/status/
# {"status":"OK"}
```

Object counts:

```bash
curl http://0.0.0.0:5000/api/v1/stats/
# {"amenities":0,"cities":0,"places":0,"reviews":0,"states":0,"users":0}
```

---

## API Endpoints

All routes are prefixed with `/api/v1`.

### Index

| Method | Path | Description |
|--------|------|-------------|
| GET | `/status` | API health check |
| GET | `/stats` | Count of objects per type |

### States

| Method | Path | Description |
|--------|------|-------------|
| GET | `/states` | List all states |
| GET | `/states/<id>` | Retrieve one state |
| DELETE | `/states/<id>` | Delete a state |
| POST | `/states` | Create a state (`name` required) |
| PUT | `/states/<id>` | Update a state |

### Cities

| Method | Path | Description |
|--------|------|-------------|
| GET | `/states/<state_id>/cities` | Cities belonging to a state |
| GET | `/cities/<id>` | Retrieve one city |
| DELETE | `/cities/<id>` | Delete a city |
| POST | `/cities` | Create a city (`name`, `state_id` required) |
| PUT | `/cities/<id>` | Update a city |

### Amenities, Users, Places, Reviews

Each resource follows the same REST pattern:

- **Collection** — `GET /resources`, `POST /resources`
- **Item** — `GET /resources/<id>`, `PUT /resources/<id>`, `DELETE /resources/<id>`

Places additionally expose nested routes:

| Method | Path | Description |
|--------|------|-------------|
| GET/POST/DELETE | `/places/<place_id>/amenities` | Link amenities to a place |
| GET/POST/DELETE | `/places/<place_id>/reviews` | Manage reviews for a place |

### Example: Create and Retrieve a State

```bash
# Create
curl -X POST http://0.0.0.0:5000/api/v1/states/ \
  -H "Content-Type: application/json" \
  -d '{"name": "California"}'

# List
curl http://0.0.0.0:5000/api/v1/states/

# Delete
curl -X DELETE http://0.0.0.0:5000/api/v1/states/<state_id>
```

Invalid requests return descriptive errors:

- `400` — Missing required JSON field or body is not JSON
- `404` — Resource not found

---

## Blueprint Architecture

`api/v1/views/__init__.py` registers a single blueprint:

```python
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
```

Each view module (`states.py`, `cities.py`, …) attaches routes to `app_views`. The main app in `api/v1/app.py` registers the blueprint, configures CORS, and defines teardown/error handlers:

```python
@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404
```

---

## Flask Web Routes (Coexisting)

The `web_flask/` directory still serves HTML pages that read directly from storage—useful for comparing server-rendered vs. API-driven approaches:

| Route | Template | Data Source |
|-------|----------|-------------|
| `/states_list` | `7-states_list.html` | `storage.all("State")` |
| `/cities_by_states` | `8-cities_by_states.html` | States + nested cities |
| `/states/<id>` | `9-states.html` | Single state detail |

Seed data with `./console.py`, then verify both the HTML pages and JSON endpoints reflect the same objects.

---

## CORS

```python
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
```

This allows browser JavaScript running on another origin to call the API—a requirement for the dynamic front end built in Phase 4.

---

## Deployment Scripts

| Script | Purpose |
|--------|---------|
| `0-setup_web_static.sh` | Remote Nginx setup |
| `1-pack_web_static.py` | Archive static files |
| `2-do_deploy_web_static.py` | Upload release |
| `3-deploy_web_static.py` | End-to-end deploy |

---

## Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `HBNB_API_HOST` | `0.0.0.0` | Bind address |
| `HBNB_API_PORT` | `5000` | Listen port |

**Dependencies:** Flask, Flask-CORS, Python 3.x

---

## What Came Before · What Comes Next

- **[Phase 2](https://github.com/mgn-dev/AirBnB_clone_v2)** — Flask routes and Jinja2 covers rendering HTML from Python.
- **[Phase 4](https://github.com/mgn-dev/AirBnB_clone_v4)** — Swap JSON file storage for **MySQL + SQLAlchemy**, document the API with **Swagger**, build a **dynamic JavaScript front end**, and add **user authentication** with hashed passwords.

---

## License

Public domain.
