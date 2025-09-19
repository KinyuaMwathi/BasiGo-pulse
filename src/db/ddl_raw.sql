-- src/db/ddl_raw.sql
-- Create raw tables aligned with your generator outputs (public schema)

-- 1. routes
CREATE TABLE IF NOT EXISTS public.routes (
  route_id         VARCHAR(16) PRIMARY KEY,
  operator         VARCHAR(64),
  origin           VARCHAR(100),
  destination      VARCHAR(100),
  distance_km      INTEGER,
  capacity         INTEGER
);

-- 2. trips
CREATE TABLE IF NOT EXISTS public.trips (
  trip_id              VARCHAR(64) PRIMARY KEY,
  date                 DATE,
  bus_id               VARCHAR(32),
  route_id             VARCHAR(16),
  passengers           INTEGER,
  ticket_price         DECIMAL(10,2),
  revenue              DECIMAL(12,2),
  expected_passengers  INTEGER,
  expected_revenue     DECIMAL(12,2)
);

-- 3. telematics
CREATE TABLE IF NOT EXISTS public.telematics (
  telemetry_id   BIGINT IDENTITY(1,1) PRIMARY KEY,
  bus_id         VARCHAR(32),
  trip_id        VARCHAR(64),
  date           DATE,
  km_driven      DECIMAL(10,2),
  energy_kwh     DECIMAL(10,2),
  charging_cost  DECIMAL(12,2),
  downtime_hr    DECIMAL(6,2),
  maint_cost     DECIMAL(12,2)
);

-- 4. financials
CREATE TABLE IF NOT EXISTS public.financials (
  record_id        VARCHAR(64) PRIMARY KEY,
  date             DATE,
  route_id         VARCHAR(16),
  total_revenue    DECIMAL(14,2),
  total_cost       DECIMAL(14,2),
  energy_cost      DECIMAL(12,2),
  maintenance_cost DECIMAL(12,2),
  driver_cost      DECIMAL(12,2),
  expected_revenue DECIMAL(14,2)
);

-- 5. maintenance
CREATE TABLE IF NOT EXISTS public.maintenance (
  maintenance_id  VARCHAR(64) PRIMARY KEY,
  bus_id          VARCHAR(32),
  date            DATE,
  issue_type      VARCHAR(128),
  cost            DECIMAL(12,2),
  downtime_hours  DECIMAL(6,2)
);