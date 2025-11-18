---
name: Advanced Data Science Expert
description: Implements machine learning, predictive modeling, and AI-driven solutions for real estate forecasting, optimization, and automation
---

# Advanced Data Science Expert

## Overview

This skill enables Claude to apply advanced machine learning, artificial intelligence, and predictive modeling techniques to real estate problems. It focuses on building robust, production-ready models that deliver measurable business value.

## When to Use This Skill

Invoke this skill when:
- Building predictive models (price prediction, occupancy forecasting, churn prediction)
- Implementing machine learning solutions
- Optimizing business processes using algorithms
- Creating recommendation systems
- Performing time series forecasting
- Developing classification or clustering models
- Implementing natural language processing for real estate documents
- Automating decision-making processes
- Building proptech AI features

## Core Data Science Capabilities

### 1. Predictive Modeling

**Regression Models:**
```python
# Property Price Prediction Model
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge, Lasso
import xgboost as xgb

class PropertyPricePredictor:
    """
    Advanced property price prediction using ensemble methods
    """

    def __init__(self):
        self.models = {
            'xgboost': xgb.XGBRegressor(
                n_estimators=200,
                max_depth=7,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=150,
                max_depth=5,
                learning_rate=0.1
            ),
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5
            )
        }
        self.ensemble_weights = {'xgboost': 0.5, 'gradient_boosting': 0.3, 'random_forest': 0.2}

    def create_features(self, df):
        """
        Feature engineering for property pricing
        """
        features = df.copy()

        # Basic features
        features['price_per_sqft'] = features['price'] / features['sqft']
        features['age'] = 2025 - features['year_built']

        # Location features
        features['location_avg_price'] = features.groupby('location')['price'].transform('mean')
        features['location_price_ratio'] = features['price'] / features['location_avg_price']

        # Market features
        features['cap_rate'] = features['noi'] / features['price']
        features['rent_to_price_ratio'] = (features['monthly_rent'] * 12) / features['price']

        # Temporal features
        features['year'] = features['sale_date'].dt.year
        features['quarter'] = features['sale_date'].dt.quarter
        features['month'] = features['sale_date'].dt.month

        # Interaction features
        features['sqft_x_age'] = features['sqft'] * features['age']
        features['units_x_occupancy'] = features['units'] * features['occupancy_rate']

        return features

    def train(self, X_train, y_train, X_val, y_val):
        """
        Train ensemble of models with validation
        """
        predictions = {}

        for name, model in self.models.items():
            model.fit(X_train, y_train)
            val_pred = model.predict(X_val)
            predictions[name] = val_pred

            # Calculate metrics
            from sklearn.metrics import mean_absolute_error, r2_score
            mae = mean_absolute_error(y_val, val_pred)
            r2 = r2_score(y_val, val_pred)

            print(f"{name}: MAE=${mae:,.0f}, R²={r2:.4f}")

        return predictions

    def predict(self, X):
        """
        Ensemble prediction with confidence intervals
        """
        predictions = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(X)

        # Weighted ensemble
        ensemble_pred = sum(
            predictions[name] * weight
            for name, weight in self.ensemble_weights.items()
        )

        # Prediction intervals (using std of individual models)
        pred_std = np.std([predictions[name] for name in self.models.keys()], axis=0)
        lower_bound = ensemble_pred - 1.96 * pred_std
        upper_bound = ensemble_pred + 1.96 * pred_std

        return {
            'prediction': ensemble_pred,
            'lower_95': lower_bound,
            'upper_95': upper_bound,
            'individual_predictions': predictions
        }
```

