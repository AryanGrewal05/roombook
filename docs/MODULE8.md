# CSC325 Module 8: RoomBook CI/CD

## Local development

Use Python 3.12, a virtual environment, and MongoDB 8.0. No paid service is
needed. Set `MONGODB_URI` to your local MongoDB for tests; never run integration
tests against a production database (Django creates and drops `test_roombook`).

```bash
python -m pip install -r requirements.txt ruff==0.16.9
python manage.py check
python manage.py makemigrations --check --dry-run
ruff check .
python -m pytest booking/tests/unit
python manage.py test booking.tests.integration --noinput
```

For a new local database, run `python manage.py migrate --noinput`. The previous
version could create `booking_booking` before having an initial migration. For
an existing database, first verify its collection matches the fields in
`booking/migrations/0001_initial.py` (ObjectId id, room, start, end), then use
`python manage.py migrate --fake-initial --noinput`. This records the matching
initial migration without dropping bookings. Do not use `--fake` to hide other
migration failures.

Start development with `python manage.py runserver`. `GET /` reports running.
`POST /api/bookings/` accepts JSON such as:

```json
{"room":"L-204","start":"2026-10-25T09:00:00Z","end":"2026-10-25T10:00:00Z"}
```

Expected: 201 created; 409 for overlap in the same room; 400 for missing or
invalid fields, end at/before start, or duration over 120 minutes. Back-to-back
bookings and overlapping bookings in different rooms succeed. This classroom
API has no authentication; its overlap check is not atomic under simultaneous
requests and is not a production reservation guarantee.

## Connect the existing Render service

Use the existing service at https://roombook-aryangrewal05.onrender.com.
Do not create a new service, database, Blueprint, or paid plan.

In that service's Render settings, verify the repository is
`AryanGrewal05/roombook` and the branch is `main`. Keep its existing MongoDB
connection. Use these commands:

- Build: `pip install -r requirements.txt`
- Start: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --no-control-socket`
- Health check path: `/`

Set `MONGODB_URI` to the existing database connection and `DJANGO_SECRET_KEY` to
a strong secret in Render's environment settings. Set `DJANGO_SECURE=1` to use
HTTPS security settings; Render supplies the forwarded-protocol header.
Do not put secret values in Git or PR comments.

Copy the existing service's **Deploy Hook** from Render Settings. In GitHub,
Settings → Secrets and variables → Actions → New repository secret, save it as
`RENDER_DEPLOY_HOOK_URL`. It is an `https://api.render.com/deploy/...` URL.
A production environment secret of the same name is also supported.
Disable Render's automatic deploy-on-commit behavior so the workflow is the
only deployment trigger and tests must pass first. Retain the existing plan.

The workflow runs Setup → Dependencies → Test → Deploy. Each job has its own
runner, so Test installs its own dependencies. Feature pushes and PRs validate
without deploying. Only a push to `main` after Test succeeds triggers the
existing deploy hook. A successful Deploy job proves the hook accepted the
request; verify the final deployment, commit, and logs in Render Events.
A running homepage alone does not prove the new commit finished deploying.
The hook deploys the service's configured branch; it does not upload the
feature-branch checkout.

The initial migration must be handled once for existing databases as described
above. The workflow deliberately does not mutate the production database.

## Protect main

In GitHub Settings → Branches (or Rules → Rulesets), first inspect existing
rules and preserve stronger protections. Add a rule targeting `main`:

- Require a pull request before merging.
- Require status checks and require the branch to be up to date.
- Select `Test`, `ci-gate`, and `security` after their first successful PR runs.
  `Test` is the CSC325 test job; `ci-gate` covers the existing Pipeline matrix.
- Require conversation resolution; block force pushes and branch deletion.
- Apply to administrators if appropriate for the class demonstration.

Do not require `Deploy`: it is intentionally skipped on pull requests.
For a solo assignment, do not require an approval you cannot obtain yourself;
if the rubric requires review, arrange a classmate/instructor reviewer and
require one approval. Branch protection availability depends on repository
visibility and the existing GitHub plan; do not upgrade to a paid plan.

## Recording and demonstration

Keep the feature branch and PR unmerged until ready to record. Do not trigger a
manual Render deploy beforehand. Start recording before the required commit
and push; show the diff and tests, commit your reviewed work on
`feature/csc325-module8-cicd`, and push it. Open a PR to `main`, show the Setup,
Dependencies, Test checks and skipped Deploy, and show branch protection.
After recording those steps and satisfying the rubric, merge the PR yourself
when ready. Show the resulting `main` workflow deployment and the matching
Render Event, then verify the live API. Do not expose the deploy hook or database
credentials on screen. If a separate demonstration change is required, create
that small reviewed change only when recording; this setup does not pre-create
or merge that demonstration commit.

When recording, review the files first, then run from the repository root:

```bash
git status --short
git diff --check
git add .github/workflows/csc325_ci_cd.yml booking config requirements.txt docs
git commit -m "Fix booking validation and configure CSC325 CI/CD"
git push -u origin feature/csc325-module8-cicd
gh pr create --draft --base main --head feature/csc325-module8-cicd \
  --title "Fix RoomBook backend and prepare CSC325 Module 8 CI/CD" \
  --body-file /workspace/roombook-pr-body.md
```

The PR body above was prepared in the current cloud workspace; copy it before
leaving this environment if you will record elsewhere. Do not merge during
preparation. The commands are provided for recording and have not been run.
