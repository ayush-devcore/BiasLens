# Security

This repository includes production guidance and a baseline security posture for BiasLens.

Key practices
- Do not commit secrets. Use GitHub Secrets and `.env` for local testing (`.env.example` provided).
- Pin critical dependencies in `requirements.txt` and perform regular vulnerability scans.
- Use least-privilege for service accounts (Firebase, cloud storage).
- Keep uploads in memory and avoid persistent storage for sensitive datasets; document retention policies.

CI Scans
- Trivy is configured to run a filesystem scan during CI. Any critical findings must be triaged before release.

Reporting
- Report security issues to the project owner via private channels. Do not open public issues with sensitive details.
