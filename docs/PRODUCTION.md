# Production Checklist — BiasLens

This document lists steps to move BiasLens from demo to production. Follow this checklist to ensure repeatable, auditable deployments.

Prerequisites
- CI passing (lint, types, tests)
- Docker images built and scanned
- Secrets stored in GitHub Secrets or secret manager

Deployment Steps
1. Configure environment secrets: `SECRET_KEY`, `DATABASE_PATH`, `FIREBASE_CREDENTIALS_JSON`, `NVIDIA_API_KEY` (optional).
2. Build and scan Docker images using the `build-and-push` workflow.
3. Deploy images to staging environment and run smoke tests (including `/health` and API endpoints).
4. Enable observability: structured logging, Prometheus metrics, tracing.
5. Run performance tests with representative datasets; validate resource limits and background job behavior.
6. Create a release tag and publish images and release notes.

Rollback
- Documented rollback steps should be added for each hosting platform.

Compliance
- Ensure dataset handling adheres to your organisation's PII/data retention policies.
