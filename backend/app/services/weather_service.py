import uuid
from typing import List, Optional
from supabase import Client
from app.schemas.weather import WeatherDataCreate

class WeatherService:
    def __init__(self, db: Client):
        self.db = db

    def ingest_weather_data(self, data: WeatherDataCreate) -> Optional[dict]:
        weather_id = str(uuid.uuid4())
        
        db_data = data.model_dump()
        # Ensure timestamp is string for JSON serialization
        db_data['timestamp'] = db_data['timestamp'].isoformat()
        db_data['id'] = weather_id

        try:
            response = self.db.table("weather_data").insert(db_data).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error ingesting weather data: {e}")
            return None

    def get_historical_data(self, lat: float, lon: float, limit: int = 100) -> List[dict]:
        try:
            # Simple bounding box or exact match for now. Real implementation needs PostGIS.
            response = self.db.table("weather_data") \
                .select("*") \
                .eq("latitude", lat) \
                .eq("longitude", lon) \
                .order("timestamp", desc=True) \
                .limit(limit) \
                .execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return []
