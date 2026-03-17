import json
import logging
import os
from pathlib import Path


logger = logging.getLogger(__name__)

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
DATASET_DIR = os.getenv("DATASET_DIR", "dataset")


def run(task: dict) -> None:
    task_ids = task["task_ids"]
    output_dir = Path(OUTPUT_DIR)
    dataset_dir = Path(DATASET_DIR)
    merged = []

    for task_id in task_ids:
        path = output_dir / f"{task_id}.json"
        records = json.loads(path.read_text())
        merged.extend(records)
        logger.info("Reduce: loaded %d records from %s", len(records), path)

    city_data: dict = {}
    for record in merged:
        location = record["location"]
        city = city_data.setdefault(location, {"total_aqi": 0.0, "peak_aqi": 0.0, "count": 0, "readings_exceeding_safe_limit": 0})
        city["total_aqi"] += record["features"]["aqi"]
        city["peak_aqi"] = max(city["peak_aqi"], record["features"]["aqi"])
        city["count"] += 1
        city["readings_exceeding_safe_limit"] += record["features"]["exceeds_safe_limit"]

    for _, data in city_data.items():
        data["avg_aqi"] = round(data.pop("total_aqi") / data.pop("count"), 2)

    final_path = output_dir / "final_features_dataset.json"
    final_path.write_text(json.dumps(city_data, indent=2))
    logger.info("Reduce complete: %d total records aggregated into %d cities -> %s", len(merged), len(city_data), final_path)

    for chunk_file in dataset_dir.glob("*_chunk_*.json"):
        chunk_file.unlink()
        logger.info("Removed chunk file %s", chunk_file)

    for task_id in task_ids:
        intermediate = output_dir / f"{task_id}.json"
        intermediate.unlink(missing_ok=True)
        logger.info("Removed intermediate file %s", intermediate)
