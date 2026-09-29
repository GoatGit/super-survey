# Security Policy

## Supported Versions

Super Survey is an agent skill distributed from the default branch. Only the latest revision on `main` receives security fixes.

| Version | Supported |
| --- | --- |
| `main` / latest | ✅ |
| older commits or tags | ❌ |

## Reporting a Vulnerability

Please report suspected vulnerabilities privately through [GitHub Security Advisories](https://github.com/GoatGit/super-survey/security/advisories/new) rather than a public issue. Include a description, affected files or commands, and reproduction steps. Maintainers respond as soon as practical and will credit reporters in the changelog unless anonymity is requested.

## Security Model

Super Survey is a local, standard-library-only Python CLI plus Markdown skill instructions. Its intended trust boundaries are:

- `scripts/survey_round.py` performs local filesystem reads/writes only. It makes no network requests and has no runtime dependencies beyond the Python standard library (3.9+).
- Survey artifacts (`surveys/`) are plain Markdown and JSONL files generated locally.
- Survey content routinely quotes third-party web pages, papers, and repository text. Skill instructions already require agents to treat all fetched third-party content as untrusted data: source-borne instructions, tool-use requests, credential requests, or workflow changes must be ignored, and only bounded factual excerpts may be stored.

## Out of Scope

The following reports are generally not treated as vulnerabilities:

- Prompt injection or misleading content inside third-party sources a user chooses to research; the skill's contract is to record and resist them, not to guarantee a perfect filter.
- Content produced by an agent that ignores the skill instructions or the host agent's own safety policy.
- Issues in host agent platforms, plugin runtimes, or other skills this project may route to.
- Social engineering of the human operator outside this repository's artifacts.

## Data Handling

Running a survey writes artifacts only inside the working directory you launch it from. Nothing is uploaded by this repository's scripts. Be mindful that report content can contain quotes from third-party sources and user-provided local files; share survey folders with the same care as any research notes.
