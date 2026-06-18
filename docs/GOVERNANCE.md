# Governance & Model Metadata

Recommendations:
- Track model and dataset metadata (use MLflow or a simple metadata store).
- Record model version, training data snapshot, metrics, and mitigation strategies applied.
- Maintain an approvals process for releases that impact production models.

Suggested minimal metadata fields:
- model_name, version, git_sha, training_dataset_id, features_hash, mitigation_applied, fairness_score, created_at
