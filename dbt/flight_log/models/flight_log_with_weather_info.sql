select
  f.flight_id,
  f.pilot,
  f.glider_type,
  f.glider_id,
  f.timestamp,
  f.latitude,
  f.longitude,
  f.altitude,
  f.circling,
  f.climb_rate,
  a.temperature,
  a.wind_speed,
  a.wind_direction,
  a.daylight_hours,
  a.humidity,
  a.rainfall
from
  {{ ref('flight_log') }} as f
left join
  {{ source('data_lake', 'amedas') }} as a
  on
    timestamp_trunc(timestamp_sub(f.timestamp, interval mod(extract(minute from f.timestamp), 10) minute), minute) = a.timestamp
