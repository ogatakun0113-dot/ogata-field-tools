import flet as ft
import math

def main(page: ft.Page):
    page.title = "緒方 Field Tools"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT  # 見やすい明るい画面

    # --- 1. dBm ⇄ dBμV 変換のロジック ---
    def convert_dbm_to_dbuv(e):
        try:
            val = float(txt_db_input.value)
            result = val + 107  # 50Ω基準
            lbl_db_result.value = f"結果: {result:.2f} dBμV"
            lbl_db_result.color = ft.Colors.BLUE_700
        except ValueError:
            lbl_db_result.value = "正しい数値を入力してください"
            lbl_db_result.color = ft.Colors.RED
        page.update()

    def convert_dbuv_to_dbm(e):
        try:
            val = float(txt_db_input.value)
            result = val - 107
            lbl_db_result.value = f"結果: {result:.2f} dBm"
            lbl_db_result.color = ft.Colors.BLUE_700
        except ValueError:
            lbl_db_result.value = "正しい数値を入力してください"
            lbl_db_result.color = ft.Colors.RED
        page.update()

    # --- 2. VSWR 計算のロジック ---
    def calculate_vswr(e):
        try:
            pf = float(txt_pf.value)
            pr = float(txt_pr.value)
            
            if pf <= 0:
                lbl_vswr_result.value = "進行波(Pf)には0より大きい値を入力してください"
                lbl_vswr_result.color = ft.Colors.RED
            elif pr < 0:
                lbl_vswr_result.value = "反射波(Pr)には0以上の値を入力してください"
                lbl_vswr_result.color = ft.Colors.RED
            elif pr >= pf:
                lbl_vswr_result.value = "エラー: 反射波が進行波以上になっています"
                lbl_vswr_result.color = ft.Colors.RED
            else:
                rho = math.sqrt(pr / pf)
                vswr = (1 + rho) / (1 - rho)
                lbl_vswr_result.value = f"計算結果 (VSWR): {vswr:.3f}"
                lbl_vswr_result.color = ft.Colors.GREEN_700
        except ValueError:
            lbl_vswr_result.value = "数値を正しく入力してください"
            lbl_vswr_result.color = ft.Colors.RED
        page.update()

    # --- 画面のデザイン配置 ---
    
    # 共通ヘッダー
    header = ft.Column([
        ft.Text("開発/制作：緒方", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.RIGHT, width=350),
        ft.Text("🌐 緒方 Field Tools", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider()
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # 【画面1】dBm/dBμV変換の配置
    txt_db_input = ft.TextField(label="変換する数値を入力", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    lbl_db_result = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
    
    view_db = ft.Column([
        ft.Text("📡 dBm ⇄ dBμV 相互変換", size=18, weight=ft.FontWeight.BOLD),
        txt_db_input,
        ft.Row([
            ft.ElevatedButton("dBm ➔ dBμV", on_click=convert_dbm_to_dbuv, height=45),
            ft.ElevatedButton("dBμV ➔ dBm", on_click=convert_dbuv_to_dbm, height=45),
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        lbl_db_result
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)

    # 【画面2】VSWR計算の配置
    txt_pf = ft.TextField(label="進行波電力 Pf (W)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    txt_pr = ft.TextField(label="反射波電力 Pr (W)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    lbl_vswr_result = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
    
    view_vswr = ft.Column([
        ft.Text("📡 VSWR 計算", size=18, weight=ft.FontWeight.BOLD),
        txt_pf,
        txt_pr,
        ft.ElevatedButton("VSWRを計算する", on_click=calculate_vswr, height=45, width=200),
        ft.Divider(),
        lbl_vswr_result
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, visible=False) # 最初は非表示

    # 安全な画面切り替えの仕組み
    def navigate(e):
        if e.control.selected_index == 0:
            view_db.visible = True
            view_vswr.visible = False
        else:
            view_db.visible = False
            view_vswr.visible = True
        page.update()

    # 画面下部に配置するナビゲーションバー
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=navigate,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CELL_TOWER, label="dBm⇄dBμV変換"),
            ft.NavigationBarDestination(icon=ft.Icons.ANALYTICS, label="VSWR計算"),
        ]
    )

    # 画面に部品を登録
    page.add(header, view_db, view_vswr)

# アプリの起動
ft.app(target=main)
