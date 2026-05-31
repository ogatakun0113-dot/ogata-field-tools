import flet as ft
import math

def main(page: ft.Page):
    page.title = "VSWR計算ツール"
    
    # 入力欄や結果表示のパーツを作る
    ref_input = ft.TextField(label="反射係数（Γ）または進行・反射電力")
    result_text = ft.Text(value="結果がここに表示されます", size=20)
    
    def calculate_vswr(e):
        # ここにVSWRの計算ロジックを書く
        # 例: vswr = (1 + r) / (1 - r)
        result_text.value = f"VSWR: {計算結果}"
        page.update()
        
    calc_button = ft.ElevatedButton("計算する", on_click=calculate_vswr)
    
    # 画面にパーツを並べる
    page.add(ref_input, calc_button, result_text)

ft.app(target=main)
