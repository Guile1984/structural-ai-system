"""
Módulo: ml/pipeline.py
Descrição: Pipeline completo de treino, serialização e previsão de modelos ML
"""

import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

ARTIFACTS_DIR = Path("ml/artifacts")
DATA_DIR = Path("data")
APPROVAL_THRESHOLD = 5000


def generate_dataset(n: int = 500) -> pd.DataFrame:
    """Gera daset sintético de elementos estruturais.

    Args:
        n: Número de amostras a gerar.

    Returns:
        DataFrame com elementos estruturais.
    Nota:
        Em produção, os dados viriam de um banco de dados ou API externa.
        O dataset sintético simula esse cenário de forma controlada.
    """
    np.random.seed(42)
    types = np.random.choice(["Beam", "Column", "Slab", "Footing"], n)
    materials = np.random.choice(["concrete", "steel"], n)
    lengths = np.random.uniform(1.0, 10.0, n).round(2)
    widths = np.random.uniform(0.2, 1.0, n).round(2)
    heights = np.random.uniform(0.1, 0.6, n).round(2)
    volumes = (lengths * widths * heights).round(3)
    densities = np.where(materials == "concrete", 2500.0, 7850.0)
    masses = (volumes * densities).round(1)
    approved = (masses < APPROVAL_THRESHOLD).astype(int)

    return pd.DataFrame(
        {
            "type": types,
            "material": materials,
            "length": lengths,
            "width": widths,
            "height": heights,
            "volume": volumes,
            "mass_kg": masses,
            "approved": approved,
        }
    )


def prepare_features(df: pd.DataFrame) -> dict:
    """Prepara features, targets, scaler e encoders.

    Args:
        df: DataFrame com dados brutos.

    Returns:
        Dicionário com X_scaled, targets, scaler e encoders.
    """
    df = df.copy()

    le_material = LabelEncoder()
    le_type = LabelEncoder()
    df["material_enc"] = le_material.fit_transform(df["material"])
    df["type_enc"] = le_type.fit_transform(df["type"])

    feature_names = ["length", "width", "height", "volume", "material_enc", "type_enc"]
    X = df[feature_names].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return {
        "X": X_scaled,
        "y_mass": df["mass_kg"].values,
        "y_approval": df["approved"].values,
        "scaler": scaler,
        "encoders": {"material": le_material, "type": le_type, "feature_names": feature_names},
    }


def train_regression(
    X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray
) -> dict:
    """
    Treina o modelo de regressão para prever massa.

    Args:
        X_train: Features de treino.
        y_train: Target de treino.
        X_test: Features de teste.
        y_test: Target de teste.

    Returns:
        Dicionário com modelo treinado e métricas.
    """
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="r2")

    metrics = {
        "mae": round(mean_absolute_error(y_test, y_pred), 2),
        "r2": round(r2_score(y_test, y_pred), 4),
        "cv_mean": round(cv_scores.mean(), 4),
        "cv_std": round(cv_scores.std(), 4),
        "cv_scores": cv_scores.tolist(),
    }

    print(f"    [Regression] MAE: {metrics['mae']} kg | R²: {metrics['r2']}")
    print(f"                 CV R² mean: {metrics['cv_mean']} ± {metrics['cv_std']}")

    return {"model": model, "metrics": metrics}


def train_classification(
    X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray
) -> dict:
    """
    Treina modelo de classificação para prever aprovação.

    Args:
        X_train: Features de treino.
        y_train: Target de treino.
        X_test: Features de teste.
        y_test: Target de teste.

    Returns:
        Dicionário com modelo treinado e métricas.
    """
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "cv_mean": round(cv_scores.mean(), 4),
        "cv_std": round(cv_scores.mean(), 4),
        "cv_scores": cv_scores.tolist(),
        "report": classification_report(
            y_test, y_pred, target_names=["Rejected", "Approved"], output_dict=True
        ),
    }

    print(f"    [Classification] Accuracy: {metrics['accuracy']}")
    print(f"                     CV Accuracy mean: {metrics['cv_mean']} ± {metrics['cv_std']}")

    return {"model": model, "metrics": metrics}


def save_artifacts(scaler, encoders, regression, classfication) -> None:
    """Serializa todos os artefatos do pipeline para disco.

    Args:
        scaler: StandardScaler treinado.
        encoders: Dicionário com LabelEncoders e feature_names.
        regression: Resultado do treino de regressão.
        classification: Resultado do treino de classificação.
    """
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    artifacts = {
        "scaler.pkl": scaler,
        "encoders.pkl": encoders,
        "model_regression.pkl": regression,
        "model_classification.pkl": classfication,
    }

    for filename, artifact in artifacts.items():
        with open(ARTIFACTS_DIR / filename, "wb") as f:
            pickle.dump(artifact, f)
        print(f"  Saved: {filename}")


