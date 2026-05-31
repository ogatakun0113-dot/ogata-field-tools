import flet as ft
import math

def main(page: ft.Page):
    page.title = "VSWR計算ツール"
    page.padding = 20
    page.scroll = "adaptive"

    pf_input = ft.TextField(label="進行電力 Pf (W)", value="10")
    pr_input = ft.TextField(label="反射電力 Pr (W)", value="0.1")
    
    result_vswr = ft.Text(value="VSWR: --", size=24, color="blue")
    result_rho = ft.Text(value="反射係数 (Γ): --", size=16)

    def calculate_vswr(e):
        try:
            pf = float(pf_input.value)
            pr = float(pr_input.value)

            if pf <= 0 or pr < 0 or pr > pf:
                result_vswr.value = "エラー: 入力値が不正です"
                page.update()
                return

            rho = math.sqrt(pr / pf)
            vswr_val = (1 + rho) / (1 - rho)

            result_vswr.value = f"VSWR: {vswr_val:.3f}"
            result_rho.value = f"反射係数 (Γ): {rho:.4f}"
        except ValueError:
            result_vswr.value = "エラー: 数値を入力してください"
        
        page.update()

    calc_button = ft.ElevatedButton("計算する", on_click=calculate_vswr)

    page.add(
        ft.Text("VSWR 計算ツール", size=28),
        ft.Divider(),
        pf_input,
        pr_input,
        calc_button,
        ft.Divider(),
        result_vswr,
        result_rho
    )

ft.app(target=main)
