# Nadhira Backend On Render

Upload this `backend-render` folder to GitHub as a repository.

## Render Setup

1. Render Dashboard -> New -> Blueprint.
2. Select the GitHub repo that contains this folder.
3. Render will read `render.yaml`.
4. It creates:
   - Web service: `nadhira-api`
   - PostgreSQL database: `nadhira-db`
5. After deploy, Render gives a URL like:

```text
https://nadhira-api.onrender.com
```

Open:

```text
https://nadhira-api.onrender.com/
```

Expected response:

```json
{"status":"running","app":"Nadhira Skin Clinic"}
```

## Custom API Domain

Best setup:

```text
api.nadhira.in -> Render backend
```

In Render, add custom domain `api.nadhira.in`.
In Hostinger DNS, add the CNAME/A record Render asks for.

If custom domain is not ready, frontend can directly use:

```text
https://nadhira-api.onrender.com
```

Update frontend `index.html` API URL accordingly.