def load_artifacts() -> dict:
    """Carrega todos os artefatos do pipeline do disco.

    Returns:
        Dicinário com scaler, encoder, regressão e classificação.

    Raises:
        FileNotFoundError: Se os artefatos não existirem.
    """
    files = ["scaler.pkl", "encoders.pkl", "model_regression.pkl", "model_classification.pkl"]

    for f in files:
        if not (ARTIFACTS_DIR / f).exists():
            raise FileNotFoundError(
                f"Artifact '{f}' not found. Run 'python main.py --train' first."
            )

    artifacts = {}
    for f in files:
        with open(ARTIFACTS_DIR / f, "rb") as file:
            key = f.replace(".pkl", "")
            artifacts[key] = pickle.load(file)

    return artifacts


def predict_mass(dimensions: dict, artifacts: dict) -> dict:
    """Prevê a massa de um elemento estrutural.

    Args:
        dimensions: Dicionário com type, material, length, width, height.
        artifacts: Dicionário com artefatos carregados.

    Returns:
        Dicionário com previsão e metadados.
    """
    element_type = dimensions["type"]
    material = dimensions["material"]
    length = float(dimensions["length"])
    width = float(dimensions["width"])
    height = float(dimensions["height"])

    scaler = artifacts["scaler"]
    encoders = artifacts["encoders"]
    model = artifacts["model_regression"]["model"]

    volume = round(length * width * height, 3)
    material_enc = encoders["material"].transform([material])[0]
    type_enc = encoders["type"].transform([element_type])[0]

    X = np.array([[length, width, height, volume, material_enc, type_enc]])
    X_scaled = scaler.transform(X)
    predicted_mass = model.predict(X_scaled)[0]

    calculated_mass = round(volume * (2500.0 if material == "concrete" else 7850.0), 2)

    return {
        "type": element_type,
        "material": material,
        "dimensions": {"length": length, "width": width, "height": height},
        "volume_m3": volume,
        "predicted_mass_kg": round(predicted_mass, 2),
        "calculated_mass_kg": calculated_mass,
        "error_kg": round(abs(predicted_mass - calculated_mass), 2),
        "model_r2": artifacts["model_regression"]["metrics"]["r2"],
    }


def predict_approval(dimensions: dict, artifacts: dict) -> dict:
    """PrevÊ se um elemento será aprovado.

    Args:
        dimensions: Dicionário com type, material, length, width, height.
        artifacts: Dicionário com artefatos carregados.
    Returns:
        Dicionário com previsão e probabilidades.
    """
    element_type = dimensions["type"]
    material = dimensions["material"]
    length = float(dimensions["length"])
    width = float(dimensions["width"])
    height = float(dimensions["height"])

    scaler = artifacts["scaler"]
    encoders = artifacts["encoders"]
    model = artifacts["model_classification"]["model"]

    volume = round(length * width * height, 3)
    material_enc = encoders["material"].transform([material])[0]
    type_enc = encoders["type"].transform([element_type])[0]

    X = np.array([[length, width, height, volume, material_enc, type_enc]])
    X_scaled = scaler.transform(X)

    prediction = model.predict(X_scaled)[0]
    probabilities = model.predict_proba(X_scaled)[0]

    return {
        "type": element_type,
        "material": material,
        "dimensions": {"length": length, "width": width, "height": height},
        "volume_m3": volume,
        "approved": bool(prediction),
        "status": "Approved" if prediction == 1 else "Rejected",
        "confidence": {
            "rejected": round(probabilities[0] * 100, 1),
            "approved": round(probabilities[1] * 100, 1),
        },
        "model_accuracy": artifacts['model_classification']["metrics"]["accuracy"],
    }


def train_pipeline() -> None:
    """Executa o pipeline completo de treino.

    Gera dataset, prepara features, treina modelos e salva artefatos.
    """
    print("=" * 50)
    print("STRUCTURAL AI - TRAINING PIPELINE")
    print("=" * 50)

    print("\n1. Generating dataset...")
    df = generate_dataset(500)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_DIR / "elements.csv", index=False)
    print(f"   {len(df)} samples generated and saved.")

    print("\n2. Preparing features...")
    prepared = prepare_features(df)
    X = prepared["X"]
    y_mass = prepared["y_mass"]
    y_approval = prepared["y_approval"]

    X_tr, X_te, ym_tr, ym_te = train_test_split(X, y_mass, test_size=0.2, random_state=42)
    _, _, ya_tr, ya_te = train_test_split(X, y_approval, test_size=0.2, random_state=42)
    print(f"    Train: {len(X_tr)} | Test: {len(X_te)}")

    print("\n3. Training regression model...")
    regression = train_regression(X_tr, ym_tr, X_te, ym_te)

    print("\n4. Training classificatio model...")
    classification = train_classification(X_tr, ya_tr, X_te, ya_te)

    print("\n5. Saving artifacts...")
    save_artifacts(prepared["scaler"], prepared["encoders"], regression, classification)

    print("\n" + "=" * 50)
    print("TRAINING COMPLETE")
    print("=" * 50)
