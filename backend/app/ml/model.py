import random
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from app.schemas.weather import WeatherData

class WeatherNowcaster:
    """
    Mock implementation of CNN + LSTM weather nowcasting and risk scoring.
    In production, this would load a pre-trained Keras/PyTorch model.
    """
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.is_loaded = True
        print("ML Model loaded successfully.")

    def preprocess_features(self, weather_data: WeatherData) -> np.ndarray:
        # Mock feature extraction
        features = [
            weather_data.temperature,
            weather_data.humidity,
            weather_data.pressure,
            weather_data.wind_speed,
            weather_data.precipitation
        ]
        # Reshape for scaler (1 sample, 5 features)
        return np.array(features).reshape(1, -1)

    def predict_risk(self, weather_data: WeatherData) -> dict:
        """
        Predict severe weather risk based on current data.
        Returns risk score and severity level.
        """
        # _ = self.preprocess_features(weather_data)
        
        # Mocking a prediction based loosely on heuristics to simulate ML
        base_risk = 0.1
        if weather_data.wind_speed > 20:
            base_risk += 0.3
        if weather_data.precipitation > 50:
            base_risk += 0.4
        if weather_data.pressure < 1000:
            base_risk += 0.2
            
        risk_score = min(max(base_risk + random.uniform(-0.1, 0.1), 0.0), 1.0)
        
        severity = "Low"
        if risk_score > 0.8:
            severity = "Critical"
        elif risk_score > 0.6:
            severity = "High"
        elif risk_score > 0.3:
            severity = "Moderate"
            
        return {
            "risk_score": round(risk_score, 2),
            "severity": severity,
            "prediction_confidence": round(random.uniform(0.75, 0.98), 2),
            "forecast_notes": "Possible severe conditions approaching." if risk_score > 0.6 else "Conditions are stable."
        }

ml_model = WeatherNowcaster()
