# Camera & Hardware Tables

## game_resources
Camera and video resource metadata for games.

**Common Columns:**
- `soccer_game_id` - Maps to `game_id` in MySQL games table
- `camera_metadata` - JSON blob with camera session info
- `game_resource_id` - Primary key
- `creation_time` - When resource was created

**camera_metadata JSON Paths:**

| Path | Description |
|------|-------------|
| `game_info_v3.swversion` | GKU software version |
| `game_info_v3.app.version` | Camcon version during upload |
| `game_info_v3.app.recordversion` | Camcon version during recording |
| `game_info_v3.caseID` | Camera case ID (e.g., "X6630") |
| `game_info_v3.cameraID` | Camera module ID (e.g., "CX6630A") |
| `game_info_v3.hw_metadata.numNoRecord` | Count of "no record" failures |
| `game_info_v3.associated_sessions` | Array of sessions (>1 = restart) |
| `game_info_v3.battery.normalOff` | Normal shutdown |
| `game_info_v3.battery.died` | Battery died |
| `game_info_v3.battery.startpercent` | Battery % at start |
| `game_info_v3.timeQuality` | Time sync quality (0-5) |
| `blurriness.<cameraID>` | Blurriness metric |

**timeQuality Values:**
- 0: GPS fix, sub-millisecond accuracy
- 1: NTP, millisecond accuracy
- 5: No time sync, could be off by months

**Extract software versions:**
```sql
SELECT
    soccer_game_id as game_id,
    NULLIF(json_extract_path_text(camera_metadata, 'game_info_v3', 'swversion'), '') AS gku_version,
    NULLIF(json_extract_path_text(camera_metadata, 'game_info_v3', 'app', 'recordversion'), '') AS camcon_version,
    NULLIF(json_extract_path_text(camera_metadata, 'game_info_v3', 'caseID'), '') AS camera_id
FROM tracedb.game_resources WHERE soccer_game_id = 12345
```

---

## hardware_assets
Camera hardware asset tracking for operations.

**Common Columns:**
- `asset_id` - Asset URL (e.g., `https://trce.ai/c?12345`)
- `status` - Current status (see below)
- `category` - e.g., 'Trace Cam 2L', 'Trace Case'
- `case_id`, `pi_id` - Camera identifiers
- `customer_sent_to` - Customer email
- `date_checked_out`, `date_checked_in` - Dates
- `division_id` - Associated division

**Status Values:**
- `Checked Out: SUB` - Checked out with subscription
- `Checked Out: Sub Unused Asset` - Checked out but not used
- `Awaiting Return` - Waiting for return

**Camera ID from asset_id:**
```sql
CONCAT('X', SUBSTRING(asset_id FROM POSITION('c?' IN asset_id) + 2)) AS camera_id
-- Example: 'https://trce.ai/c?12345' → 'X12345'
```

---

## cases
Camera case information.
- `case_id` - Primary key
- `pi_id` - Camera identifier (e.g., 'X6630')

---

## case_sessions
Camera connection sessions - tracks when cameras come online.

**Common Columns:**
- `case_id`, `case_session_id` - Keys
- `cameras` - SUPER type (JSON array)
- `wifi_name` - Connected WiFi
- `start_time`, `end_time`, `update_time` - Times
- `tracemon_version` - Camcon version (integer, e.g., 384)
- `pi_temperature` - JSON with CPU temp
- `record_camera` - Recording camera info with `batteryPercent`

```sql
-- Cameras online with specific version
SELECT c.pi_id AS camera_id, cs.tracemon_version, cs.update_time, cs.wifi_name
FROM tracedb.case_sessions cs
JOIN tracedb.cases c ON c.case_id = cs.case_id
WHERE cs.update_time > CURRENT_TIMESTAMP - INTERVAL '24 hours'
    AND cs.tracemon_version = 384 AND c.pi_id LIKE 'X%'
```

---

## case_video_sets
Video file sets uploaded from cameras.
- `case_video_set_id`, `case_id`, `case_session_id` - Keys
- `camera_id`, `game_id`, `num_video_files`
- `video_set_time`, `creation_time`

---

## game_video_info
Individual video file metadata.
- `game_id`, `file_relative_path` - Keys
- `duration_ms` - Expected: 300000 = 5 minutes
- `fps`, `camera_name`, `pi_id`
- `file_mode` - 'chunk' for video chunks

**Video File Naming:**
```sql
CASE WHEN file_relative_path LIKE '%CX%A_%' THEN 'A'
     WHEN file_relative_path LIKE '%CX%B_%' THEN 'B' END AS camera_type
-- First video chunk (_001.MP4) contains sound sync tone
```

---

## game_clips
Game clip highlights with player tagging.
- `game_clip_id`, `game_id`
- `type` - 'FullGameVideo', 'generic', 'CustomUpload'
- `meta` - JSON array of tagged players (e.g., `["home-5", "home-12"]`)

---

## batch_job_stats / batch_process_stats
Processing pipeline statistics.

**Job Type Categories:**
- `mcv`, `video_chunk` → `tracecam_video_copy`
- `udetect_c`, `full_panorama_processor` → `object_detection`
- `gpu_hls`, `render2_start_control` → `video_render`

---

# Redshift JSON Parsing

**Different from MySQL!** Use PostgreSQL-style functions:

```sql
-- Extract nested string value
json_extract_path_text(camera_metadata, 'game_info_v3', 'swversion')

-- Get array length
json_array_length(NULLIF(json_extract_path_text(camera_metadata, 'game_info_v3', 'associated_sessions'), ''))

-- Extract array element (index 1 = second element)
json_extract_array_element_text(json_extract_path_text(...), 1)
```

**Camera Failure Detection:**
```sql
WITH session_data AS (
    SELECT soccer_game_id as game_id,
        json_array_length(NULLIF(json_extract_path_text(camera_metadata, 'game_info_v3', 'associated_sessions'), '')) as num_sessions,
        NULLIF(json_extract_path_text(camera_metadata, 'game_info_v3', 'hw_metadata', 'numNoRecord'), '')::int as num_no_record
    FROM game_resources WHERE soccer_game_id IN (...)
)
SELECT game_id,
    CASE WHEN num_sessions > 2 OR num_no_record > 0 THEN 1 ELSE 0 END AS has_camera_issue
FROM session_data
```
