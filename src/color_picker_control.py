import re
import flet as ft  # type: ignore


class ColorPickerControl(ft.Column):
    """カラーピッカー画面"""

    def __init__(self, preview_visible=False, on_change=None):
        """コンストラクタ"""
        super().__init__()
        self.preview_visible = preview_visible
        self.input_regex = r"^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$"
        self.red = 0
        self.green = 0
        self.blue = 0
        self.previous_red = self.red
        self.previous_green = self.green
        self.previous_blue = self.blue
        self.preview_radius = 50
        self.input_width = 60
        self.controls = [self.build()]
        self.on_change = on_change

    def rgb_to_hex(self, r, g, b):
        """RGBを16進数に変換"""
        return f"#{int(r):02X}{int(g):02X}{int(b):02X}"

    def build(self):
        """ビルド"""
        # 色表示エリア
        self.color_display = ft.Container(
            # self.red, self.green, self.blue を使って色を表示
            bgcolor=self.rgb_to_hex(self.red, self.green, self.blue),
            width=self.preview_radius * 2,
            height=self.preview_radius * 2,
            border_radius=self.preview_radius,
            border=ft.border.all(1, ft.colors.BLACK),
            visible=self.preview_visible,
        )
        # スライダー Red - テキストフィールド Red (0-255)
        self.red_slider_label = ft.Text("Red")
        self.red_slider = ft.Slider(
            min=0,
            max=255,
            value=self.red,
            expand=True,
            on_change=self.on_change_red,
        )
        self.red_text_field = ft.TextField(
            value=str(self.red),
            expand=False,
            width=self.input_width,
            on_blur=self.on_blur_red,
        )
        # スライダー Green - テキストフィールド Green (0-255)
        self.green_slider_label = ft.Text("Green")
        self.green_slider = ft.Slider(
            min=0,
            max=255,
            value=self.green,
            expand=True,
            on_change=self.on_change_green,
        )
        self.green_text_field = ft.TextField(
            value=str(self.green),
            expand=False,
            width=self.input_width,
            on_blur=self.on_blur_green,
        )
        # スライダー Blue - テキストフィールド Blue (0-255)
        self.blue_slider_label = ft.Text("Blue")
        self.blue_slider = ft.Slider(
            min=0,
            max=255,
            value=self.blue,
            expand=True,
            on_change=self.on_change_blue,
        )
        self.blue_text_field = ft.TextField(
            value=str(self.blue),
            expand=False,
            width=self.input_width,
            on_blur=self.on_blur_blue,
        )
        # ラベルの幅を揃える
        self.red_slider_label.width = 50
        self.green_slider_label.width = 50
        self.blue_slider_label.width = 50

        return ft.Column(
            [
                # 色表示エリア
                self.color_display,
                # スライダー、テキストフィールド
                ft.Row(
                    [
                        self.red_slider_label,
                        self.red_slider,
                        self.red_text_field,
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        self.green_slider_label,
                        self.green_slider,
                        self.green_text_field,
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        self.blue_slider_label,
                        self.blue_slider,
                        self.blue_text_field,
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def on_change_red(self, e):
        """Redのスライダーが変更されたときの処理"""
        self.red = round(e.control.value)
        self.previous_red = self.red
        self.red_text_field.value = str(self.red)
        self.color_display.bgcolor = self.rgb_to_hex(self.red, self.green, self.blue)
        self.update()

    def on_blur_red(self, e):
        """Redのテキストフィールドがフォーカスを失ったときの処理"""
        # 0-255の範囲外の場合は前の値に戻す
        if not re.match(self.input_regex, e.control.value):
            self.red = self.previous_red
            self.red_text_field.value = str(self.previous_red)
            self.red_slider.value = self.previous_red
        else:
            self.previous_red = int(e.control.value)
            self.red = int(e.control.value)
            self.red_slider.value = self.red
            if self.on_change:
                self.on_change(self.red, self.green, self.blue)
        self.color_display.bgcolor = self.rgb_to_hex(self.red, self.green, self.blue)
        self.update()

    def on_change_green(self, e):
        """Greenのスライダーが変更されたときの処理"""
        self.green = round(e.control.value)
        self.previous_green = self.green
        self.green_text_field.value = str(self.green)
        self.color_display.bgcolor = self.rgb_to_hex(self.red, self.green, self.blue)
        self.update()

    def on_blur_green(self, e):
        """Greenのテキストフィールドがフォーカスを失ったときの処理"""
        # 0-255の範囲外の場合は前の値に戻す
        if not re.match(self.input_regex, e.control.value):
            self.green = self.previous_green
            self.green_text_field.value = str(self.previous_green)
            self.green_slider.value = self.previous_green
        else:
            self.previous_green = int(e.control.value)
            self.green = int(e.control.value)
            self.green_slider.value = self.green
            if self.on_change:
                self.on_change(self.red, self.green, self.blue)
        self.color_display.bgcolor = self.rgb_to_hex(self.red, self.green, self.blue)
        self.update()

    def on_change_blue(self, e):
        """Blueのスライダーが変更されたときの処理"""
        self.blue = round(e.control.value)
        self.previous_blue = self.blue
        self.blue_text_field.value = str(self.blue)
        self.color_display.bgcolor = self.rgb_to_hex(self.red, self.green, self.blue)
        self.update()

    def on_blur_blue(self, e):
        """Blueのテキストフィールドがフォーカスを失ったときの処理"""
        # 0-255の範囲外の場合は前の値に戻す
        if not re.match(self.input_regex, e.control.value):
            self.blue = self.previous_blue
            self.blue_text_field.value = str(self.previous_blue)
            self.blue_slider.value = self.previous_blue
        else:
            self.previous_blue = int(e.control.value)
            self.blue = int(e.control.value)
            self.blue_slider.value = self.blue
            if self.on_change:
                self.on_change(self.red, self.green, self.blue)
        self.color_display.bgcolor = self.rgb_to_hex(self.red, self.green, self.blue)
        self.update()
