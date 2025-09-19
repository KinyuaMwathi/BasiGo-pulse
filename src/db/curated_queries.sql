-- src/db/curated_queries.sql
-- Curated analytics tables for BasiGo Pulse (all in public schema)

-- 1. Daily route metrics
DROP TABLE IF EXISTS public.daily_route_metrics;
CREATE TABLE public.daily_route_metrics AS
SELECT
    t.date,
    t.route_id,
    r.origin,
    r.destination,
    r.operator,
    SUM(t.passengers) AS total_passengers,
    SUM(t.revenue) AS total_revenue,
    SUM(t.expected_passengers) AS expected_passengers,
    SUM(t.expected_revenue) AS expected_revenue,
    SUM(f.total_cost) AS total_cost,
    SUM(f.energy_cost) AS energy_cost,
    SUM(f.maintenance_cost) AS maintenance_cost,
    SUM(f.driver_cost) AS driver_cost,
    CASE WHEN SUM(t.passengers)=0 THEN 0
         ELSE SUM(t.passengers)::FLOAT / NULLIF(COUNT(t.trip_id)*r.capacity,0) END AS avg_load_factor,
    CASE WHEN SUM(te.km_driven)=0 THEN NULL ELSE SUM(f.total_cost)::FLOAT / SUM(te.km_driven) END AS cost_per_km,
    CASE WHEN SUM(t.revenue)=0 THEN NULL ELSE (SUM(t.revenue)-SUM(f.total_cost))/SUM(t.revenue) END AS profit_margin,
    SUM(t.revenue)-SUM(f.total_cost) AS profit,
    SUM(t.revenue)-SUM(t.expected_revenue) AS variance_vs_expected
FROM public.trips t
LEFT JOIN public.routes r ON t.route_id = r.route_id
LEFT JOIN public.financials f ON t.route_id = f.route_id AND t.date = f.date
LEFT JOIN public.telematics te ON t.trip_id = te.trip_id
GROUP BY t.date, t.route_id, r.origin, r.destination, r.operator;

-- 2. Bus utilization metrics
DROP TABLE IF EXISTS public.bus_utilization;
CREATE TABLE public.bus_utilization AS
SELECT
    te.bus_id,
    te.date,
    COUNT(DISTINCT t.trip_id) AS trips_count,
    SUM(te.km_driven) AS km_driven,
    SUM(te.energy_kwh) AS total_energy,
    SUM(te.charging_cost) AS charging_cost,
    SUM(te.downtime_hr) AS downtime_hr,
    SUM(te.maint_cost) AS maintenance_cost,
    AVG(CASE WHEN t.passengers IS NULL THEN 0 ELSE t.passengers::FLOAT END) AS avg_passengers_per_trip
FROM public.telematics te
LEFT JOIN public.trips t ON te.trip_id = t.trip_id
GROUP BY te.bus_id, te.date;

-- 3. Route financials summary
DROP TABLE IF EXISTS public.route_financials;
CREATE TABLE public.route_financials AS
SELECT
    f.date,
    f.route_id,
    SUM(f.total_revenue) AS total_revenue,
    SUM(f.total_cost) AS total_cost,
    SUM(f.energy_cost) AS energy_cost,
    SUM(f.maintenance_cost) AS maintenance_cost,
    SUM(f.driver_cost) AS driver_cost,
    SUM(f.expected_revenue) AS expected_revenue,
    SUM(f.total_revenue)-SUM(f.total_cost) AS profit,
    SUM(f.total_revenue)-SUM(f.expected_revenue) AS variance_vs_expected
FROM public.financials f
GROUP BY f.date, f.route_id;

-- 4. Maintenance summary per bus
DROP TABLE IF EXISTS public.maintenance_summary;
CREATE TABLE public.maintenance_summary AS
SELECT
    m.date,
    m.bus_id,
    COUNT(m.maintenance_id) AS issues_count,
    SUM(m.cost) AS total_cost,
    SUM(m.downtime_hours) AS total_downtime
FROM public.maintenance m
GROUP BY m.date, m.bus_id;

-- 5. Forecast comparison (optional)
DROP TABLE IF EXISTS public.forecasts_comparison;
CREATE TABLE public.forecasts_comparison AS
SELECT
    drm.date,
    drm.route_id,
    drm.total_passengers,
    drm.total_revenue,
    drm.expected_passengers,
    drm.expected_revenue,
    drm.profit,
    drm.variance_vs_expected
FROM public.daily_route_metrics drm;
