# CRUD React Frontend

A deliberately simple React frontend for the current FastAPI CRUD backend.

## Run locally

```bash
npm install
npm run dev
```

Set:

```env
VITE_API_URL=http://localhost:8000
```

The frontend uses the backend routes that currently exist:
- `/auth`
- `/users`
- `/posts`
- `/media`
- `/vote`
- `/bookmarks`
- `/stories`
- `/messages`
- `/livestreams`

No fake settings, notifications, follower dashboards, or invented endpoints are included.

## Docker

```bash
docker build --build-arg VITE_API_URL=http://localhost:8000 -t crud-frontend:latest .
docker run --rm -p 5173:80 crud-frontend:latest
```

For Kubernetes, build/push the image to your registry and expose the frontend with its own Service/Ingress. Configure `VITE_API_URL` at build time to the URL the browser can reach for FastAPI.
