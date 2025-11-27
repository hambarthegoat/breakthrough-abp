from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QWidget

from view.styles import StyleSheets


class MetricsPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.depth_label = None
        self.nodes_label = None
        self.time_label = None
        self.complexity_label = None
        self.big_o_label = None
        self.eval_label = None
        self.status_label = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("AI Performance Metrics")
        title.setStyleSheet(StyleSheets.LABEL_TITLE)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        metrics_group = QGroupBox("Current Analysis")
        metrics_group.setStyleSheet(StyleSheets.GROUP_BOX)

        metrics_layout = QVBoxLayout()
        metrics_layout.setSpacing(12)

        self.depth_label = self._create_metric_label("Search Depth:", "—")
        self.nodes_label = self._create_metric_label("Nodes Visited:", "—")
        self.time_label = self._create_metric_label("Execution Time:", "—")
        self.complexity_label = self._create_metric_label("Branching Factor:", "—")
        self.big_o_label = self._create_metric_label("Complexity:", "—")
        self.eval_label = self._create_metric_label("Position Score:", "—")

        metrics_layout.addWidget(self.depth_label)
        metrics_layout.addWidget(self.nodes_label)
        metrics_layout.addWidget(self.time_label)
        metrics_layout.addWidget(self.complexity_label)
        metrics_layout.addWidget(self.big_o_label)
        metrics_layout.addWidget(self.eval_label)

        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)

        self.status_label = QLabel("⚪ Waiting")
        self.status_label.setStyleSheet(
            StyleSheets.STATUS_LABEL.format(color="#90EE90")
        )
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addStretch()
        self.setLayout(layout)

    def _create_metric_label(self, title: str, value: str) -> QLabel:
        label = QLabel(f"{title}\n  {value}")
        label.setStyleSheet(StyleSheets.METRIC_LABEL)
        return label

    def update_metrics(self, metrics: dict):
        depth = metrics.get("depth", "—")
        nodes = metrics.get("nodes_visited", "—")
        exec_time = metrics.get("execution_time", "—")
        branch_factor = metrics.get("branching_factor", "—")
        evaluation = metrics.get("evaluation", "—")

        self.depth_label.setText(f"Search Depth:\n  {depth}")

        if isinstance(nodes, int):
            self.nodes_label.setText(f"Nodes Visited:\n  {nodes:,}")
        else:
            self.nodes_label.setText(f"Nodes Visited:\n  {nodes}")

        if isinstance(exec_time, float):
            self.time_label.setText(f"Execution Time:\n  {exec_time:.3f}s")
        else:
            self.time_label.setText(f"Execution Time:\n  {exec_time}")

        if isinstance(branch_factor, float):
            self.complexity_label.setText(f"Branching Factor:\n  {branch_factor:.2f}")
            self.big_o_label.setText(f"Complexity:\n  O({branch_factor:.1f}^{depth})")
        else:
            self.complexity_label.setText(f"Branching Factor:\n  {branch_factor}")
            self.big_o_label.setText(f"Complexity:\n  —")

        if isinstance(evaluation, (int, float)):
            self.eval_label.setText(f"Position Score:\n  {evaluation:+.1f}")
        else:
            self.eval_label.setText(f"Position Score:\n  {evaluation}")

    def set_status(self, status: str, color: str = None):
        if color is None:
            color = "#90EE90"

        self.status_label.setText(status)
        self.status_label.setStyleSheet(StyleSheets.STATUS_LABEL.format(color=color))

    def reset_metrics(self):
        self.depth_label.setText("Search Depth:\n  —")
        self.nodes_label.setText("Nodes Visited:\n  —")
        self.time_label.setText("Execution Time:\n  —")
        self.complexity_label.setText("Branching Factor:\n  —")
        self.big_o_label.setText("Complexity:\n  —")
        self.eval_label.setText("Position Score:\n  —")
        self.set_status("Waiting", "#90EE90")
