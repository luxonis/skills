#!/usr/bin/env python3
"""Capture or replay a clean holistic recording of this device's sources.

Copy into the customer project and run from the isolated env that has DepthAI v3.
Do not record through the product app. Confirm Camera / RecordConfig / IMU APIs
against the current holistic_record example before a first run on a new DepthAI
version.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


def load_depthai():
    try:
        import depthai as dai
    except ImportError as error:
        raise SystemExit(
            "depthai is not installed in this environment; use the project venv "
            "that already imports DepthAI v3"
        ) from error
    return dai


def connected_sockets(dai, device):
    if device is not None and hasattr(device, "getConnectedCameras"):
        sockets = list(device.getConnectedCameras())
        if sockets:
            return sockets
    return [dai.CameraBoardSocket.CAM_A]


def connected_imu(device) -> str:
    if device is None or not hasattr(device, "getConnectedIMU"):
        return ""
    try:
        value = device.getConnectedIMU() or ""
    except Exception:
        return ""
    name = str(value).strip()
    if name.upper() in ("", "NONE", "NULL"):
        return ""
    return name


def latest_tar(directory: Path) -> Path | None:
    tars = list(directory.glob("*.tar")) + list(directory.glob("**/*.tar"))
    if not tars:
        return None
    return max(tars, key=lambda path: path.stat().st_mtime)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("recordings"),
        help="Recording output directory (record mode)",
    )
    parser.add_argument(
        "--replay",
        type=Path,
        help="Replay this .tar instead of recording",
    )
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument(
        "--seconds",
        type=float,
        help="Stop after N seconds (needed when there is no preview window)",
    )
    parser.add_argument(
        "--save-frame",
        type=Path,
        help="Write one preview frame (PNG/JPEG) then continue until stop",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dai = load_depthai()
    try:
        import cv2
    except ImportError:
        cv2 = None
        if args.save_frame is not None or args.seconds is None:
            raise SystemExit(
                "opencv-python is required for preview or --save-frame; "
                "install it in this env or pass --seconds without --save-frame"
            )

    if args.replay is not None and not args.replay.exists():
        raise SystemExit(f"recording not found: {args.replay}")

    with dai.Pipeline(True) as pipeline:
        if args.replay is not None:
            pipeline.enableHolisticReplay(str(args.replay))
        else:
            args.out.mkdir(parents=True, exist_ok=True)
            config = dai.RecordConfig()
            config.outputDir = str(args.out)
            if hasattr(config, "syncCameraOutputs"):
                config.syncCameraOutputs = True
            pipeline.enableHolisticRecord(config)

        device = pipeline.getDefaultDevice()
        sockets = connected_sockets(dai, device)
        imu_name = connected_imu(device)
        print(f"cameras={[str(socket) for socket in sockets]}")
        print(f"imu={imu_name or 'none'}")

        preview = None
        sync = pipeline.create(dai.node.Sync)
        if hasattr(sync, "setSyncAttempts"):
            sync.setSyncAttempts(0)
        for index, socket in enumerate(sockets):
            camera = pipeline.create(dai.node.Camera).build(socket)
            full = camera.requestFullResolutionOutput(fps=args.fps)
            full.link(sync.inputs[f"cam{index}"])
            if preview is None:
                preview = camera.requestOutput((640, 480), fps=args.fps)

        imu_queue = None
        if imu_name:
            imu = pipeline.create(dai.node.IMU)
            imu.enableIMUSensor(dai.IMUSensor.ACCELEROMETER_RAW, 400)
            imu.enableIMUSensor(dai.IMUSensor.GYROSCOPE_RAW, 400)
            imu.setBatchReportThreshold(100)
            imu_queue = imu.out.createOutputQueue()

        preview_queue = preview.createOutputQueue()
        pipeline.start()
        deadline = time.monotonic() + args.seconds if args.seconds else None
        saved = False
        try:
            while pipeline.isRunning():
                frame = preview_queue.get()
                if cv2 is not None:
                    image = frame.getCvFrame()
                    if args.save_frame is not None and not saved:
                        args.save_frame.parent.mkdir(parents=True, exist_ok=True)
                        cv2.imwrite(str(args.save_frame), image)
                        saved = True
                        print(f"wrote_frame={args.save_frame}")
                    cv2.imshow("holistic-record", image)
                    if cv2.waitKey(1) == ord("q"):
                        break
                if imu_queue is not None:
                    imu_queue.tryGet()
                if deadline is not None and time.monotonic() >= deadline:
                    break
        except KeyboardInterrupt:
            pass
        pipeline.stop()

    if args.replay is None:
        tar = latest_tar(args.out)
        if tar is None:
            raise SystemExit(f"no .tar written under {args.out}")
        print(f"recording={tar}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