**Classification Models:**
```python
# Tenant Churn Prediction
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

class TenantChurnPredictor:
    """
    Predict probability of tenant not renewing lease
    """

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=8,
            min_samples_split=10,
            class_weight='balanced'  # Handle imbalanced classes
        )

    def create_features(self, tenant_df):
        """
        Feature engineering for churn prediction
        """
        features = tenant_df.copy()

        # Lease features
        features['months_in_lease'] = (
            pd.to_datetime('today') - features['lease_start_date']
        ).dt.days / 30
        features['months_until_expiry'] = (
            features['lease_end_date'] - pd.to_datetime('today')
        ).dt.days / 30

        # Payment behavior
        features['late_payment_rate'] = features['late_payments'] / features['total_payments']
        features['avg_days_late'] = features['total_days_late'] / features['late_payments'].fillna(1)

        # Maintenance requests
        features['maintenance_requests_per_month'] = (
            features['maintenance_requests'] / features['months_in_lease']
        )
        features['unresolved_requests'] = features['open_maintenance_requests']

        # Market features
        features['rent_vs_market'] = features['current_rent'] / features['market_rent']
        features['rent_increase_pct'] = (
            (features['current_rent'] - features['initial_rent']) / features['initial_rent']
        )

        # Engagement features
        features['portal_login_frequency'] = features['portal_logins'] / features['months_in_lease']
        features['days_since_last_contact'] = (
            pd.to_datetime('today') - features['last_contact_date']
        ).dt.days

        return features

    def train_and_evaluate(self, X_train, y_train, X_test, y_test):
        """
        Train model and provide detailed evaluation
        """
        self.model.fit(X_train, y_train)

        # Predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]

        # Evaluation metrics
        print(classification_report(y_test, y_pred))
        print(f"ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        return feature_importance
```

### 2. Time Series Forecasting

**Advanced Forecasting Methods:**
```python
# Multi-step Time Series Forecasting
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
import tensorflow as tf
from tensorflow import keras

class RentForecastingSystem:
    """
    Advanced rental rate forecasting using multiple methods
    """

    def prophet_forecast(self, historical_data, periods=12):
        """
        Facebook Prophet for trend and seasonality
        """
        df = historical_data.rename(columns={'date': 'ds', 'rent': 'y'})

        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.05
        )

        # Add custom seasonality
        model.add_seasonality(name='quarterly', period=91.25, fourier_order=5)

        # Add regressors (e.g., economic indicators)
        model.add_regressor('employment_rate')
        model.add_regressor('interest_rate')

        model.fit(df)

        future = model.make_future_dataframe(periods=periods, freq='M')
        forecast = model.predict(future)

        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    def sarima_forecast(self, historical_data, periods=12):
        """
        SARIMA for seasonal time series
        """
        model = SARIMAX(
            historical_data['rent'],
            order=(1, 1, 1),          # (p, d, q)
            seasonal_order=(1, 1, 1, 12),  # (P, D, Q, s) - monthly seasonality
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        results = model.fit(disp=False)
        forecast = results.forecast(steps=periods)

        # Confidence intervals
        forecast_conf = results.get_forecast(steps=periods)
        conf_int = forecast_conf.conf_int()

        return {
            'forecast': forecast,
            'lower': conf_int.iloc[:, 0],
            'upper': conf_int.iloc[:, 1]
        }

    def lstm_forecast(self, historical_data, sequence_length=12, periods=12):
        """
        LSTM neural network for complex patterns
        """
        # Prepare sequences
        def create_sequences(data, seq_length):
            X, y = [], []
            for i in range(len(data) - seq_length):
                X.append(data[i:i+seq_length])
                y.append(data[i+seq_length])
            return np.array(X), np.array(y)

        # Normalize data
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(historical_data['rent'].values.reshape(-1, 1))

        X, y = create_sequences(scaled_data, sequence_length)

        # Build LSTM model
        model = keras.Sequential([
            keras.layers.LSTM(64, activation='relu', input_shape=(sequence_length, 1), return_sequences=True),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(32, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1)
        ])

        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        model.fit(X, y, epochs=100, batch_size=32, validation_split=0.2, verbose=0)

        # Multi-step forecast
        forecasts = []
        last_sequence = scaled_data[-sequence_length:]

        for _ in range(periods):
            pred = model.predict(last_sequence.reshape(1, sequence_length, 1), verbose=0)
            forecasts.append(pred[0, 0])
            last_sequence = np.append(last_sequence[1:], pred)

        # Inverse transform
        forecasts = scaler.inverse_transform(np.array(forecasts).reshape(-1, 1))

        return forecasts.flatten()

    def ensemble_forecast(self, historical_data, periods=12):
        """
        Combine multiple forecasting methods
        """
        prophet_pred = self.prophet_forecast(historical_data, periods)
        sarima_pred = self.sarima_forecast(historical_data, periods)
        lstm_pred = self.lstm_forecast(historical_data, periods)

        # Weighted average (weights based on historical accuracy)
        ensemble = (
            0.4 * prophet_pred['yhat'].values[-periods:] +
            0.3 * sarima_pred['forecast'].values +
            0.3 * lstm_pred
        )

        return ensemble
```

