# SmartCampus AI

Socle technique d’une plateforme d’orientation universitaire. Le chatbot de démonstration utilisera des réponses déterministes via l’API FastAPI; aucun LLM, modèle, embedding ou pipeline RAG n’est intégré.

## Architecture

- `frontend/` : Next.js App Router, React/TypeScript strict, Tailwind, page d’accueil chat sans connexion candidat.
- `backend/` : FastAPI, configuration Pydantic, base asynchrone SQLAlchemy et API versionnée sous `/api/v1`.
- `data/` : données et scripts de démonstration à venir.
- `docs/` : documentation complémentaire à venir.
- `docker-compose.yml` : PostgreSQL, API et frontend.

## Lancement avec Docker

1. Copiez `.env.example` vers `.env` et remplacez les secrets pour tout usage hors démonstration locale.
2. Lancez `docker compose up --build`.
3. Ouvrez le frontend sur http://localhost:3000, la documentation FastAPI sur http://localhost:8000/docs et le contrôle de santé sur http://localhost:8000/api/v1/health.

Les données PostgreSQL persistent dans le volume `postgres_data`. Pour arrêter les services, utilisez `docker compose down`. Supprimer les données nécessite explicitement `docker compose down -v`.

## Lancement sans Docker

API, depuis `backend/` :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Configurez `DATABASE_URL` et les autres variables depuis la racine (ou votre environnement). PostgreSQL doit être accessible à l’adresse configurée.

Frontend, depuis `frontend/` :

```powershell
npm install
npm run dev
```

## État

Le socle API expose une route de santé et un endpoint de chat déterministe :

- `GET /api/v1/health` : vérifie que l’API est disponible.
- `POST /api/v1/chat` : accepte `{"message": "...", "session_id": null}` et retourne
  `{"reply": "...", "session_id": "..."}`.

Le chatbot ne consomme pas encore de LLM et ne persiste pas les conversations en
base de données. En l’absence de données de formations dans le projet, il indique
que le catalogue sera bientôt disponible. Les sessions, les modèles/migrations,
l’authentification et les espaces métier restent à implémenter dans les prochaines
étapes. Les liens Formations et Préinscription sont des points de navigation
provisoires.

## Tests

Depuis `backend/` :

```powershell
python -m unittest discover -s tests -v
```

Depuis `frontend/` :

```powershell
npm test
npm run lint
npm run build
```
