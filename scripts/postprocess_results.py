"""Recalculate local joint-axis torques from the archived RecurDyn request file.

Python 3.10+; standard library only. This does not start or rerun RecurDyn.
Use --check to verify committed results without writing files.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "SystemDynamics_UR3_pick_place_screw_bearing"
JOINTS = ("J1_Base", "J2_Shoulder", "J3_Elbow", "J4_Wrist1", "J5_Wrist2", "J6_Wrist3")


def rmd_blocks(text: str, entity: str) -> dict[int, str]:
    starts = list(re.finditer(r"(?m)^([A-Z_]+)\s*/\s*(\d+)\s*$", text))
    return {
        int(match.group(2)): text[match.end():starts[index + 1].start() if index + 1 < len(starts) else len(text)]
        for index, match in enumerate(starts)
        if match.group(1) == entity
    }


def integer_field(block: str, field: str) -> int:
    match = re.search(rf"(?m)^,\s*{field}\s*=\s*(\d+)\s*$", block)
    if match is None:
        raise ValueError(f"Missing RMD field: {field}")
    return int(match.group(1))


def check_model(path: Path) -> dict[int, tuple[int, int]]:
    text = path.read_text(encoding="utf-8-sig")
    for field, unit in (("FORCE", "Newton"), ("LENGTH", "Millimeter"), ("TIME", "Second"), ("MASS", "Kilogram")):
        if not re.search(rf"(?m)^,\s*{field}\s*=\s*{unit}\s*$", text):
            raise ValueError(f"Unsupported model unit: {field}; expected {unit}")
    joints, requests = rmd_blocks(text, "JOINT"), rmd_blocks(text, "REQUEST")
    if set(requests) != set(range(1, 7)):
        raise ValueError("Expected exactly six standard force requests, IDs 1..6")
    markers = {}
    for index, label in enumerate(JOINTS, 1):
        joint, request = joints[index], requests[index]
        if f"NAME = 'Rev_{label}'" not in joint or not re.search(r"(?m)^,\s*Revolute\s*$", joint):
            raise ValueError(f"Joint {index} is not the expected revolute joint")
        if f"NAME = 'REQ_TORQUE_J{index}_Rev_{label}'" not in request:
            raise ValueError(f"Unexpected request name at ID {index}")
        if not re.search(r"(?m)^,\s*FORCE\s*$", request):
            raise ValueError(f"Request {index} is not a force request")
        pair = integer_field(joint, "I"), integer_field(joint, "J")
        if (integer_field(request, "I"), integer_field(request, "J")) != pair:
            raise ValueError(f"Request {index} does not measure its joint marker pair")
        if integer_field(request, "RM") != pair[1]:
            raise ValueError(f"Request {index} is not resolved in its joint base marker; local TZ is not justified")
        markers[index] = pair
    return markers


def read_req(path: Path, markers: dict[int, tuple[int, int]]):
    lines = [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if len(lines) < 9 or lines[0] != "A.R3":
        raise ValueError("Expected an ASCII RecurDyn A.R3 request file")
    request_count, ucf = lines[1].split()
    count = int(request_count)
    if count != 6 or not math.isclose(float(ucf), 1000.0):
        raise ValueError("Expected six requests and N/kg/mm/s unit correlation factor 1000")
    ids = []
    for line in lines[2:2 + count]:
        req_id, kind, action, base, zero = map(int, line.split())
        if kind != 4 or markers.get(req_id) != (action, base) or zero != 0:
            raise ValueError("REQ header does not match the RMD force request marker pairs")
        ids.append(req_id)
    if len(set(ids)) != count:
        raise ValueError("Duplicate request ID")
    remainder = lines[2 + count:]
    if len(remainder) % (count + 1):
        raise ValueError("Truncated request timestep")
    samples = {req_id: [] for req_id in ids}
    previous_time = -math.inf
    for offset in range(0, len(remainder), count + 1):
        time_s = float(remainder[offset])
        if not math.isfinite(time_s) or time_s <= previous_time:
            raise ValueError("REQ times must be finite and strictly increasing")
        previous_time = time_s
        for position, req_id in enumerate(ids, 1):
            values = tuple(float(v) for v in remainder[offset + position].split())
            if len(values) != 6 or not all(map(math.isfinite, values)):
                raise ValueError("Each force request must have six finite FX,FY,FZ,TX,TY,TZ values")
            samples[req_id].append((time_s, values))
    times = [time_s for time_s, _ in samples[1]]
    if len(times) != 901:
        raise ValueError("Expected exactly 901 samples in the archived final run")
    if not times or not math.isclose(times[0], 0.0, abs_tol=1e-9) or not math.isclose(times[-1], 18.5, abs_tol=1e-7):
        raise ValueError("Expected the archived final run from 0 to 18.5 seconds")
    return samples


def read_waypoints(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    times = [float(row["time_s"]) for row in rows]
    if len(rows) != 20 or any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError("Expected twenty internal motion states with increasing timestamps")
    return rows


def csv_text(rows: list[dict]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate(req: Path, rmd: Path, waypoints: Path, safety_factor: float = 1.5):
    markers = check_model(rmd)
    samples = read_req(req, markers)
    waypoint_rows = read_waypoints(waypoints)
    time_rows, summary_rows = [], []
    for req_id, label in enumerate(JOINTS, 1):
        joint_rows = []
        for time_s, values in samples[req_id]:
            fx, fy, fz, tx, ty, tz = values
            row = {
                "time_s": time_s,
                "joint": label,
                "axis_component": "TZ",
                "axis_torque_Nm": tz / 1000.0,
                "moment_resultant_Nm": math.sqrt(tx * tx + ty * ty + tz * tz) / 1000.0,
                "force_resultant_N": math.sqrt(fx * fx + fy * fy + fz * fz),
            }
            joint_rows.append(row)
        time_rows.extend(joint_rows)
        peak = max(joint_rows, key=lambda row: abs(row["axis_torque_Nm"]))
        avg_speed = max(
            abs(float(b[f"J{req_id}_deg"]) - float(a[f"J{req_id}_deg"])) /
            (float(b["time_s"]) - float(a["time_s"]))
            for a, b in zip(waypoint_rows, waypoint_rows[1:])
        )
        summary_rows.append({
            "joint": label,
            "axis_component": "TZ",
            "reference_marker_id": markers[req_id][1],
            "peak_time_s": peak["time_s"],
            "peak_signed_axis_torque_Nm": peak["axis_torque_Nm"],
            "required_peak_abs_torque_Nm": abs(peak["axis_torque_Nm"]),
            "safety_factor": safety_factor,
            "joint_torque_with_margin_Nm": abs(peak["axis_torque_Nm"]) * safety_factor,
            "max_waypoint_avg_speed_deg_s": avg_speed,
            "moment_resultant_at_peak_Nm": peak["moment_resultant_Nm"],
            "force_resultant_at_peak_N": peak["force_resultant_N"],
            "max_moment_resultant_Nm": max(row["moment_resultant_Nm"] for row in joint_rows),
            "max_force_resultant_N": max(row["force_resultant_N"] for row in joint_rows),
        })
    verification = {
        "method": "Recalculate archived request data; no solver rerun",
        "axis": "Local TZ for every revolute joint; request RM equals the joint base marker",
        "force_unit": "N",
        "source_torque_unit": "N mm",
        "output_torque_unit": "N m",
        "duration_s": samples[1][-1][0],
        "samples_per_joint": len(samples[1]),
        "internal_motion_states": len(waypoint_rows),
        "safety_factor": safety_factor,
        "sha256": {"req": digest(req), "rmd": digest(rmd), "joint_table": digest(waypoints)},
        "limitations": [
            "Prescribed motion, rigid surrogate gripper and switched ideal constraints",
            "No active contact forces or validated frictional gripping/free fall",
            "Joint-side sampled peak torques, not a gearbox or commercial motor selection",
            "Waypoint-average speeds are not instantaneous STEP profile peak speeds",
        ],
    }
    return {
        "torque_timeseries.csv": csv_text(time_rows),
        "motor_capacity_summary.csv": csv_text(summary_rows),
        "verification.json": json.dumps(verification, indent=2, ensure_ascii=False) + "\n",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--req", type=Path, default=ROOT / "results/solver/UR3_v81_clean_optimized.req")
    parser.add_argument("--rmd", type=Path, default=ROOT / f"model/{BASE}.rmd")
    parser.add_argument("--waypoints", type=Path, default=ROOT / "data/joint_table.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--check", action="store_true", help="verify committed files without changing them")
    args = parser.parse_args()
    try:
        outputs = calculate(args.req, args.rmd, args.waypoints)
        if not args.check:
            args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, expected in outputs.items():
            destination = args.output_dir / name
            if args.check:
                if not destination.is_file() or destination.read_text(encoding="utf-8") != expected:
                    raise ValueError(f"Result is missing or differs from recomputation: {name}")
            else:
                destination.write_text(expected, encoding="utf-8", newline="")
        print("PASS: six local-TZ requests, 901 samples per joint, 0-18.5 s; " +
              ("committed results match" if args.check else "results recalculated"))
    except (OSError, ValueError, KeyError, IndexError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")


if __name__ == "__main__":
    main()
