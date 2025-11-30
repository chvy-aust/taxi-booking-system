from typing import override
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout

from src.scenes.base import BaseScene
from src.widgets.button import Button


class SplashScreen(BaseScene):
    """
    Splash screen class to be displayed at application launch.
    Allows navigation to login and register screen.
    """

    def __init__(self, signals):
        super().__init__(
            scene_name='splash',
            signals=signals
        )
        self.signals = signals
        self._load_ui()

    @override
    def _load_ui(self):
        """Setup UI layout for scene."""
        label = QLabel("Taxi Booking System")

        # Make buttons.
        register_btn = Button("Register", self.signals.request_register)
        login_btn = Button("Login", self.signals.request_login)

        # Button container + spacing.
        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(register_btn)
        btns.addWidget(login_btn)
        btns.addStretch()

        # Layout window elements + spacing.
        container = QVBoxLayout()
        container.addStretch()
        container.addWidget(label)
        container.addLayout(btns)
        container.addStretch()

        self.setLayout(container)