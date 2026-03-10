#!/usr/bin/env python3
import argparse
import json
import time
import sys
from typing import Any


def load_pyautogui():
    try:
        import pyautogui  # type: ignore
    except ImportError:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "pyautogui is not installed",
                    "hint": "Install it with: pip install pyautogui",
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)
    return pyautogui


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def add_common_runtime_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--pause", type=float, default=0.0, help="Pause after each PyAutoGUI call")
    parser.add_argument(
        "--disable-failsafe",
        action="store_true",
        help="Disable PyAutoGUI failsafe. Use with care.",
    )


def configure_runtime(pyautogui: Any, args: argparse.Namespace) -> None:
    pyautogui.PAUSE = args.pause
    pyautogui.FAILSAFE = not args.disable_failsafe


def current_position(pyautogui: Any) -> tuple[int, int]:
    x, y = pyautogui.position()
    return int(x), int(y)


def cmd_screen_size(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    width, height = pyautogui.size()
    emit({"ok": True, "width": width, "height": height})


def cmd_mouse_position(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    x, y = current_position(pyautogui)
    emit({"ok": True, "x": x, "y": y})


def cmd_move(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    pyautogui.moveTo(args.x, args.y, duration=args.duration)
    x, y = current_position(pyautogui)
    emit({"ok": True, "action": "move", "x": x, "y": y, "duration": args.duration})


def cmd_drag(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    pyautogui.dragTo(args.x, args.y, duration=args.duration, button=args.button)
    x, y = current_position(pyautogui)
    emit(
        {
            "ok": True,
            "action": "drag",
            "x": x,
            "y": y,
            "duration": args.duration,
            "button": args.button,
        }
    )


def cmd_click(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    if args.x is not None and args.y is not None:
        pyautogui.click(
            x=args.x,
            y=args.y,
            clicks=args.clicks,
            interval=args.interval,
            button=args.button,
        )
    else:
        pyautogui.click(clicks=args.clicks, interval=args.interval, button=args.button)
    x, y = current_position(pyautogui)
    emit(
        {
            "ok": True,
            "action": "click",
            "x": x,
            "y": y,
            "button": args.button,
            "clicks": args.clicks,
            "interval": args.interval,
        }
    )


def cmd_mouse_down(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    kwargs: dict[str, Any] = {"button": args.button}
    if args.x is not None and args.y is not None:
        kwargs["x"] = args.x
        kwargs["y"] = args.y
    pyautogui.mouseDown(**kwargs)
    x, y = current_position(pyautogui)
    emit({"ok": True, "action": "mouse-down", "x": x, "y": y, "button": args.button})


def cmd_mouse_up(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    kwargs: dict[str, Any] = {"button": args.button}
    if args.x is not None and args.y is not None:
        kwargs["x"] = args.x
        kwargs["y"] = args.y
    pyautogui.mouseUp(**kwargs)
    x, y = current_position(pyautogui)
    emit({"ok": True, "action": "mouse-up", "x": x, "y": y, "button": args.button})


def cmd_type(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    pyautogui.write(args.text, interval=args.interval)
    if args.enter:
        pyautogui.press("enter")
    emit(
        {
            "ok": True,
            "action": "type",
            "text_length": len(args.text),
            "interval": args.interval,
            "enter": args.enter,
        }
    )


def cmd_press(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    pyautogui.press(args.key, presses=args.presses, interval=args.interval)
    emit(
        {
            "ok": True,
            "action": "press",
            "key": args.key,
            "presses": args.presses,
            "interval": args.interval,
        }
    )


def cmd_hotkey(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    pyautogui.hotkey(*args.keys, interval=args.interval)
    emit({"ok": True, "action": "hotkey", "keys": args.keys, "interval": args.interval})


def cmd_scroll(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    if args.x is not None and args.y is not None:
        pyautogui.scroll(args.clicks, x=args.x, y=args.y)
    else:
        pyautogui.scroll(args.clicks)
    x, y = current_position(pyautogui)
    emit({"ok": True, "action": "scroll", "clicks": args.clicks, "x": x, "y": y})


def cmd_screenshot(args: argparse.Namespace) -> None:
    pyautogui = load_pyautogui()
    configure_runtime(pyautogui, args)
    region = None
    if args.x is not None or args.y is not None or args.width is not None or args.height is not None:
        if None in (args.x, args.y, args.width, args.height):
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "x, y, width, and height must be provided together for region screenshots",
                    },
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            raise SystemExit(2)
        region = (args.x, args.y, args.width, args.height)
    image = pyautogui.screenshot(region=region)
    image.save(args.path)
    emit({"ok": True, "action": "screenshot", "path": args.path, "region": region})


def cmd_wait(args: argparse.Namespace) -> None:
    time.sleep(args.seconds)
    emit({"ok": True, "action": "wait", "seconds": args.seconds})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PyAutoGUI desktop automation helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    screen_size = subparsers.add_parser("screen-size", help="Get current screen resolution")
    add_common_runtime_flags(screen_size)
    screen_size.set_defaults(func=cmd_screen_size)

    mouse_position = subparsers.add_parser("mouse-position", help="Get current mouse position")
    add_common_runtime_flags(mouse_position)
    mouse_position.set_defaults(func=cmd_mouse_position)

    move = subparsers.add_parser("move", help="Move mouse to the target coordinates")
    move.add_argument("--x", type=int, required=True)
    move.add_argument("--y", type=int, required=True)
    move.add_argument("--duration", type=float, default=0.0)
    add_common_runtime_flags(move)
    move.set_defaults(func=cmd_move)

    drag = subparsers.add_parser("drag", help="Drag mouse to the target coordinates")
    drag.add_argument("--x", type=int, required=True)
    drag.add_argument("--y", type=int, required=True)
    drag.add_argument("--duration", type=float, default=0.0)
    drag.add_argument("--button", choices=["left", "middle", "right"], default="left")
    add_common_runtime_flags(drag)
    drag.set_defaults(func=cmd_drag)

    click = subparsers.add_parser("click", help="Click mouse at current or target coordinates")
    click.add_argument("--x", type=int)
    click.add_argument("--y", type=int)
    click.add_argument("--button", choices=["left", "middle", "right"], default="left")
    click.add_argument("--clicks", type=int, default=1)
    click.add_argument("--interval", type=float, default=0.0)
    add_common_runtime_flags(click)
    click.set_defaults(func=cmd_click)

    mouse_down = subparsers.add_parser("mouse-down", help="Press and hold a mouse button")
    mouse_down.add_argument("--x", type=int)
    mouse_down.add_argument("--y", type=int)
    mouse_down.add_argument("--button", choices=["left", "middle", "right"], default="left")
    add_common_runtime_flags(mouse_down)
    mouse_down.set_defaults(func=cmd_mouse_down)

    mouse_up = subparsers.add_parser("mouse-up", help="Release a mouse button")
    mouse_up.add_argument("--x", type=int)
    mouse_up.add_argument("--y", type=int)
    mouse_up.add_argument("--button", choices=["left", "middle", "right"], default="left")
    add_common_runtime_flags(mouse_up)
    mouse_up.set_defaults(func=cmd_mouse_up)

    type_cmd = subparsers.add_parser("type", help="Type text with optional interval")
    type_cmd.add_argument("--text", required=True)
    type_cmd.add_argument("--interval", type=float, default=0.0)
    type_cmd.add_argument("--enter", action="store_true")
    add_common_runtime_flags(type_cmd)
    type_cmd.set_defaults(func=cmd_type)

    press = subparsers.add_parser("press", help="Press a keyboard key one or more times")
    press.add_argument("--key", required=True)
    press.add_argument("--presses", type=int, default=1)
    press.add_argument("--interval", type=float, default=0.0)
    add_common_runtime_flags(press)
    press.set_defaults(func=cmd_press)

    hotkey = subparsers.add_parser("hotkey", help="Send a multi-key hotkey combination")
    hotkey.add_argument("--keys", nargs="+", required=True)
    hotkey.add_argument("--interval", type=float, default=0.0)
    add_common_runtime_flags(hotkey)
    hotkey.set_defaults(func=cmd_hotkey)

    scroll = subparsers.add_parser("scroll", help="Scroll vertically at current or target coordinates")
    scroll.add_argument("--clicks", type=int, required=True)
    scroll.add_argument("--x", type=int)
    scroll.add_argument("--y", type=int)
    add_common_runtime_flags(scroll)
    scroll.set_defaults(func=cmd_scroll)

    screenshot = subparsers.add_parser("screenshot", help="Save a screenshot to a file")
    screenshot.add_argument("--path", required=True)
    screenshot.add_argument("--x", type=int)
    screenshot.add_argument("--y", type=int)
    screenshot.add_argument("--width", type=int)
    screenshot.add_argument("--height", type=int)
    add_common_runtime_flags(screenshot)
    screenshot.set_defaults(func=cmd_screenshot)

    wait = subparsers.add_parser("wait", help="Sleep for a number of seconds")
    wait.add_argument("--seconds", type=float, required=True)
    wait.set_defaults(func=cmd_wait)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
