import flet as ft
import math

def main(page: ft.Page):
    page.title = "VSWR計算"
    page.theme_mode = ft.ThemeMode.LIGHT
    # スマホ画面でスクロールできるように設定
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 15

    # --- 状態管理用（リアルタイム計算用） ---
    # タブ1: VSWR用
    pf_input = ft.TextField(label="前進電力 Pf (W)", value="3.96", keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.colors.RED_400, border_width=2, on_change=lambda e: calculate_vswr())
    pr_input = ft.TextField(label="反射電力 Pr (W)", value="0.03", keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.colors.BLUE_400, border_width=2, on_change=lambda e: calculate_vswr())
    result_status = ft.Text(value="判定：良", size=24, color=ft.colors.GREEN, weight=ft.FontWeight.BOLD)
    result_vswr = ft.Text(value="3.110", size=36, weight=ft.FontWeight.BOLD)

    # タブ2: 波長用
    freq_input = ft.TextField(label="使用周波数 (MHz)", value="71.790", keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: calculate_wavelength())
    vfactor_input = ft.TextField(label="同軸短縮率 (例: 10D-2Vは0.67)", value="0.67", keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: calculate_wavelength())
    
    w_1_free = ft.Text(value="0.000 m", size=16)
    w_1_coax = ft.Text(value="(0.000 m)", size=16, color=ft.colors.BLUE_900)
    w_2_free = ft.Text(value="0.000 m", size=16)
    w_2_coax = ft.Text(value="(0.000 m)", size=16, color=ft.colors.BLUE_900)
    w_4_free = ft.Text(value="0.000 m", size=16)
    w_4_coax = ft.Text(value="(0.000 m)", size=16, color=ft.colors.BLUE_900)
    
    n_input = ft.TextField(label="倍数を選択 (n倍)", value="12", keyboard_type=ft.KeyboardType.NUMBER, on_change=lambda e: calculate_wavelength())
    recommended_text = ft.Text(value="推奨ケーブル長: 0.000 m", size=18, color=ft.colors.GREEN_700, weight=ft.FontWeight.BOLD)

    # --- 計算ロジック ---
    def calculate_vswr():
        try:
            pf = float(pf_input.value)
            pr = float(pr_input.value)
            if pf <= 0:
                result_status.value = "Pfに0より大きい値を入力してください"
                result_status.color = ft.colors.ORANGE_700
                result_vswr.value = "---"
            else:
                rho = math.sqrt(pr / pf)
                if rho < 1:
                    vswr = (1 + rho) / (1 - rho)
                    result_vswr.value = f"{vswr:.3f}"
                    if vswr < 1.5:
                        result_status.value = "判定：良"
                        result_status.color = ft.colors.GREEN
                    else:
                        result_status.value = "判定：要調整"
                        result_status.color = ft.colors.RED
                else:
                    result_vswr.value = "∞"
                    result_status.value = "判定：要調整"
                    result_status.color = ft.colors.RED
        except ValueError:
            result_vswr.value = "入力エラー"
            result_status.value = "数値を正しく入力してください"
        page.update()

    def calculate_wavelength():
        try:
            freq = float(freq_input.value)
            vf = float(vfactor_input.value)
            n = int(n_input.value) if n_input.value else 0

            if freq > 0:
                lambda_free = 300 / freq
                lambda_coax = lambda_free * vf

                w_1_free.value = f"{lambda_free:.3f} m"
                w_1_coax.value = f"({lambda_coax:.3f} m)"
                w_2_free.value = f"{lambda_free/2:.3f} m"
                w_2_coax.value = f"({lambda_coax/2:.3f} m)"
                w_4_free.value = f"{lambda_free/4:.3f} m"
                w_4_coax.value = f"({lambda_coax/4:.3f} m)"

                recommended_len = (lambda_coax / 2) * n
                recommended_text.value = f"推奨ケーブル長 ({n}倍): {recommended_len:.3f} m"
            else:
                recommended_text.value = "周波数には0より大きい値を入力してください"
        except ValueError:
            pass
        page.update()

    # --- 初回計算実行 ---
    calculate_vswr()
    calculate_wavelength()

    # --- 画面レイアウトの組み立て ---
    
    # ヘッダー（クレジット付き）
    header = ft.Row(
        [
            ft.Text("📡 VSWR計算", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("開発/制作：緒方", size=12, color=ft.colors.GREY_600)
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # タブ1の中身
    tab1_content = ft.Container(
        content=ft.Column([
            ft.Text("📊 VSWR測定・判定", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
            ft.Row([pf_input, pr_input], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.Column([
                    ft.Text("計算結果", size=14, color=ft.colors.GREY_700),
                    result_status,
                    ft.Text("VSWR値:", size=12, color=ft.colors.GREY_600),
                    result_vswr
                ]),
                bgcolor=ft.colors.GREY_100,
                padding=15,
                border_radius=10,
                border=ft.border.only(left=ft.border.BorderSide(5, ft.colors.BLUE_700))
            ),
            ft.Divider(),
            ft.Text("📝 VSWR計算式", size=16, weight=ft.FontWeight.BOLD),
            ft.Image(src="https://latex.codecogs.com/png.image?large&space;color{DarkBlue}VSWR=\frac{1+\sqrt{P_r/P_f}}{1-\sqrt{P_r/P_f}}", height=50),
            ft.Container(
                content=ft.Column([
                    ft.Text("【凡例】", weight=ft.FontWeight.BOLD),
                    ft.Text("Pf ：前進電力 (Forward Power)", color=ft.colors.RED_700, weight=ft.FontWeight.BOLD),
                    ft.Text("Pr ：反射電力 (Reflected Power)", color=ft.colors.BLUE_700, weight=ft.FontWeight.BOLD),
                ]),
                bgcolor=ft.colors.GREY_50,
                padding=10,
                border_radius=5,
                border=ft.border.all(1, ft.colors.GREY_300)
            )
        ], spacing=15),
        padding=10
    )

    # タブ2の中身
    tab2_content = ft.Container(
        content=ft.Column([
            ft.Text("📏 波長(λ)および同軸長計算", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_700),
            freq_input,
            vfactor_input,
            ft.Divider(),
            ft.Text("### 波長計算結果", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Column([ft.Text("1λ", weight=ft.FontWeight.BOLD), w_1_free, w_1_coax], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([ft.Text("1/2λ", weight=ft.FontWeight.BOLD), w_2_free, w_2_coax], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([ft.Text("1/4λ", weight=ft.FontWeight.BOLD), w_4_free, w_4_coax], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ft.Divider(),
            ft.Text("### 同軸ケーブル推奨長", size=16, weight=ft.FontWeight.BOLD),
            n_input,
            ft.Container(content=recommended_text, bgcolor=ft.colors.GREEN_50, padding=15, border_radius=5)
        ], spacing=15),
        padding=10
    )

    # タブの配置
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="VSWR計算", content=tab1_content),
            ft.Tab(text="波長・ケーブル長", content=tab2_content),
        ],
        expand=1
    )

    # 戻るボタン（ポータルサイト連携用リンクボタン）
    back_button = ft.ElevatedButton(
        text="🏠 戻る",
        color=ft.colors.WHITE,
        bgcolor=ft.colors.LIGHT_BLUE_500,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=150,
        on_click=lambda e: page.launch_url("https://7fjndw39dicdzckugyepb2.streamlit.app/")
    )

    # ページ全体に配置
    page.add(
        header,
        ft.Divider(),
        tabs,
        ft.Divider(),
        ft.Row([back_button], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
