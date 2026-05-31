import flet as ft
import math

def main(page: ft.Page):
    page.title = "VSWR計算ツール"
    page.padding = 20
    page.scroll = "adaptive"

    # 入力欄の作成
    pf_input = ft.TextField(label="進行電力 Pf (W)", value="10", keyboard_type=ft.KeyboardType.NUMBER)
    pr_input = ft.TextField(label="反射電力 Pr (W)", value="0.1", keyboard_type=ft.KeyboardType.NUMBER)
    
    # 結果表示用のテキスト
    result_vswr = ft.Text(value="VSWR: --", size=24, weight=ft.FontWeight.BOLD, color="blue")
    result_rho = ft.Text(value="反射係数 (Γ): --", size=16)
    result_return_loss = ft.Text(value="リターンロス: -- dB", size=16)

    def calculate_vswr(e):
        try:
            # 入力された文字列を数値（浮動小数点数）に変換
            pf = float(pf_input.value)
            pr = float(pr_input.value)

            if pf <= 0:
                result_vswr.value = "エラー: Pfは0より大きい値を入力してください"
                page.update()
                return
            if pr < 0 or pr > pf:
                result_vswr.value = "エラー: Prの値が不正です"
                page.update()
                return

            # 1. 反射係数 Γ (Gamma) の計算
            rho = math.sqrt(pr / pf)

            # 2. VSWR の計算
            if rho >= 1.0:
                vswr_val = float('inf')
                vswr_str = "∞ (全反射)"
            else:
                vswr_val = (1 + rho) / (1 - rho)
                vswr_str = f"{vswr_val:.3f}"

            # 3. リターンロス (dB) の計算
            if pr == 0:
                rl_str = "∞"
            else:
                rl_val = 10 * math.log10(pf / pr)
                rl_str = f"{rl_val:.2f}"

            # 画面の表示を更新
            result_vswr.value = f"VSWR: {vswr_str}"
            result_rho.value = f"反射係数 (Γ): {rho:.4f}"
            result_return_loss.value = f"リターンロス: {rl_str} dB"

        except ValueError:
            result_vswr.value = "エラー: 正しい数値を入力してください"
        
        page.update()

    # 計算ボタン
    calc_button = ft.ElevatedButton("計算する", on_click=calculate_vswr, width=200)

    # 画面にパーツを配置する
    page.add(
        ft.Text("VSWR 計算ツール", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        pf_input,
        pr_input,
        ft.VerticalDivider(height=10),
        ft.Row([calc_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        result_vswr,
        result_rho,
        result_return_loss
    )

ft.app(target=main)
