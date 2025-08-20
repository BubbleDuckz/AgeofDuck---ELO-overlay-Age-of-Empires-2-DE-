import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QComboBox, QHBoxLayout, QLabel, QTextEdit,
    QSizePolicy, QPushButton, QGridLayout, QListWidget, QToolButton
    )
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QRectF
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPainterPath, QPainter
ACCENT = "#CDE6FF"
FG     = "#EAF2F9"
MUTED  = "#AFC4D8"

def rounded_icon(path: str, size: int, radius: int) -> QIcon:
    pm = QPixmap(path)
    if pm.isNull():
        return QIcon()
        pm = pm.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        out = QPixmap(size, size)
        out.fill(Qt.transparent)

        p = QPainter(out)
        p.setRenderHint(QPainter.Antialiasing, True)
        rect = QRectF(0, 0, size, size)

        clip = QPainterPath()
        clip.addRoundedRect(rect, radius, radius)
        p.setClipPath(clip)
        p.drawPixmap(rect, pm, QRectF(0, 0, pm.width(), pm.height()))
        p.end()

        return QIcon(out)

        class CollapsibleSection(QWidget):
    collapsed = pyqtSignal()  # notify parent so it can relayout
    toggled = pyqtSignal()

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.is_collapsed = True
        self.arrow_closed = "▶"
        self.arrow_open   = "▼"
        self.title = title

        self.toggle_button = QPushButton()
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.clicked.connect(self.toggle_section)
        self.toggle_button.setStyleSheet(f"""
            QPushButton {{
            text-align: left;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 6px;
            color: {FG};
            font-family: 'Segoe UI';
            font-size: 9pt;
            font-weight: 600;
            padding: 3px 4px;
            }}
            QPushButton:hover  {{ background: rgba(255,255,255,0.10); }}
            QPushButton:pressed{{ background: rgba(255,255,255,0.14); }}
            """)

        self.content = QWidget()
        self.content.setVisible(False)
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(8, 6, 8, 6)
        self.content_layout.setSpacing(6)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 6, 0, 0)
        self.main_layout.setSpacing(6)
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.content)

        self.update_button_text()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        def set_header_scale(self, radius_px: int, base_pt: int):
            self.toggle_button.setStyleSheet(f"""
                QPushButton {{
                text-align: left;
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: {radius_px}px;
                color: {FG};
                font-family: 'Segoe UI';
                font-size: {max(7, base_pt)}pt;
                font-weight: 600;
                padding: {max(2, base_pt//3)}px {max(3, base_pt//2)}px;
                }}
                QPushButton:hover  {{ background: rgba(255,255,255,0.10); }}
                QPushButton:pressed{{ background: rgba(255,255,255,0.14); }}
                """)

            def update_button_text(self):
                arrow = self.arrow_open if not self.is_collapsed else self.arrow_closed
                self.toggle_button.setText(f"{arrow}  {self.title}")

                def setContentLayout(self, layout):
                    self.content.setLayout(layout)

                    def setContentWidget(self, widget):
                        for i in reversed(range(self.content_layout.count())):
                            child = self.content_layout.takeAt(i)
                            if child.widget():
                                child.widget().deleteLater()
                                self.content_layout.addWidget(widget)

                                def toggle_section(self):
                                    if self.is_collapsed:
                                        self.expand_section()
                                    else:
                                        self.collapse_section()

                                        def expand_section(self):
                                            self.is_collapsed = False
                                            self.toggle_button.setChecked(True)
                                            self.content.setVisible(True)
                                            self.update_button_text()
        self.toggled.emit()  # <— fire on expand

        def collapse_section(self):
            self.is_collapsed = True
            self.toggle_button.setChecked(False)
            self.content.setVisible(False)
            self.update_button_text()
            self.collapsed.emit()
        self.toggled.emit()  # <— fire on collapse too


        class CivTooltip(QWidget):
            def __init__(self, civ_data_path="civ_data.json", assets_root=None, parent=None):
                super().__init__(parent)
                self.scale_factor = 1.0
        self._BASE_PT            = 9        # default body text in your stylesheet
        self._BASE_ICON          = 24       # civ icon square
        self._BASE_ICON_RADIUS   = 4
        self._BASE_SECTION_PAD   = (8, 6, 8, 6)
        self._BASE_SECTION_SPACE = 6
        self._BASE_HEAD_SPACE    = 8
        self._BASE_ROW_SPACE     = 6
        self._BASE_COMBO_H       = 32
        self._BASE_UNIT_BTN      = 45       # category buttons (and hero)
        self._BASE_UNIT_RADIUS   = 8
        self._BASE_RESULTS_SPACE = 8
        self._BASE_TEXT_MIN_H    = 100
        self.assets_root = assets_root or os.path.dirname(os.path.abspath(__file__))
        civ_data_path = civ_data_path if os.path.isabs(civ_data_path) \
        else os.path.join(self.assets_root, civ_data_path)
        units_db_path = os.path.join(self.assets_root, "units_db.json")
        with open(civ_data_path, "r", encoding="utf-8") as f:
            self.civ_data = json.load(f)
            if os.path.exists(units_db_path):
                with open(units_db_path, "r", encoding="utf-8") as f:
                    self.units_db = json.load(f)
                else:
                    self.units_db = {}
                    self.unit_counters = None
                    self.units_dir    = os.path.join(self.assets_root, "Units")
                    self.civicons_dir = os.path.join(self.assets_root, "CivIcons")

                    self.in_game = False
                    self._is_resetting = False
                    self.available_civs = []
        self.units_data = {}            # <- always defined
        self.current_profile_civ = None # overlay can set this
        self._last_civ_list_sig = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, self._s(2), self._s(2), 0)
        self.layout.setSpacing(self._s(self._BASE_ROW_SPACE))
        self.setStyleSheet(f"""
            QWidget {{
            background: transparent;        /* let overlay glass show through */
            color: {FG};
            font-family: 'Segoe UI';
            font-size: 9pt;
            }}
            QComboBox {{
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 6px;
            padding: 6px 10px;
            color: {FG};
            selection-background-color: rgba(255,255,255,0.12);
            }}
            QTextEdit {{
            background: rgba(0,0,0,0.22);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 6px;
            padding: 8px;
            color: {FG};
            }}
            QListWidget {{
            background: rgba(0,0,0,0.22);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 6px;
            color: {FG};
            }}
            QLabel#muted {{
            color: {MUTED};
            }}
            QLabel#accent {{
            color: {ACCENT};
            }}
            QLabel#good {{
            color: #34D399;         /* green */
            font-weight: 700;
            }}
            QLabel#bad {{
            color: #F87171;         /* red */
            font-weight: 700;
            }}
            """)
        civ_row = QHBoxLayout()
        civ_row.setContentsMargins(0, 0, 0, 0)
        civ_row.setSpacing(self._s(6))

        self.combo_civs = QComboBox()
        self.combo_civs.addItem("Select a civ")
        self.combo_civs.addItems(sorted(self.civ_data.keys()))
        self.combo_civs.currentTextChanged.connect(self.on_civ_changed)
        self.combo_civs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.combo_civs.setMaximumHeight(self._s(self._BASE_COMBO_H))

        self.civ_reset_button = QToolButton()
        self.civ_reset_button.setText("✕")
        self.civ_reset_button.setToolTip("Reset selection")
        self.civ_reset_button.setEnabled(False)
        self.civ_reset_button.clicked.connect(self.reset_civ_selection)
        self.civ_reset_button.setStyleSheet("""
            QToolButton {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 6px;
            padding: 0px 8px;
            color: rgba(255,255,255,0.92);
            }
            QToolButton:hover  { background: rgba(255,255,255,0.12); }
            QToolButton:pressed{ background: rgba(255,255,255,0.16); }
            """)

        civ_row.addWidget(self.combo_civs)
        civ_row.addWidget(self.civ_reset_button)
        self.layout.addLayout(civ_row)
        head = QHBoxLayout()
        head.setSpacing(self._s(self._BASE_HEAD_SPACE))
        head.setContentsMargins(0, 0, 0, 0)

        self.label_icon = QLabel()
        self.label_icon.setFixedSize(self._s(self._BASE_ICON), self._s(self._BASE_ICON))
        self.label_icon.setStyleSheet(
            f"border: 1px solid rgba(255,255,255,0.10); border-radius: {self._s(self._BASE_ICON_RADIUS)}px;"
            )
        self.label_icon.setScaledContents(True)
        head.addWidget(self.label_icon)

        self.label_name = QLabel("")
        self.label_name.setObjectName("accent")
        self.label_name.setStyleSheet(f"font-weight: 700; font-size: 11pt;")
        head.addWidget(self.label_name, 1)

        self.layout.addLayout(head)

        self.label_team_bonus = QLabel("")
        self.label_team_bonus.setObjectName("muted")
        self.label_team_bonus.setWordWrap(True)
        self.layout.addWidget(self.label_team_bonus)
        self.section_bonuses    = CollapsibleSection("Civilization Bonuses")
        self.section_strengths  = CollapsibleSection("Strengths")
        self.section_weaknesses = CollapsibleSection("Weaknesses")
        self.section_strategies = CollapsibleSection("Strategies")
        self.section_units      = CollapsibleSection("Counter Unit Guide")
        self.layout.addWidget(self.section_bonuses)
        self.layout.addWidget(self.section_strengths)
        self.layout.addWidget(self.section_weaknesses)
        self.layout.addWidget(self.section_strategies)
        self.layout.addWidget(self.section_units)
        self.text_bonuses     = QTextEdit(); self.text_bonuses.setReadOnly(True)
        self.text_strength    = QTextEdit(); self.text_strength.setReadOnly(True)
        self.text_weaknesses  = QTextEdit(); self.text_weaknesses.setReadOnly(True)
        self.text_strategies  = QTextEdit(); self.text_strategies.setReadOnly(True)
        for t in (self.text_bonuses, self.text_strength, self.text_weaknesses, self.text_strategies):
            t.setMinimumHeight(self._s(self._BASE_TEXT_MIN_H))
            self.section_bonuses.setContentWidget(self.text_bonuses)
            self.section_strengths.setContentWidget(self.text_strength)
            self.section_weaknesses.setContentWidget(self.text_weaknesses)
            self.section_strategies.setContentWidget(self.text_strategies)
            self.section_bonuses.content_layout.setContentsMargins(*[self._s(v) for v in self._BASE_SECTION_PAD])
            self.section_bonuses.content_layout.setSpacing(self._s(self._BASE_SECTION_SPACE))
            for sec in (self.section_strengths, self.section_weaknesses, self.section_strategies, self.section_units):
                sec.content_layout.setContentsMargins(*[self._s(v) for v in self._BASE_SECTION_PAD])
                sec.content_layout.setSpacing(self._s(self._BASE_SECTION_SPACE))
                self.setup_unit_category()
                for w in (self.label_icon, self.label_name, self.label_team_bonus,
                  self.section_bonuses, self.section_strengths, self.section_weaknesses,
                  self.section_strategies, self.section_units):
                w.hide()
                for sec in (self.section_bonuses, self.section_strengths, self.section_weaknesses,
                    self.section_strategies, self.section_units):
                sec.collapsed.connect(self.on_section_collapsed)
                sec.toggled.connect(self.on_section_collapsed)

                self.combo_civs.setCurrentIndex(0)



                def _s(self, x: int | float) -> int:
                    return max(1, int(round(x * self.scale_factor)))
                    def setup_unit_category(self):
                        self.units_widget = QWidget()
                        self.units_layout = QVBoxLayout(self.units_widget)
                        self.units_layout.setContentsMargins(0, 0, 0, 0)
                        self.units_layout.setSpacing(self._s(6))

                        self.units_grid = QGridLayout()
                        self.units_grid.setSpacing(self._s(8))

                        self.unit_categories = [
                        ("Military",   "Barracksavailable.webp",       "Select a Barracks Unit to counter"),
                        ("Archery",    "Archeryrangeavailable.webp",   "Select an Archery Range Unit to counter"),
                        ("Cavalry",    "Stableavailable.webp",         "Select a Stable Unit to counter"),
                        ("Siege",      "Siegeworkshopavailable.webp",  "Select a Siege Workshop Unit to counter"),
                        ("Castle",     "Castleavailable.webp",         "Select a Castle Unit to counter"),
                        ("Monastery",  "Monasteryavailable.webp",      "Select a Monastery Unit to counter"),
                        ("Docks",      "Dockavailable.webp",           "Select a Dock Unit to counter"),
                        ]
                        self.category_aliases = {
                        "Military":  ["Military", "Barracks"],
                        "Archery":   ["Archery", "Archery Range", "Archery Ranges"],
                        "Cavalry":   ["Cavalry", "Stable", "Stables"],
                        "Siege":     ["Siege", "Siege Workshop", "Siege Workshops"],
                        "Castle":    ["Castle Units"],
                        "Monastery": ["Monastery", "Monastry", "Monastery/Church", "Church"],
                        "Dock":      ["Docks", "Dock", "Harbor", "Harbour"],
                        }

                        self.unit_buttons = {}
                        btn_size   = self._s(self._BASE_UNIT_BTN)
                        btn_radius = self._s(self._BASE_UNIT_RADIUS)

                        for idx, (cat, img_file, _placeholder) in enumerate(self.unit_categories):
                            row = idx // 6
                            col = idx % 6

                            btn = QPushButton()
                            btn.setFixedSize(btn_size, btn_size)
                            btn.setEnabled(False)

                            img_path = os.path.join(self.units_dir, img_file)
                            if os.path.exists(img_path):
                                btn.setIcon(rounded_icon(img_path, btn_size, btn_radius))
                                btn.setIconSize(QSize(btn_size, btn_size))
                            else:
                                btn.setText(cat)

                                btn.setStyleSheet(f"""
                                    QPushButton {{
                                    background: rgba(255,255,255,0.06);
                                    border: 1px solid rgba(255,255,255,0.10);
                                    border-radius: {btn_radius}px;
                                    color: #EAF2F9;
                                    padding: 0;
                                    }}
                                    QPushButton:hover  {{ background: rgba(255,255,255,0.10); }}
                                    QPushButton:pressed{{ background: rgba(255,255,255,0.14); }}
                                    QPushButton:disabled{{ opacity:0.5; }}
                                    """)
                                btn.clicked.connect(lambda _checked, c=cat: self.on_unit_category_clicked(c))
                                self.units_grid.addWidget(btn, row * 2, col)
                                self.unit_buttons[cat] = btn
                                row_after = (len(self.unit_categories) // 6) * 2 + 1
                                dropdown_row = QHBoxLayout()

                                self.unit_dropdown = QComboBox()
                                self.unit_dropdown.addItem("Select a Unit Category")
                                self.unit_dropdown.setEnabled(False)
                                self.unit_dropdown.currentIndexChanged.connect(self.on_unit_selected)
                                self.unit_dropdown.setMinimumHeight(self._s(28))
                                self.unit_dropdown.setMaximumHeight(self._s(self._BASE_COMBO_H))
                                dropdown_row.addWidget(self.unit_dropdown)

                                self.unit_reset_button = QToolButton()
                                self.unit_reset_button.setText("✕")
                                self.unit_reset_button.setToolTip("Reset unit selection")
                                self.unit_reset_button.setEnabled(False)
                                self.unit_reset_button.clicked.connect(self.reset_unit_selection)
                                self.unit_reset_button.setStyleSheet(f"""
                                    QToolButton {{
                                    background: rgba(255,255,255,0.08);
                                    border: 1px solid rgba(255,255,255,0.10);
                                    border-radius: {self._s(6)}px;
                                    padding: 0px {self._s(8)}px;
                                    color: rgba(255,255,255,0.92);
                                    }}
                                    QToolButton:hover  {{ background: rgba(255,255,255,0.12); }}
                                    QToolButton:pressed{{ background: rgba(255,255,255,0.16); }}
                                    """)
                                dropdown_row.addWidget(self.unit_reset_button)

                                self.units_grid.addLayout(dropdown_row, row_after, 0, 1, 6)
                                self.hero_button = QPushButton()
                                self.hero_button.setFixedSize(btn_size, btn_size)
                                hero_img_path = os.path.join(self.units_dir, "hero.webp")
                                if os.path.exists(hero_img_path):
                                    self.hero_button.setIcon(QIcon(hero_img_path))
                                    self.hero_button.setIconSize(self.hero_button.size())
                                    self.hero_button.clicked.connect(self.on_hero_button_clicked)
                                    self.hero_button.hide()
                                    self.units_grid.addWidget(self.hero_button, row_after + 1, 0)

                                    self.hero_dropdown = QComboBox()
                                    self.hero_dropdown.addItem("Select a Hero Unit to counter")
                                    self.hero_dropdown.setEnabled(False)
                                    self.hero_dropdown.currentIndexChanged.connect(self.on_unit_selected)
                                    self.hero_dropdown.hide()
                                    self.units_grid.addWidget(self.hero_dropdown, row_after + 2, 0)
                                    results_grid = QGridLayout()
                                    results_grid.setSpacing(self._s(self._BASE_RESULTS_SPACE))

                                    lbl_strong = QLabel("Strong Against")
                                    lbl_strong.setObjectName("good")

                                    lbl_counters = QLabel("Counter Units")
                                    lbl_counters.setObjectName("bad")

                                    self.unit_strong_list = QListWidget()
                                    self.unit_counters_list = QListWidget()

                                    results_grid.addWidget(lbl_strong, 0, 0)
                                    results_grid.addWidget(lbl_counters, 0, 1)
                                    results_grid.addWidget(self.unit_strong_list, 1, 0)
                                    results_grid.addWidget(self.unit_counters_list, 1, 1)
                                    self.units_layout.addLayout(self.units_grid)
                                    self.units_layout.addLayout(results_grid)
                                    self.section_units.setContentWidget(self.units_widget)


                                    def set_scale(self, factor: float, base_overlay_pt: int | None = None):
                                        """Scale the entire tooltip. Optionally pass overlay's computed base pt."""
                                        self.scale_factor = max(0.6, min(2.0, float(factor)))
                                        base_pt = base_overlay_pt if base_overlay_pt is not None else int(round(self._BASE_PT * self.scale_factor))
                                        base_pt = max(7, base_pt)
                                        self.setStyleSheet(self.styleSheet().replace("font-size: 9pt", f"font-size: {base_pt}pt"))
                                        self.combo_civs.setStyleSheet(f"""
                                            QComboBox {{
                                            background: rgba(255,255,255,0.06);
                                            border: 1px solid rgba(255,255,255,0.10);
                                            border-radius: {self._s(6)}px;
                                            padding: {self._s(6)}px {self._s(10)}px;
                                            color: {FG};
                                            selection-background-color: rgba(255,255,255,0.12);
                                            font-size: {base_pt}pt;
                                            }}
                                            """)
                                        self.label_name.setStyleSheet(f"font-weight: 700; font-size: {max(base_pt+2, 8)}pt; color: {ACCENT};")
                                        self.label_team_bonus.setStyleSheet(f"font-size: {base_pt}pt; color: {MUTED};")
                                        for t in (self.text_bonuses, self.text_strength, self.text_weaknesses, self.text_strategies):
                                            t.setStyleSheet(
                                                f"font-size: {base_pt}pt; "
                                                f"background: rgba(0,0,0,0.22); "
                                                f"border: 1px solid rgba(255,255,255,0.08); "
                                                f"border-radius: {self._s(6)}px; "
                                                f"padding: {self._s(8)}px; color: {FG};"
                                                )
                                            t.setMinimumHeight(self._s(self._BASE_TEXT_MIN_H))
                                            self.label_icon.setFixedSize(self._s(self._BASE_ICON), self._s(self._BASE_ICON))
                                            self.label_icon.setStyleSheet(
                                                f"border: 1px solid rgba(255,255,255,0.10); border-radius: {self._s(self._BASE_ICON_RADIUS)}px;"
                                                )
                                            for sec in (self.section_bonuses, self.section_strengths, self.section_weaknesses,
                                                self.section_strategies, self.section_units):
                                            sec.content_layout.setContentsMargins(*[self._s(v) for v in self._BASE_SECTION_PAD])
                                            sec.content_layout.setSpacing(self._s(self._BASE_SECTION_SPACE))
                                            sec.set_header_scale(self._s(6), base_pt)
                                            self.units_layout.setSpacing(self._s(6))
                                            self.units_grid.setSpacing(self._s(8))

                                            btn_size   = self._s(self._BASE_UNIT_BTN)
                                            btn_radius = self._s(self._BASE_UNIT_RADIUS)
                                            for cat, btn in self.unit_buttons.items():
                                                btn.setFixedSize(btn_size, btn_size)
                                                btn.setStyleSheet(
                                                    f"QPushButton {{ background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.10); "
                                                    f"border-radius: {btn_radius}px; color: #EAF2F9; padding: 0; }}"
                                                    "QPushButton:hover { background: rgba(255,255,255,0.10); }"
                                                    "QPushButton:pressed{ background: rgba(255,255,255,0.14); }"
                                                    "QPushButton:disabled{ opacity:0.5; }"
                                                    )
                                                btn.setIconSize(QSize(btn_size, btn_size))
                                                self.hero_button.setFixedSize(btn_size, btn_size)
                                                self.hero_button.setIconSize(self.hero_button.size())
                                                self.layout.invalidate(); self.layout.activate()
                                                self.adjustSize(); self.updateGeometry()
                                                top = self.window()
                                                if top and top is not self:
                                                    top.adjustSize(); top.updateGeometry()



                                                    def on_section_collapsed(self):
                                                        """Relayout and resize when any section is toggled."""
                                                        if hasattr(self, "layout"):
                                                            self.layout.invalidate()
                                                            self.layout.activate()

                                                            self.adjustSize()
                                                            self.updateGeometry()
                                                            parent = self.parentWidget()
                                                            if parent:
                                                                parent.adjustSize()
                                                                parent.updateGeometry()

                                                                top = self.window()
                                                                if top and top is not self:
                                                                    top.adjustSize()
                                                                    top.updateGeometry()
                                                                    def set_available_civs(self, civ_list):
                                                                        civs = sorted(set(civ_list)) if civ_list else sorted(self.civ_data.keys())
                                                                        sig = tuple(civs)
                                                                        if self._last_civ_list_sig == sig:
            return  # no change; leave UI alone
            self._last_civ_list_sig = sig
            self.available_civs = civs
            self.update_civ_dropdown(preserve_selection=True)

            def update_civ_dropdown(self, preserve_selection=False):
                prev = self.combo_civs.currentText()
                self.combo_civs.blockSignals(True)
                self.combo_civs.clear()
                self.combo_civs.addItem("Select a civ")
                self.combo_civs.addItems(self.available_civs)

                if preserve_selection and prev in self.available_civs:
                    self.combo_civs.setCurrentIndex(self.combo_civs.findText(prev))
                else:
                    self.combo_civs.setCurrentIndex(self.combo_civs.findText(prev) if prev in self.available_civs else 0)

                    self.combo_civs.blockSignals(False)

                    def reset_civ_selection(self):
                        if getattr(self, '_is_resetting', False):
                            return
                            self._is_resetting = True

                            self.combo_civs.blockSignals(True)
                            self.combo_civs.setCurrentIndex(0)
                            self.combo_civs.blockSignals(False)
                            self.civ_reset_button.setEnabled(False)
                            for btn in self.unit_buttons.values():
                                btn.setEnabled(False)
                                self.reset_unit_selection()
                                self.hero_button.hide()
                                self.hero_dropdown.hide()

                                self.on_civ_changed_waiting("Select a civ")
                                self._is_resetting = False
                                def _get_unit_relations(self, unit_name: str):
                                    """Return (strong_vs_list, countered_by_list) for a unit name from units_db."""
                                    data = self.units_db.get(unit_name, {})
                                    strong_vs = [
                                    d["unit"] for d in data.get("strong_vs", [])
                                    if isinstance(d, dict) and "unit" in d
                                    ]
                                    countered_by = [
                                    d["unit"] for d in data.get("countered_by", [])
                                    if isinstance(d, dict) and "unit" in d
                                    ]
                                    return strong_vs, countered_by

                                    def _filter_by_civ_availability(self, units: list[str]) -> list[str]:
                                        """Filter a list of unit names to only those buildable by the current profile civ (in-game)."""
                                        if not (self.in_game and self.current_profile_civ):
                                            return units
                                            civ_info = self.civ_data.get(self.current_profile_civ, {})
                                            civ_units_available = {}

                                            units_available = civ_info.get("unitsAvailable", {})
                                            unique_units = civ_info.get("unique_units_by_category", {})

                                            for _cat, units_dict in units_available.items():
                                                for u_name, available in units_dict.items():
                                                    if available:
                                                        civ_units_available[u_name] = True
                                                        for _cat, lst in unique_units.items():
                                                            for u_name in lst:
                                                                civ_units_available[u_name] = True

                                                                return [u for u in units if civ_units_available.get(u, False)]

                                                                def on_hero_button_clicked(self):
                                                                    self.hero_dropdown.setEnabled(True)
                                                                    self.hero_dropdown.setCurrentIndex(0)
                                                                    self.unit_strong_list.clear()
                                                                    self.unit_counters_list.clear()

                                                                    def on_unit_category_clicked(self, category):
                                                                        if not self.units_data:
                                                                            return
                                                                            self.current_unit_category = category
                                                                            self.unit_dropdown.clear()
                                                                            self.unit_dropdown.setEnabled(True)
                                                                            self.unit_reset_button.setEnabled(True)

                                                                            units_list = self.units_data.get(category, [])
                                                                            placeholder = next((ph for (cat, _img, ph) in self.unit_categories if cat == category), "Select a Unit")
                                                                            self.unit_dropdown.addItem(placeholder)
                                                                            for unit in units_list:
                                                                                self.unit_dropdown.addItem(unit)

                                                                                self.unit_strong_list.clear()
                                                                                self.unit_counters_list.clear()

                                                                                def on_unit_selected(self, index):
                                                                                    dropdown = self.sender() if isinstance(self.sender(), QComboBox) else None
                                                                                    if not dropdown or index == 0:
                                                                                        self.unit_strong_list.clear()
                                                                                        self.unit_counters_list.clear()
                                                                                        return

                                                                                        unit_name = dropdown.currentText()
                                                                                        strong_vs, countered_by = self._get_unit_relations(unit_name)
                                                                                        self.unit_strong_list.clear()
                                                                                        self.unit_counters_list.clear()

                                                                                        self.unit_strong_list.addItems(strong_vs if strong_vs else ["No data"])

                                                                                        if self.in_game and self.current_profile_civ:
                                                                                            counters_filtered = self._filter_by_civ_availability(countered_by)
                                                                                            self.unit_counters_list.addItems(
                                                                                                counters_filtered if counters_filtered else ["No counters available for this civ"]
                                                                                                )
                                                                                        else:
                                                                                            self.unit_counters_list.addItems(countered_by if countered_by else ["No counters found"])


                                                                                            def reset_unit_selection(self):
                                                                                                self.unit_dropdown.blockSignals(True)
                                                                                                self.unit_dropdown.clear()
                                                                                                self.unit_dropdown.addItem("Select a Unit Category")
                                                                                                self.unit_dropdown.setCurrentIndex(0)
                                                                                                self.unit_dropdown.blockSignals(False)
                                                                                                self.unit_strong_list.clear()
                                                                                                self.unit_counters_list.clear()
                                                                                                self.unit_dropdown.setEnabled(False)
                                                                                                self.unit_reset_button.setEnabled(False)
                                                                                                def on_civ_changed(self, civ_name):
                                                                                                    if self.in_game:
                                                                                                        self.on_civ_changed_in_game(civ_name)
                                                                                                    else:
                                                                                                        self.on_civ_changed_waiting(civ_name)

                                                                                                        def on_civ_changed_waiting(self, civ_name):
                                                                                                            self.civ_reset_button.setEnabled(civ_name != "Select a civ")

                                                                                                            if civ_name == "Select a civ":
                                                                                                                for w in (self.label_icon, self.label_name, self.label_team_bonus,
                                                                                                                  self.section_bonuses, self.section_strengths, self.section_weaknesses,
                                                                                                                  self.section_strategies, self.section_units):
                                                                                                                w.hide()
                                                                                                                self.text_bonuses.clear()
                                                                                                                self.text_strength.clear()
                                                                                                                self.text_weaknesses.clear()
                                                                                                                self.text_strategies.clear()
                                                                                                                self.label_name.clear()
                                                                                                                self.label_team_bonus.clear()
                                                                                                                self.label_icon.clear()
                                                                                                                for btn in self.unit_buttons.values():
                                                                                                                    btn.setEnabled(False)
                                                                                                                    self.reset_unit_selection()
                                                                                                                    self.updateGeometry(); self.adjustSize()
                                                                                                                    top = self.window(); 
                                                                                                                    if top: top.updateGeometry(); top.adjustSize()
                                                                                                                    return

                                                                                                                    civ = self.civ_data.get(civ_name, {})

                                                                                                                    self.label_name.setText(civ.get("civName", civ_name))
                                                                                                                    self.label_team_bonus.setText(f"<b>Team Bonus:</b> {civ.get('civTeamBonus', 'N/A')}")

                                                                                                                    icon_path = os.path.join(self.civicons_dir, f"{civ_name}_AoE2.webp")
                                                                                                                    if os.path.exists(icon_path):
                                                                                                                        self.label_icon.setPixmap(QPixmap(icon_path))
                                                                                                                        self.label_icon.show()
                                                                                                                    else:
                                                                                                                        self.label_icon.hide()

                                                                                                                        for w in (self.label_name, self.label_team_bonus,
                                                                                                                          self.section_bonuses, self.section_strengths, self.section_weaknesses,
                                                                                                                          self.section_strategies, self.section_units):
                                                                                                                        w.show()
                                                                                                                        civ_strength_raw = civ.get("civStrength", "No strength info available.")
                                                                                                                        parts = civ_strength_raw.split("\n\n", 1)
                                                                                                                        civ_bonuses = parts[0] if parts else ""
                                                                                                                        civ_strength = parts[1] if len(parts) == 2 else ""

                                                                                                                        self.text_bonuses.setPlainText(civ_bonuses)
                                                                                                                        self.text_strength.setPlainText(civ_strength)
                                                                                                                        self.text_weaknesses.setPlainText(civ.get("civWeakness", "No weakness info available."))
                                                                                                                        self.text_strategies.setPlainText(civ.get("civStrategy", "No strategy info available."))
                                                                                                                        self.units_data = {}
                                                                                                                        units_available = civ.get("unitsAvailable", {}) or {}
                                                                                                                        unique_units     = civ.get("unique_units_by_category", {}) or {}
                                                                                                                        for ui_cat, _img, _ph in self.unit_categories:
                                                                                                                            aliases = self.category_aliases.get(ui_cat, [ui_cat])
                                                                                                                            names = []
                                                                                                                            for k in aliases:
                                                                                                                                d = units_available.get(k)
                                                                                                                                if isinstance(d, dict):
                                                                                                                                    names.extend([u for u, ok in d.items() if ok])
                                                                                                                                    for k in aliases:
                                                                                                                                        lst = unique_units.get(k)
                                                                                                                                        if isinstance(lst, list):
                                                                                                                                            names.extend(lst)
                                                                                                                                            self.units_data[ui_cat] = sorted(dict.fromkeys(names))
                                                                                                                                            for cat, btn in self.unit_buttons.items():
                                                                                                                                                btn.setEnabled(bool(self.units_data.get(cat)))
                                                                                                                                                hero_units = units_available.get("Hero Unit", {})
                                                                                                                                                available_heroes = [h for h, ok in hero_units.items() if ok]
                                                                                                                                                if available_heroes:
                                                                                                                                                    self.hero_button.show()
                                                                                                                                                    self.hero_dropdown.show()
                                                                                                                                                    self.hero_dropdown.setEnabled(True)
                                                                                                                                                    self.hero_dropdown.blockSignals(True)
                                                                                                                                                    self.hero_dropdown.clear()
                                                                                                                                                    self.hero_dropdown.addItem("Select a Hero Unit")
                                                                                                                                                    for hero in available_heroes:
                                                                                                                                                        self.hero_dropdown.addItem(hero)
                                                                                                                                                        self.hero_dropdown.blockSignals(False)
                                                                                                                                                    else:
                                                                                                                                                        self.hero_button.hide()
                                                                                                                                                        self.hero_dropdown.hide()
                                                                                                                                                        self.hero_dropdown.setEnabled(False)

                                                                                                                                                        self.updateGeometry(); self.adjustSize()

                                                                                                                                                        def on_civ_changed_in_game(self, civ_name):
                                                                                                                                                            if civ_name == "Select a civ" or civ_name not in getattr(self, 'available_civs', []):
                                                                                                                                                                self.reset_civ_selection()
                                                                                                                                                                return
                                                                                                                                                                self.on_civ_changed_waiting(civ_name)
                                                                                                                                                                def set_game_state(self, in_game: bool):
                                                                                                                                                                    if self.in_game == in_game:
            return  # nothing to do
            self.in_game = in_game
            cur = self.combo_civs.currentText()
            if cur and cur != "Select a civ":
                self.on_civ_changed(cur)


                def set_font_size(self, size: int):
                    base = size
                    self.setStyleSheet(self.styleSheet().replace("font-size: 9pt", f"font-size: {base}pt"))
                    self.combo_civs.setStyleSheet(f"""
                        QComboBox {{
                        background: rgba(255,255,255,0.06);
                        border: 1px solid rgba(255,255,255,0.10);
                        border-radius: 6px;
                        padding: 6px 10px;
                        color: {FG};
                        selection-background-color: rgba(255,255,255,0.12);
                        font-size: {base}pt;
                        }}
                        """)
                    self.label_name.setStyleSheet(f"font-weight: 700; font-size: {base}pt; color: {ACCENT};")
                    self.label_team_bonus.setStyleSheet(f"font-size: {base}pt; color: {MUTED};")
                    for t in (self.text_bonuses, self.text_strength, self.text_weaknesses, self.text_strategies):
                        t.setStyleSheet(f"font-size: {base}pt; background: rgba(0,0,0,0.22); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px; padding: 8px; color: {FG};")

                        def select_civ(self, civ_name: str):
                            idx = self.combo_civs.findText(civ_name)
                            if idx >= 0:
                                self.combo_civs.setCurrentIndex(idx)