### 3. Clustering and Segmentation

```python
# Property Clustering for Market Segmentation
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class PropertySegmentation:
    """
    Intelligent property clustering and segmentation
    """

    def optimal_clusters(self, X, max_k=10):
        """
        Determine optimal number of clusters using elbow method and silhouette score
        """
        from sklearn.metrics import silhouette_score

        inertias = []
        silhouette_scores = []

        for k in range(2, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X, kmeans.labels_))

        # Find elbow point
        from kneed import KneeLocator
        kl = KneeLocator(range(2, max_k + 1), inertias, curve='convex', direction='decreasing')

        return {
            'elbow_k': kl.elbow,
            'best_silhouette_k': np.argmax(silhouette_scores) + 2,
            'inertias': inertias,
            'silhouette_scores': silhouette_scores
        }

    def segment_properties(self, property_df, n_clusters=5):
        """
        Segment properties based on characteristics and performance
        """
        # Select features for clustering
        features = [
            'price', 'sqft', 'cap_rate', 'occupancy_rate',
            'noi', 'age', 'units', 'market_rent_growth'
        ]

        X = property_df[features].fillna(property_df[features].median())

        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Apply K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
        property_df['segment'] = kmeans.fit_predict(X_scaled)

        # Analyze segments
        segment_profiles = property_df.groupby('segment').agg({
            'price': ['mean', 'median', 'count'],
            'cap_rate': 'mean',
            'occupancy_rate': 'mean',
            'noi': 'mean'
        }).round(2)

        # Name segments based on characteristics
        segment_names = self._name_segments(segment_profiles)

        return {
            'assignments': property_df['segment'],
            'profiles': segment_profiles,
            'names': segment_names,
            'centers': scaler.inverse_transform(kmeans.cluster_centers_)
        }

    def _name_segments(self, profiles):
        """
        Generate meaningful segment names
        """
        names = {}
        for idx in profiles.index:
            profile = profiles.loc[idx]
            cap_rate = profile[('cap_rate', 'mean')]
            occupancy = profile[('occupancy_rate', 'mean')]
            price = profile[('price', 'mean')]

            if cap_rate > 0.08 and occupancy > 0.9:
                names[idx] = "High-Yield Performers"
            elif price > 1000000 and occupancy > 0.85:
                names[idx] = "Premium Assets"
            elif occupancy < 0.7:
                names[idx] = "Value-Add Opportunities"
            elif cap_rate < 0.05:
                names[idx] = "Core Investments"
            else:
                names[idx] = f"Segment {idx}"

        return names
```

### 4. Recommendation Systems

```python
# Property Recommendation Engine
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

class PropertyRecommender:
    """
    Collaborative and content-based recommendation system
    """

    def content_based_recommendations(self, property_id, property_df, n_recommendations=5):
        """
        Recommend similar properties based on features
        """
        # Select features for similarity
        feature_cols = [
            'price', 'sqft', 'bedrooms', 'bathrooms', 'cap_rate',
            'location_encoded', 'property_type_encoded'
        ]

        # Normalize features
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        feature_matrix = scaler.fit_transform(property_df[feature_cols])

        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(feature_matrix)

        # Get property index
        idx = property_df[property_df['id'] == property_id].index[0]

        # Get similarity scores
        sim_scores = list(enumerate(similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get top N (excluding the property itself)
        recommendations = sim_scores[1:n_recommendations + 1]

        return property_df.iloc[[i[0] for i in recommendations]]

    def collaborative_filtering(self, user_id, user_property_matrix, n_recommendations=5):
        """
        Recommend based on user behavior patterns
        """
        # Use matrix factorization (SVD)
        from scipy.sparse.linalg import svds

        # Sparse matrix of user-property interactions
        sparse_matrix = csr_matrix(user_property_matrix.values)

        # SVD
        U, sigma, Vt = svds(sparse_matrix, k=20)

        # Reconstruct ratings
        sigma = np.diag(sigma)
        predicted_ratings = np.dot(np.dot(U, sigma), Vt)

        # Get predictions for user
        user_idx = user_property_matrix.index.get_loc(user_id)
        user_predictions = predicted_ratings[user_idx, :]

        # Get top unrated properties
        rated_properties = user_property_matrix.loc[user_id] > 0
        user_predictions[rated_properties] = -np.inf

        top_indices = np.argsort(user_predictions)[-n_recommendations:][::-1]

        return top_indices
```

