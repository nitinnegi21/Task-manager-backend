# Task Management API

Hey! This is a simple REST API I built for managing tasks. It's written in Flask and uses MongoDB for storage.

## What does it do?

Pretty straightforward - you can create tasks, mark them complete, update them, delete them, and get some basic statistics. Nothing fancy, but it gets the job done.

## Tech Stack

- **Flask** - Web framework
- **MongoDB** - Database (because I needed something flexible)
- **PyMongo** - MongoDB driver
- **Flask-CORS** - For handling cross-origin requests

## Getting Started

### What you need

- Python 3.8 or newer
- MongoDB running locally (or a connection string to a remote instance)
- That's pretty much it

### Installation

Clone this and set things up:

```bash
# Get the code
git clone <your-repo>
cd task-management-backend

# Make a virtual environment (seriously, do this)
python -m venv venv

# Turn it on
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install stuff
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root folder. Here's what mine looks like:

```env
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=some-random-string-here

MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=todolist

LOG_LEVEL=INFO
LOG_FILE=app.log
```

Change `SECRET_KEY` to something random. The rest should work as-is if you're running MongoDB locally.

### Running it

```bash
python app.py
```

That's it. The API will be running on `http://localhost:5000`.

## Project Structure

I organized it like this to keep things clean:

```
task-management-backend/
├── app.py                  # Main entry point
├── config.py              # All the config stuff
├── database.py            # MongoDB connection logic
├── models/
│   └── task.py           # Task operations (CRUD)
├── routes/
│   └── task_routes.py    # All the API endpoints
├── utils/
│   ├── validators.py     # Input validation
│   ├── response.py       # Standard response format
│   ├── error_handlers.py # Error handling
│   └── logger.py         # Logging setup
└── tests/                # Tests (wrote these to make sure nothing breaks)
```

## API Endpoints

All responses follow this format:

```json
{
  "success": true,
  "status_code": 200,
  "data": { ... },
  "message": "optional message"
}
```

### Check if it's alive

**GET** `/api/health`

Just checking if everything's connected properly.

### Get all tasks

**GET** `/api/tasks`

Optional filters:
- `completed=true/false` - Filter by completion status
- `priority=low/medium/high` - Filter by priority
- `status=pending/in_progress/completed` - Filter by status
- `page=1` - Page number (default: 1)
- `limit=20` - Items per page (default: 20)

Example:
```bash
curl http://localhost:5000/api/tasks?completed=false&priority=high
```

### Get a specific task

**GET** `/api/tasks/{task_id}`

### Create a task

**POST** `/api/tasks`

Send this:
```json
{
  "title": "Finish the README",
  "description": "Make it look human-written",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59"
}
```

Only `title` is required. Priority defaults to "medium" if you don't specify.

### Update a task

**PUT** `/api/tasks/{task_id}`

Send whatever fields you want to update:
```json
{
  "title": "Updated title",
  "priority": "low"
}
```

### Delete a task

**DELETE** `/api/tasks/{task_id}`

### Toggle completion

**PATCH** `/api/tasks/{task_id}/toggle`

Quick way to mark a task as done (or undone).

### Get statistics

**GET** `/api/tasks/stats`

Returns counts for total tasks, completed, priorities, etc.

## Testing

I wrote some tests. Run them with:

```bash
pytest
```

For more details:
```bash
pytest -v
```

To see coverage:
```bash
pytest --cov=. --cov-report=html
```

## Common Issues

**MongoDB connection fails:**
- Make sure MongoDB is actually running
- Check your connection string in `.env`

**Port 5000 already in use:**
- Change `FLASK_PORT` in your `.env` file
- Or kill whatever's using port 5000

**Import errors:**
- Did you activate the virtual environment?
- Try `pip install -r requirements.txt` again

## Notes

- This uses Flask's development server. Don't use this in production - use gunicorn or something similar.
- Logs go to `logs/app.log` - check there if something's broken
- The API uses MongoDB indexes for better performance, but if you're just testing with a few tasks you won't notice
- All dates are stored in UTC

## What's next?

Some ideas if you want to extend this:
- Add user authentication (JWT maybe?)
- Add task categories or tags
- File attachments for tasks
- Task comments
- Notifications for due dates

## License

MIT - do whatever you want with it

## Questions?

If something's not working, check the logs first. If you're still stuck, open an issue.

---

Built this as part of an assignment. Hope it's useful!