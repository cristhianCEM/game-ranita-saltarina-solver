import arcade
import arcade.gui

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
PADDING = 10
GRID_MIN = 1
GRID_MAX = 20

class GridButton(arcade.gui.UIFlatButton):
    def __init__(self, row, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = row
        self.col = col

    def on_click(self, event):
        print(f"Botón en ({self.row}, {self.col}) presionado")

class ButtonGridWindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Rejilla Dinámica de Botones")
        arcade.set_background_color(arcade.color.LIGHT_GRAY)

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        self.input_height = 3
        self.input_width = 4

        self.buttons_grid = []
        self.control_buttons = []

        self.setup_ui()

    def setup_ui(self):
        self.ui_manager.clear()
        self.create_control_buttons()
        self.create_grid_buttons(self.input_height, self.input_width)

    def create_grid_buttons(self, rows, cols):
        self.buttons_grid.clear()

        total_width = cols * (BUTTON_WIDTH + PADDING) - PADDING
        total_height = rows * (BUTTON_HEIGHT + PADDING) - PADDING
        offset_x = (WINDOW_WIDTH - total_width) // 2
        offset_y = 150  # Espacio reservado para botones de control

        for row in range(rows):
            for col in range(cols):
                x = offset_x + col * (BUTTON_WIDTH + PADDING) + BUTTON_WIDTH // 2
                y = offset_y + (rows - row - 1) * (BUTTON_HEIGHT + PADDING) + BUTTON_HEIGHT // 2

                button = GridButton(
                    row=row,
                    col=col,
                    text=f"{row},{col}",
                    x=x,
                    y=y,
                    width=BUTTON_WIDTH
                )
                self.ui_manager.add(button)
                self.buttons_grid.append(button)

    def create_control_buttons(self):
        self.control_buttons.clear()

        label = arcade.gui.UILabel(text="Grid size:", x=100, y=WINDOW_HEIGHT - 50)
        self.ui_manager.add(label)

        # Botones para height
        self.add_control("Height +", 250, lambda: self.adjust_grid("height", 1))
        self.add_control("Height –", 340, lambda: self.adjust_grid("height", -1))

        # Botones para width
        self.add_control("Width +", 450, lambda: self.adjust_grid("width", 1))
        self.add_control("Width –", 540, lambda: self.adjust_grid("width", -1))

        # Mostrar dimensiones actuales
        self.size_label = arcade.gui.UILabel(
            text=f"{self.input_height} x {self.input_width}",
            x=700,
            y=WINDOW_HEIGHT - 50,
            width=200
        )
        self.ui_manager.add(self.size_label)

    def add_control(self, text, x, callback):
        button = arcade.gui.UIFlatButton(text=text, x=x, y=WINDOW_HEIGHT - 50, width=80)
        button.on_click = lambda event: callback()
        self.ui_manager.add(button)
        self.control_buttons.append(button)

    def adjust_grid(self, axis, delta):
        if axis == "height":
            new_height = max(GRID_MIN, min(GRID_MAX, self.input_height + delta))
            if new_height != self.input_height:
                self.input_height = new_height
                self.setup_ui()
        elif axis == "width":
            new_width = max(GRID_MIN, min(GRID_MAX, self.input_width + delta))
            if new_width != self.input_width:
                self.input_width = new_width
                self.setup_ui()

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
        self.size_label.text = f"{self.input_height} x {self.input_width}"

if __name__ == "__main__":
    ButtonGridWindow()
    arcade.run()