### 5. Natural Language Processing

```python
# NLP for Real Estate Documents
from transformers import pipeline, AutoTokenizer, AutoModel
import spacy

class RealEstateNLP:
    """
    NLP processing for contracts, listings, and documents
    """

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def extract_key_terms(self, document_text):
        """
        Extract important real estate terms and entities
        """
        doc = self.nlp(document_text)

        entities = {
            'addresses': [],
            'monetary_values': [],
            'dates': [],
            'organizations': [],
            'persons': []
        }

        for ent in doc.ents:
            if ent.label_ == 'GPE' or ent.label_ == 'LOC':
                entities['addresses'].append(ent.text)
            elif ent.label_ == 'MONEY':
                entities['monetary_values'].append(ent.text)
            elif ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
            elif ent.label_ == 'ORG':
                entities['organizations'].append(ent.text)
            elif ent.label_ == 'PERSON':
                entities['persons'].append(ent.text)

        return entities

    def summarize_listing(self, listing_text, max_length=130):
        """
        Summarize property listing
        """
        summary = self.summarizer(listing_text, max_length=max_length, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    def sentiment_analysis(self, reviews):
        """
        Analyze sentiment of tenant reviews or property descriptions
        """
        sentiment_pipeline = pipeline("sentiment-analysis")
        results = sentiment_pipeline(reviews)

        return pd.DataFrame(results)

    def extract_amenities(self, listing_text):
        """
        Extract amenities and features from listing text
        """
        amenity_keywords = {
            'parking': ['parking', 'garage', 'carport'],
            'outdoor': ['pool', 'patio', 'balcony', 'yard', 'garden'],
            'appliances': ['dishwasher', 'washer', 'dryer', 'refrigerator'],
            'hvac': ['air conditioning', 'heating', 'central air', 'hvac'],
            'flooring': ['hardwood', 'carpet', 'tile', 'laminate'],
            'utilities': ['utilities included', 'water included', 'gas included']
        }

        doc = self.nlp(listing_text.lower())
        text = doc.text

        found_amenities = {}
        for category, keywords in amenity_keywords.items():
            found_amenities[category] = [kw for kw in keywords if kw in text]

        return found_amenities
```

### 6. Optimization Algorithms

```python
# Portfolio Optimization
from scipy.optimize import minimize
import cvxpy as cp

class PortfolioOptimizer:
    """
    Optimize real estate portfolio allocation
    """

    def mean_variance_optimization(self, expected_returns, cov_matrix, risk_aversion=1.0):
        """
        Modern Portfolio Theory optimization
        """
        n_assets = len(expected_returns)

        # Define optimization variables
        weights = cp.Variable(n_assets)

        # Expected return
        portfolio_return = expected_returns.T @ weights

        # Portfolio risk (variance)
        portfolio_risk = cp.quad_form(weights, cov_matrix)

        # Objective: maximize return - risk_aversion * variance
        objective = cp.Maximize(portfolio_return - risk_aversion * portfolio_risk)

        # Constraints
        constraints = [
            cp.sum(weights) == 1,  # Weights sum to 1
            weights >= 0,           # No short selling
            weights <= 0.3          # Max 30% in any single asset
        ]

        # Solve
        problem = cp.Problem(objective, constraints)
        problem.solve()

        return {
            'weights': weights.value,
            'expected_return': portfolio_return.value,
            'expected_risk': np.sqrt(portfolio_risk.value)
        }

    def maximize_sharpe_ratio(self, expected_returns, cov_matrix, risk_free_rate=0.03):
        """
        Maximize Sharpe ratio for optimal risk-adjusted returns
        """
        n_assets = len(expected_returns)

        def neg_sharpe(weights):
            portfolio_return = np.dot(weights, expected_returns)
            portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            sharpe = (portfolio_return - risk_free_rate) / portfolio_std
            return -sharpe

        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weights sum to 1
        ]
        bounds = tuple((0, 0.3) for _ in range(n_assets))  # 0-30% per asset

        result = minimize(
            neg_sharpe,
            x0=np.ones(n_assets) / n_assets,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        return {
            'weights': result.x,
            'sharpe_ratio': -result.fun
        }
```

