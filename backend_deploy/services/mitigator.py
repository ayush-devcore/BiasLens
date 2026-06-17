from typing import List, Tuple, Dict, Any, Optional
from models.schemas import MitigationStrategy, MetricResult, SeverityLevel, BiasIssue
import uuid
import pandas as pd
import numpy as np


ALL_STRATEGIES = [
    MitigationStrategy(
        id="mit_reweighing",
        title="Reweighing",
        stage="Pre-processing",
        description=(
            "Assigns different weights to training samples based on group membership and label. "
            "Increases the influence of underrepresented combinations without modifying data. "
            "Simple, effective, and interpretable. Best first step for most datasets."
        ),
        implementation="IBM AIF360 — Reweighing transformer",
        effort="Low",
        impact="High",
        library="aif360",
        code_snippet="""from aif360.algorithms.preprocessing import Reweighing
from aif360.datasets import BinaryLabelDataset

# Wrap your dataframe
dataset = BinaryLabelDataset(
    df=df,
    label_names=['label'],
    protected_attribute_names=['gender', 'race']
)

# Apply reweighing
rw = Reweighing(
    unprivileged_groups=[{'gender': 0}],
    privileged_groups=[{'gender': 1}]
)
dataset_transformed = rw.fit_transform(dataset)
df_reweighed = dataset_transformed.convert_to_dataframe()[0]
"""
    ),
    MitigationStrategy(
        id="mit_adversarial",
        title="Adversarial Debiasing",
        stage="In-processing",
        description=(
            "Trains a classifier alongside an adversarial network that tries to predict "
            "sensitive attributes from predictions. The main model learns to be both accurate "
            "and fair simultaneously. Best for deep learning pipelines."
        ),
        implementation="IBM AIF360 — AdversarialDebiasing",
        effort="High",
        impact="High",
        library="aif360",
        code_snippet="""import tensorflow as tf
from aif360.algorithms.inprocessing import AdversarialDebiasing
from aif360.datasets import BinaryLabelDataset

sess = tf.Session()
debiased_model = AdversarialDebiasing(
    privileged_groups=[{'gender': 1}],
    unprivileged_groups=[{'gender': 0}],
    scope_name='debiased_classifier',
    debias=True,
    sess=sess
)

debiased_model.fit(train_dataset)
predictions = debiased_model.predict(test_dataset)
"""
    ),
    MitigationStrategy(
        id="mit_eqodds",
        title="Calibrated Equalized Odds",
        stage="Post-processing",
        description=(
            "Adjusts prediction thresholds independently per demographic group after training "
            "to equalize true positive and false positive rates. Does not require retraining. "
            "Best when you already have a trained model and want to fix it."
        ),
        implementation="IBM AIF360 — CalibratedEqOddsPostprocessing",
        effort="Medium",
        impact="High",
        library="aif360",
        code_snippet="""from aif360.algorithms.postprocessing import CalibratedEqOddsPostprocessing

cpp = CalibratedEqOddsPostprocessing(
    privileged_groups=[{'race': 1}],
    unprivileged_groups=[{'race': 0}],
    cost_constraint='fnr',  # or 'fpr', 'weighted'
    seed=42
)

cpp = cpp.fit(val_dataset, val_predictions)
test_predictions_fair = cpp.predict(test_predictions)
"""
    ),
    MitigationStrategy(
        id="mit_prejudice_remover",
        title="Prejudice Remover Regularizer",
        stage="In-processing",
        description=(
            "Adds a fairness-aware regularization term to the learning objective. "
            "Penalizes the model when its predictions are correlated with sensitive attributes. "
            "Works with logistic regression and similar models."
        ),
        implementation="IBM AIF360 — PrejudiceRemover",
        effort="Medium",
        impact="Medium",
        library="aif360",
        code_snippet="""from aif360.algorithms.inprocessing import PrejudiceRemover

model = PrejudiceRemover(
    eta=25.0,           # fairness penalty strength
    sensitive_attr='gender',
    class_attr='label'
)

model.fit(train_dataset)
predictions = model.predict(test_dataset)
"""
    ),
    MitigationStrategy(
        id="mit_fairlearn_reduction",
        title="Fairlearn Exponentiated Gradient",
        stage="In-processing",
        description=(
            "Reduces fair classification to a sequence of cost-sensitive classification problems. "
            "Finds the best trade-off between accuracy and fairness using Lagrange multipliers. "
            "Works with any scikit-learn compatible classifier."
        ),
        implementation="Microsoft Fairlearn — ExponentiatedGradient",
        effort="Medium",
        impact="High",
        library="fairlearn",
        code_snippet="""from fairlearn.reductions import ExponentiatedGradient, DemographicParity
from sklearn.tree import DecisionTreeClassifier

estimator = DecisionTreeClassifier(max_depth=4)
constraint = DemographicParity()

mitigator = ExponentiatedGradient(estimator, constraint)
mitigator.fit(X_train, y_train, sensitive_features=A_train)

y_pred = mitigator.predict(X_test)
"""
    ),
    MitigationStrategy(
        id="mit_proxy_removal",
        title="Remove Proxy Variables",
        stage="Pre-processing",
        description=(
            "Drops or transforms feature columns that are highly correlated with sensitive attributes. "
            "Proxy variables like 'Zip Code' can encode racial information and enable "
            "indirect discrimination even when protected attributes are excluded."
        ),
        implementation="Custom preprocessing — pandas",
        effort="Low",
        impact="Medium",
        library="pandas",
        code_snippet="""import pandas as pd
from scipy.stats import pearsonr

def remove_proxies(df, sensitive_attrs, threshold=0.70):
    proxy_cols = []
    for col in df.columns:
        if col in sensitive_attrs:
            continue
        for s in sensitive_attrs:
            try:
                corr, _ = pearsonr(df[col].fillna(0), df[s].fillna(0))
                if abs(corr) >= threshold:
                    proxy_cols.append(col)
                    print(f"Removing proxy: {col} (r={corr:.2f} with {s})")
            except:
                pass
    return df.drop(columns=list(set(proxy_cols)))

df_clean = remove_proxies(df, ['gender', 'race'])
"""
    ),
    MitigationStrategy(
        id="mit_resampling",
        title="Stratified Resampling",
        stage="Pre-processing",
        description=(
            "Balances the training dataset by oversampling underrepresented groups "
            "or undersampling overrepresented ones. Addresses historical bias where "
            "minority groups are severely underrepresented."
        ),
        implementation="imbalanced-learn — SMOTE + Custom Stratification",
        effort="Low",
        impact="Medium",
        library="imbalanced-learn",
        code_snippet="""from imblearn.over_sampling import SMOTE
from sklearn.model_selection import StratifiedKFold

# SMOTE for numeric features
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Or custom group-based resampling
def group_resample(df, sensitive_attr, label_col, strategy='oversample'):
    groups = df[sensitive_attr].unique()
    max_size = df[sensitive_attr].value_counts().max()
    resampled = []
    for g in groups:
        group_df = df[df[sensitive_attr] == g]
        if strategy == 'oversample' and len(group_df) < max_size:
            group_df = group_df.sample(max_size, replace=True, random_state=42)
        resampled.append(group_df)
    return pd.concat(resampled).sample(frac=1, random_state=42)
"""
    ),
    MitigationStrategy(
        id="mit_threshold_opt",
        title="Threshold Optimization",
        stage="Post-processing",
        description=(
            "Finds optimal decision thresholds per group to satisfy fairness constraints. "
            "The fastest post-hoc fix — requires no retraining and works with any "
            "existing model that outputs probabilities."
        ),
        implementation="Microsoft Fairlearn — ThresholdOptimizer",
        effort="Low",
        impact="Medium",
        library="fairlearn",
        code_snippet="""from fairlearn.postprocessing import ThresholdOptimizer
from sklearn.ensemble import RandomForestClassifier

# Train your base model first
base_model = RandomForestClassifier(n_estimators=100, random_state=42)
base_model.fit(X_train, y_train)

# Apply threshold optimization
optimizer = ThresholdOptimizer(
    estimator=base_model,
    constraints="equalized_odds",   # or "demographic_parity"
    predict_method="predict_proba",
    objective="balanced_accuracy_score"
)

optimizer.fit(X_train, y_train, sensitive_features=A_train)
y_pred_fair = optimizer.predict(X_test, sensitive_features=A_test)
"""
    ),
]


