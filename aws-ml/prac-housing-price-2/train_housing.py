#!/usr/bin/env python3
"""
train_housing.py
Local end-to-end training for a realistic housing price regressor.
- Generates a semi-realistic dataset
- Trains a scikit-learn GradientBoostingRegressor in a Pipeline
- Evaluates and prints metrics
- Exports the model as model.joblib (not .pkl, per preference)
"""

import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

def main():
    out_dir = Path(".")
    rng = np.random.default_rng(42)
    n = 5000

    # --- Generate a semi-realistic housing dataset ---
    city_index = rng.integers(0, 5, size=n)
    bedrooms = rng.integers(1, 6, size=n)
    bathrooms = rng.integers(1, 5, size=n)
    sqft = rng.normal(1800, 600, size=n).clip(400, 6000)
    lot_size = rng.normal(5000, 2500, size=n).clip(800, 20000)
    year_built = rng.integers(1950, 2024, size=n)
    distance_to_center = rng.gamma(2.5, 2.0, size=n).clip(0.1, 40.0)
    school_rating = rng.normal(6.5, 1.5, size=n).clip(1, 10)
    crime_rate = rng.normal(40, 15, size=n).clip(5, 120)
    hoa_fee = rng.choice([0, 50, 100, 200, 300, 500], size=n, p=[0.35,0.2,0.18,0.15,0.08,0.04])

    city_base = np.array([320_000, 450_000, 600_000, 500_000, 380_000])
    city_mult = np.array([0.9, 1.1, 1.5, 1.2, 1.0])

    age = 2025 - year_built
    price = (
        city_base[city_index]
        + city_mult[city_index] * (sqft * 220 + bedrooms * 18_000 + bathrooms * 25_000)
        - np.log1p(distance_to_center) * 45_000
        + school_rating * 12_000
        - crime_rate * 800
        - age.clip(0, 100) * 1_000
        - hoa_fee * 50
        + rng.normal(0, 45_000, size=n)
    )

    # df of synthetic housing data
    housing_df = pd.DataFrame({
        "city_index": city_index,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "sqft": sqft,
        "lot_size": lot_size,
        "year_built": year_built,
        "distance_to_center": distance_to_center,
        "school_rating": school_rating,
        "crime_rate": crime_rate,
        "hoa_fee": hoa_fee,
        "price": price
    })
    housing_df.to_csv(out_dir / "housing_train.csv", index=False)

    # --- Train/test split ---
    X = housing_df.drop(columns=["price"])
    y = housing_df["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Pipeline: scale numeric features, fit GBR ---
    pipe = Pipeline([
        ("scaler", StandardScaler(with_mean=False)),
        ("gbr", GradientBoostingRegressor(random_state=42)),
    ])

    pipe.fit(X_train, y_train)

    # --- Evaluate ---
    y_pred = pipe.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Test MAE: {mae:,.2f}")
    print(f"Test R^2: {r2:.4f}")

    # --- Export model ---
    joblib.dump(pipe, out_dir / "housing_model.joblib")
    print("Saved model to housing_model.joblib")
    print("Saved training data to housing_train.csv")

    # --- Example inference ---
    sample = np.array([[0, 3, 2, 1600, 4500, 2001, 3.2, 7.5, 30, 100]])
    print("Sample prediction:", pipe.predict(sample).tolist())

if __name__ == "__main__":
    main()