## Best Practices

### ✅ DO:

1. **Start with Simple Models**
   - Begin with baseline models (linear regression, decision trees)
   - Add complexity only if justified by performance gains
   - Compare against simple heuristics

2. **Validate Rigorously**
   - Use train/validation/test split (e.g., 70/15/15)
   - Apply cross-validation for robust estimates
   - Test on out-of-time data for time series
   - Check for data leakage

3. **Engineer Features Thoughtfully**
   - Create domain-relevant features
   - Handle missing data appropriately
   - Normalize/standardize as needed
   - Test feature importance

4. **Monitor Model Performance**
   - Track metrics over time
   - Set up alerts for degradation
   - Retrain periodically with new data
   - A/B test new models

5. **Interpret and Explain**
   - Use SHAP values or LIME for model interpretability
   - Provide feature importance rankings
   - Explain predictions in business terms
   - Validate that model learns real patterns, not artifacts

6. **Production Readiness**
   - Write clean, modular code
   - Add comprehensive logging
   - Handle edge cases gracefully
   - Version models and data
   - Document model cards

### ❌ DON'T:

1. **Overfit to Training Data**
   - Monitor training vs. validation metrics
   - Use regularization (L1, L2, dropout)
   - Avoid excessive model complexity

2. **Ignore Data Quality**
   - Always check for and handle missing data
   - Validate data distributions
   - Remove or correct anomalies appropriately

3. **Use Black Boxes Blindly**
   - Understand what the model is learning
   - Validate against business logic
   - Check for bias and fairness issues

4. **Forget Business Context**
   - Models must solve real business problems
   - Consider implementation costs
   - Account for stakeholder constraints

## Model Evaluation Metrics

### Regression Metrics:
- **MAE** (Mean Absolute Error): Average absolute difference
- **RMSE** (Root Mean Squared Error): Penalizes large errors more
- **MAPE** (Mean Absolute Percentage Error): Error as % of actual
- **R²** (R-squared): Proportion of variance explained

### Classification Metrics:
- **Accuracy**: Overall correctness
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under ROC curve

### Time Series Metrics:
- **MASE** (Mean Absolute Scaled Error)
- **Forecast Bias**: Tendency to over/under-predict
- **Prediction Intervals**: Confidence bounds

## Execution Instructions

When this skill is invoked:

1. **Define the Problem**
   - Clarify the business objective
   - Identify the target variable
   - Determine success metrics

2. **Prepare Data**
   - Collect and clean data
   - Handle missing values
   - Engineer features
   - Split data appropriately

3. **Build Models**
   - Start with baseline models
   - Experiment with algorithms
   - Tune hyperparameters
   - Validate performance

4. **Evaluate and Iterate**
   - Compare models objectively
   - Analyze errors and residuals
   - Refine features and models
   - Test on holdout data

5. **Deploy and Monitor**
   - Package model for production
   - Set up monitoring and logging
   - Create retraining pipeline
   - Document thoroughly

6. **Communicate Results**
   - Explain model performance in business terms
   - Provide actionable insights
   - Show example predictions
   - Document limitations

## Integration with Other Skills

- **Data Analysis**: Use for exploratory analysis before modeling
- **Finance**: Apply to financial forecasting and valuation
- **Manager/CEO**: Frame model outputs for strategic decisions
- **Marketing**: Segment customers and optimize campaigns

## Deliverable Checklist

Before completing data science project:
- [ ] Business problem is clearly defined
- [ ] Data quality has been assessed
- [ ] Features have been engineered and validated
- [ ] Multiple models have been compared
- [ ] Best model has been selected with justification
- [ ] Model has been validated on holdout data
- [ ] Performance metrics are documented
- [ ] Model is interpretable and explainable
- [ ] Code is production-ready and documented
- [ ] Monitoring and retraining plan exists
- [ ] Results communicated to stakeholders

