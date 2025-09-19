import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Ensure top-level data directory exists
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")
os.makedirs(DATA_DIR, exist_ok=True)

fake = Faker()

# Define operators & routes
routes_data = [
    ("R01", "Citi Hoppa", "CBD", "Airport", 18, 40),
    ("R02", "East Shuttle", "City Stadium", "Dandora", 12, 35),
    ("R03", "Super Metro", "CBD", "Kikuyu", 22, 45),
    ("R04", "Super Metro", "CBD", "Kitengela", 30, 45),
    ("R05", "OMA", "CBD", "Kariobangi South", 15, 30),
    ("R06", "OMA", "CBD", "CIVO", 14, 30),
    ("R07", "MetroTrans", "CBD", "Utawala", 25, 40),
    ("R08", "Embassava", "CBD", "Nyayo Estate", 10, 33),
    ("R09", "Embassava", "CBD", "Jacaranda", 20, 33),
]

# Save routes.csv
routes_df = pd.DataFrame(routes_data, columns=[
    "route_id", "operator", "origin", "destination", "distance_km", "capacity"
])
routes_df.to_csv(os.path.join(DATA_DIR, "routes.csv"), index=False)

# Config
num_days = 120         # ~4 months of data
buses_per_route = 5
trips_per_day = 8

# Generate trips.csv
trips_records = []
for rid, operator, origin, dest, dist, cap in routes_data:
    for bus_num in range(1, buses_per_route+1):
        bus_id = f"{rid}-B{bus_num}"
        for day in range(num_days):
            date = datetime.today() - timedelta(days=num_days-day)
            for trip in range(trips_per_day):
                passengers = np.random.randint(cap//2, cap+1)
                ticket_price = random.choice([50, 70, 100])
                revenue = passengers * ticket_price

                # Forecast vs Actual
                expected_passengers = int(cap * np.random.uniform(0.6, 0.95))
                expected_revenue = expected_passengers * ticket_price

                trips_records.append([
                    fake.uuid4(), date.date(), bus_id, rid,
                    passengers, ticket_price, revenue,
                    expected_passengers, expected_revenue
                ])

trips_df = pd.DataFrame(trips_records, columns=[
    "trip_id", "date", "bus_id", "route_id",
    "passengers", "ticket_price", "revenue",
    "expected_passengers", "expected_revenue"
])
trips_df.to_csv(os.path.join(DATA_DIR, "trips.csv"), index=False)

# Generate telematics.csv
telematics_records = []
for idx, row in trips_df.iterrows():
    km = row["passengers"] * 0.5 + np.random.randint(5, 10)
    energy = km * 1.2
    charging_cost = energy * 15   # KES estimate
    downtime = np.random.choice([0, 0.5, 1], p=[0.9, 0.05, 0.05])
    maint_cost = np.random.choice([0, 200, 500, 1000], p=[0.85, 0.1, 0.03, 0.02])
    telematics_records.append([
        row["bus_id"], row["trip_id"], row["date"],
        km, energy, charging_cost, downtime, maint_cost
    ])

telematics_df = pd.DataFrame(telematics_records, columns=[
    "bus_id", "trip_id", "date", "km_driven",
    "energy_kwh", "charging_cost", "downtime_hr", "maint_cost"
])
telematics_df.to_csv(os.path.join(DATA_DIR, "telematics.csv"), index=False)

# Generate financials.csv
financials_records = []
for (rid, operator, origin, dest, dist, cap) in routes_data:
    for day in range(num_days):
        date = datetime.today() - timedelta(days=num_days-day)
        revenue = trips_df.loc[
            (trips_df["date"] == date.date()) & (trips_df["route_id"] == rid),
            "revenue"
        ].sum()

        # Costs capped at 40% of revenue
        energy_cost = int(revenue * np.random.uniform(0.05, 0.15))
        driver_cost = int(revenue * np.random.uniform(0.1, 0.15))
        maintenance_cost = int(revenue * np.random.uniform(0.05, 0.1))
        total_cost = energy_cost + driver_cost + maintenance_cost

        # Expected revenue is slightly lower than actual revenue
        expected_revenue = revenue * np.random.uniform(0.85, 0.95)

        financials_records.append([
            fake.uuid4(), date.date(), rid, revenue,
            total_cost, energy_cost, maintenance_cost, driver_cost,
            expected_revenue
        ])

financials_df = pd.DataFrame(financials_records, columns=[
    "record_id", "date", "route_id", "total_revenue",
    "total_cost", "energy_cost", "maintenance_cost", "driver_cost",
    "expected_revenue"
])
financials_df.to_csv(os.path.join(DATA_DIR, "financials.csv"), index=False)

# Generate maintenance.csv
maintenance_records = []
for rid, operator, origin, dest, dist, cap in routes_data:
    for bus_num in range(1, buses_per_route+1):
        bus_id = f"{rid}-B{bus_num}"
        for _ in range(25):   # ~25 logs per bus
            date = datetime.today() - timedelta(days=np.random.randint(1, num_days))
            issue = random.choice([
                "Battery Fault", "Brake Issue", "Software Update", "Suspension", "Motor Fault"
            ])
            # Cap maintenance cost at 40% of average ticket revenue per trip for that bus
            avg_revenue_per_trip = trips_df.loc[trips_df["bus_id"] == bus_id, "revenue"].mean()
            cost = min(np.random.randint(500, 5000), int(avg_revenue_per_trip * 0.4))
            downtime = round(np.random.uniform(1, 5), 1)
            maintenance_records.append([
                fake.uuid4(), bus_id, date.date(), issue, cost, downtime
            ])

maintenance_df = pd.DataFrame(maintenance_records, columns=[
    "maintenance_id", "bus_id", "date", "issue_type", "cost", "downtime_hours"
])
maintenance_df.to_csv(os.path.join(DATA_DIR, "maintenance.csv"), index=False)

print("✅ Mock CSVs generated in ./data/ with capped costs and expected revenue < actual revenue")