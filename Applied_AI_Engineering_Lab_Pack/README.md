# Applied AI Engineering: 24 weeks / 48 labs

Start with COURSE.md or the separate PDF. Python 3.12 was used for offline validation.
The offline workbench needs no packages, account, network, GPU, or API keys.

## Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe demo.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
$env:COURSE_IMPL = "student"
.\.venv\Scripts\python.exe -m unittest tests.test_core.Foundation -v
Remove-Item Env:COURSE_IMPL
```
## macOS/Linux
```bash
python3 -m venv .venv
.venv/bin/python demo.py
.venv/bin/python -m unittest discover -s tests -v
COURSE_IMPL=student .venv/bin/python -m unittest tests.test_core.Foundation -v
```
Reference mode is the default. Student mode imports labs/exercises.py, whose
NotImplementedError failures are intentional. Complete one function at a time.
Run from this folder, not its parent. Test groups: Foundation, SQL, Context,
Retrieval, Agent, Persistence, Operations. Persistence uses the supplied reference
function in both modes, as a demonstration for week 17.

## Contents and scope
- COURSE.md: all 24 lessons, 48 lab briefs, guidance, pass criteria, solution notes.
- labs/exercises.py: 14 unfinished functions for selected offline labs.
- solutions/core.py: worked answers and synthetic SQLite setup.
- tests/test_core.py: behavior and failure-case checks for the offline workbench.
- demo.py and data/: deterministic demonstration and synthetic documents.
- integrations/: optional starting code, not a finished capstone.
- INTEGRATIONS.md: install/run instructions, live-lab boundaries and version policy.
- Dockerfile: teaching API container recipe; build locally as the week-19 lab.
- lab_journal.md: reproducible lab report template.

Do not represent the simulated agent, lexical retrieval, or invented model prices
as live AI, semantic search, or real provider pricing. Use the later labs to extend
the reference system. The teaching API has no authentication and synthetic data
only; add real identity and scope enforcement before a private pilot uses real data.

## Full-video alignment
COURSE.md includes a full-transcript review of the supplied Sajjaad Khader video,
a timestamp-to-course map, a file-summary addition to Lab 08A, and four optional
advanced extensions (outside the 48 core labs): multi-agent comparison, reviewable
developer automation, a tiny language model, and model optimization experiments.

Offline mini-project:
```text
python -m integrations.summarize_file data/notes.txt --provider fake
```
Use your virtual-environment Python in place of python. Fake mode tests plumbing
only; it explicitly does not generate a summary. Live mode uses the optional SDKs.
