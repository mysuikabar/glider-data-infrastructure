with tmp_flight_log as (
  select
    *,
    first_value(altitude) over (partition by timestamp_trunc(timestamp, minute) order by timestamp rows between unbounded preceding and unbounded following) as first_altitude,
    last_value(altitude) over (partition by timestamp_trunc(timestamp, minute) order by timestamp rows between unbounded preceding and unbounded following) as last_altitude,
    first_value(timestamp) over (partition by timestamp_trunc(timestamp, minute) order by timestamp rows between unbounded preceding and unbounded following) as first_timestamp,
    last_value(timestamp) over (partition by timestamp_trunc(timestamp, minute) order by timestamp rows between unbounded preceding and unbounded following) as last_timestamp
  from
    {{ source('data_lake', 'flight_log') }}
),

tmp_flight_log_aggregated as (
  select
    min(flight_id) as flight_id,
    min(pilot) as pilot,
    min(glider_type) as glider_type,
    min(glider_id) as glider_id,
    timestamp_trunc(timestamp, minute) as timestamp,
    avg(latitude) as latitude,
    avg(longitude) as longitude,
    avg(altitude) as altitude,
    min(circling) as circling,
    min(first_altitude) as first_altitude,
    min(last_altitude) as last_altitude,
    min(first_timestamp) as first_timestamp,
    min(last_timestamp) as last_timestamp
  from
    tmp_flight_log
  group by
    timestamp
)

select
  flight_id,
  pilot,
  glider_type,
  glider_id,
  timestamp,
  latitude,
  longitude,
  altitude,
  circling,
  (last_altitude - first_altitude) / timestamp_diff(last_timestamp, first_timestamp, second) as climb_rate
from
  tmp_flight_log_aggregated
where
  timestamp_diff(last_timestamp, first_timestamp, second) > 0
