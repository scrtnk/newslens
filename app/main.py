# app/main.py
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # keep running after window closes

    # Must come AFTER QApplication() — that's what initialises NSApp under the hood.
    # Hides the app from the Dock so it behaves as a pure menu bar app.
    if sys.platform == "darwin":
        try:
            import AppKit
            AppKit.NSApp.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
        except Exception:
            pass  # non-fatal if pyobjc unavailable

    icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png")
    icon = QIcon(icon_path)

    from app.tray import TrayApp
    tray = TrayApp(icon)
    tray.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