def get_relevant_strategies(issues: List[BiasIssue]) -> List[MitigationStrategy]:
    """Return strategies most relevant to the detected issues."""
    has_proxy = any("proxy" in i.title.lower() for i in issues)
    has_critical = any(i.severity == SeverityLevel.CRITICAL for i in issues)
    has_disparate_impact = any("disparate impact" in i.title.lower() for i in issues)
    has_equal_opp = any("equal opportunity" in i.title.lower() for i in issues)

    # Always include the top strategies
    always_include = {"mit_reweighing", "mit_eqodds", "mit_fairlearn_reduction", "mit_threshold_opt"}

    # Conditionally include
    if has_proxy:
        always_include.add("mit_proxy_removal")
    if has_critical:
        always_include.add("mit_adversarial")
        always_include.add("mit_resampling")
    if has_equal_opp:
        always_include.add("mit_prejudice_remover")

    return [s for s in ALL_STRATEGIES if s.id in always_include]


# ── ACTUAL MITIGATION LOGIC ──────────────────────────────────────────────────

def apply_mitigation(
    df: pd.DataFrame,
    strategy_id: str,
    label_col: str,
    sensitive_attrs: List[str],
    positive_label: Any = 1
) -> Tuple[pd.DataFrame, str]:
    """
    Applies the actual data transformation for the chosen strategy.
    Returns: (Transformed DataFrame, Description of what was done)
    """
    # FIX 1: Empty check moved to top — before any logic runs
    if df.empty:
        raise ValueError("Dataset is empty")

    if strategy_id == "mit_proxy_removal":
        from .metrics import detect_proxy_variables
        proxies = detect_proxy_variables(df, sensitive_attrs, label_col, threshold=0.55)
        cols_to_drop = list(set([p.column for p in proxies]))
        if not cols_to_drop:
            return df, "No proxy variables met the correlation threshold for removal."
        df_new = df.drop(columns=cols_to_drop)
        return df_new, f"Removed {len(cols_to_drop)} proxy variables: {', '.join(cols_to_drop)}."

    # FIX 2: Changed all standalone `if` blocks to `elif` so the final `else`
    # is reachable for ALL unmatched strategy_ids, not just after mit_reweighing.
    elif strategy_id == "mit_resampling":
        # Stratified Resampling (Simplified: Oversampling minority groups)
        df_new = df.copy()
        if not sensitive_attrs:
            return df, "No sensitive attributes provided for resampling."
        
        # We'll balance on the first sensitive attribute for now
        attr = sensitive_attrs[0]
        max_size = df_new[attr].value_counts().max()
        groups = []
        for g in df_new[attr].unique():
            group_df = df_new[df_new[attr] == g]
            if len(group_df) < max_size:
                # Oversample minority group
                upsampled = group_df.sample(max_size, replace=True, random_state=42)
                groups.append(upsampled)
            else:
                groups.append(group_df)
        df_balanced = pd.concat(groups).sample(frac=1, random_state=42).reset_index(drop=True)
        return df_balanced, f"Applied stratified resampling to balance groups in '{attr}'."

    elif strategy_id == "mit_reweighing":
        # For a live audit, we implement Reweighing as a selective resampling 
        # to simulate the effect of weights on the distributions.
        # (True reweighing requires the metric functions to support weight params)
        df_new = df.copy()
        attr = sensitive_attrs[0] if sensitive_attrs else None
        if not attr:
            return df, "No sensitive attributes for reweighing."
        
        # Calculate ideal probability (Statistical Parity)
        total_pos = (df_new[label_col] == positive_label).sum()
        total_records = len(df_new)
        ideal_rate = total_pos / total_records
        
        groups = []
        for g in df_new[attr].unique():
            group_df = df_new[df_new[attr] == g]
            pos_mask = group_df[label_col] == positive_label
            neg_mask = ~pos_mask
            
            # Simple balancing: adjust pos/neg ratio to match ideal rate
            # This is a heuristic to "fix" the disparate impact visually
            n_pos = int(len(group_df) * ideal_rate)
            n_neg = len(group_df) - n_pos
            
            if n_pos > 0 and pos_mask.any():
                df_pos = group_df[pos_mask].sample(n_pos, replace=True, random_state=42)
            else:
                df_pos = group_df[pos_mask]
                
            if n_neg > 0 and neg_mask.any():
                df_neg = group_df[neg_mask].sample(n_neg, replace=True, random_state=42)
            else:
                df_neg = group_df[neg_mask]
                
            groups.append(pd.concat([df_pos, df_neg]))
            
        df_reweighed = pd.concat(groups).sample(frac=1, random_state=42).reset_index(drop=True)
        return df_reweighed, f"Simulated reweighing by adjusting outcome distributions across '{attr}' groups."

    else:
        raise ValueError(
            f"Unsupported mitigation strategy: {strategy_id}"
        )