# Django — Blog

A blog with categories, search, pagination, comments, a configured admin and a
small read-only JSON API.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations blog
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Site: http://localhost:8000
- Admin (create posts here): http://localhost:8000/admin
- API: http://localhost:8000/api/posts/ and `/api/posts/<slug>/`

## Test

```bash
python manage.py test blog
```

## Concepts shown
- Custom model manager (`Post.published`) hides drafts and future-dated posts
- Auto-generated unique slugs
- `select_related` to avoid N+1 queries
- ModelForm with CSRF protection and Post/Redirect/Get
- Admin customization: filters, search, inlines and a bulk action
- Template inheritance

---

Portfolio reference implementation by [Zaid Mubbashar](https://github.com/ranazaid) · [zaid-mubbashar.vercel.app](https://zaid-mubbashar.vercel.app)
