import requests
from tqdm import tqdm
import os
import re
from PIL import Image, ImageDraw, ImageFont
import time

map_folder_name = "マップ"
cosmetics_folder_name = "NEWコスメティクス"
lobby_folder_name = "ロビー"
mnemonicfolder_path = "プレイリスト"
newssave_folder = "ニュースフィード"
allcosmetics_folder_name = "全コスメティクス"
map_file_name = "map.png"
cosmetics_file_name = "cosmetics_data.txt"
lobby_file_name = "ロビー背景.png"
decrypted_folder_name = "複合化アイテム"

#APIのURL
aes_url = "https://fortnitecentral.genxgames.gg/api/v1/aes"
cosmetics_base_url = "https://fortnite-api.com/v2/cosmetics/br/search/all?dynamicPakId={}&language=ja"
font_path = "GENEIPOPLEPW-BK.TTF"
map_url = "https://fortnite-api.com/images/map_ja.png"
newcosmetics_url = "https://fortnite-api.com/v2/cosmetics/new?language=ja"
allcosmetics_url = "https://fortnite-api.com/v2/cosmetics?language=ja"
lobby_url = "https://fljpapi2-8h78.onrender.com/api/lobby"
newsapi_url = "https://fljpapi-c73j.onrender.com/api/v2/news?platform=Windows&language=ja&country=JN&battlepass=true&battlepassLevel=100&tags=Product.BR"
mnemonicurl = "https://fljpapi-c73j.onrender.com/api/v2/links/fn/set_br_playlists"

# アスキーアートで「FLeak」を表示
def print_fleak():
    fleak_art = """
    FFFFFF   L          EEEEE    AAAAA    K   K
    F        L          E       A     A   K  K
    FFFF     L          EEEE    AAAAAAA   KKK
    F        L          E       A     A   K  K
    F        LLLLL      EEEEE   A     A   K   K

    """
    print(fleak_art)

print_fleak()

def print_kuuhaku():
    kuuhaku = """
    """
    print(kuuhaku)

while True:
    # 処理選択メニュー
    print_kuuhaku()
    print("====== 処理選択メニュー ======")
    print("1. 最新のマップをダウンロード")
    print("2. NEWコスメティックの取得")
    print("3. 全コスメティックを取得")
    print("4. ロビー背景")
    print("5. 複合化ファイルアイテム取得")
    print("6. ニュースフィード")
    print("7. プレイリスト取得")
    print("8. 好きなアイテムの画像生成")
    print("9. 終了")
    choice = input("番号を選択してください: ")

    # 最新のマップをダウンロード
    if choice == "1":
        print("処理を開始します...")
        if not os.path.exists(map_folder_name):
            print(f"{map_folder_name} フォルダが存在しないため作成します...")
            os.makedirs(map_folder_name)

        try:
            print("マップ画像をダウンロード中...")
            response = requests.get(map_url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))

            save_path = os.path.join(map_folder_name, map_file_name)
            with open(save_path, "wb") as file, tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                colour="green",
                desc="進行状況",
            ) as pbar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        pbar.update(len(chunk))

            print(f"ダウンロード完了！ {save_path} に保存されました。")
        except requests.exceptions.RequestException as e:
            print(f"エラーが発生しました: {e}")

    # NEWコスメティックの取得
    elif choice == "2":
        print("処理を開始します...")
        if not os.path.exists(cosmetics_folder_name):
            print(f"{cosmetics_folder_name} フォルダが存在しないため作成します...")
            os.makedirs(cosmetics_folder_name)

        try:
            print("APIからデータを取得中...")
            response = requests.get(newcosmetics_url)
            response.raise_for_status()
            data = response.json()
            items = data.get("data", {}).get("items", {}).get("br", [])
            if not items:
                print("データが見つかりませんでした。")
            else:
                save_path = os.path.join(cosmetics_folder_name, cosmetics_file_name)
                with open(save_path, "w", encoding="utf-8") as file, tqdm(
                    total=len(items),
                    unit="item",
                    colour="green",
                    desc="進行状況",
                ) as pbar:
                    for item in items:
                        name = item.get("name", "不明")
                        description = item.get("description", "不明")
                        item_id = item.get("id", "不明")
                        set_text = item.get("set", {}).get("text", "不明")
                        rarity = item.get("rarity", {}).get("displayValue", "不明")
                        icon_url = item.get("images", {}).get("icon", "不明")
                        file.write(f"名前: {name}\n")
                        file.write(f"説明: {description}\n")
                        file.write(f"ID: {item_id}\n")
                        file.write(f"セット: {set_text}\n")
                        file.write(f"レア度: {rarity}\n")
                        file.write(f"スキン画像: {icon_url}\n\n")
                        file.write("-" * 125 + "\n\n")
                        pbar.update(1)

                print(f"データの保存が完了しました！ ファイル: {save_path}")

        except requests.exceptions.RequestException as e:
            print(f"エラーが発生しました: {e}")

    # 全コスメティックを取得
    elif choice == "3":
        print("処理を開始します...")
        if not os.path.exists(allcosmetics_folder_name):
            print(f"{allcosmetics_folder_name} フォルダが存在しないため作成します...")
            os.makedirs(allcosmetics_folder_name)

        try:
            print("APIからデータを取得中...")
            response = requests.get(allcosmetics_url)
            response.raise_for_status()
            data = response.json()
            items = data.get("data", {}).get("br", [])
            if not items:
                print("データが見つかりませんでした。")
            else:
                save_path = os.path.join(allcosmetics_folder_name, cosmetics_file_name)
                with open(save_path, "w", encoding="utf-8") as file, tqdm(
                    total=len(items),
                    unit="item",
                    colour="green",
                    desc="進行状況",
                ) as pbar:
                    for item in items:
                        name = item.get("name", "不明")
                        description = item.get("description", "不明")
                        item_id = item.get("id", "不明")
                        set_text = item.get("set", {}).get("text", "不明")
                        rarity = item.get("rarity", {}).get("displayValue", "不明")
                        icon_url = item.get("images", {}).get("icon", "不明")
                        file.write(f"名前: {name}\n")
                        file.write(f"説明: {description}\n")
                        file.write(f"ID: {item_id}\n")
                        file.write(f"セット: {set_text}\n")
                        file.write(f"レア度: {rarity}\n")
                        file.write(f"スキン画像: {icon_url}\n\n")
                        file.write("-" * 125 + "\n\n")
                        pbar.update(1)

                print(f"データの保存が完了しました！ ファイル: {save_path}")

        except requests.exceptions.RequestException as e:
            print(f"エラーが発生しました: {e}")

    # ロビー背景の取得
    elif choice == "4":
        print("処理を開始します...")

        # フォルダが存在しなければ作成
        if not os.path.exists(lobby_folder_name):
            print(f"{lobby_folder_name} フォルダが存在しないため作成します...")
            os.makedirs(lobby_folder_name)

        # ロビー背景の取得
        try:
            print("APIからロビー背景を取得中...")
            response = requests.get(lobby_url)
            response.raise_for_status()
            data = response.json()

            # 背景画像のURL取得
            backgrounds = data.get("data", {}).get("backgrounds", {}).get("backgrounds", [])
            if not backgrounds:
                print("背景データが見つかりませんでした。")
            else:
                background_image_url = backgrounds[0].get("backgroundimage", None)
                if not background_image_url:
                    print("背景画像URLが見つかりませんでした。")
                else:
                    # 背景画像のダウンロード
                    print("背景画像をダウンロード中...")
                    response = requests.get(background_image_url, stream=True)
                    response.raise_for_status()
                    total_size = int(response.headers.get("content-length", 0))

                    # ファイル保存
                    save_path = os.path.join(lobby_folder_name, lobby_file_name)
                    with open(save_path, "wb") as file, tqdm(
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        colour="green",
                        desc="進行状況",
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                                pbar.update(len(chunk))

                    print(f"ダウンロード完了！ {save_path} に保存されました。")

        except requests.exceptions.RequestException as e:
            print(f"エラーが発生しました: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")

    elif choice == "5":
        print("複合化アイテムの処理を開始します...")

        # フォルダが存在しない場合は作成
        if not os.path.exists(decrypted_folder_name):
            print(f"{decrypted_folder_name} フォルダが存在しないため作成します...")
            os.makedirs(decrypted_folder_name)

        if not os.path.exists(font_path):
            print(f"フォントファイル {font_path} が見つかりません。正しいパスを指定してください。")
            continue

        try:
            # AESキーを取得
            print("AESキーを取得中...")
            aes_response = requests.get(aes_url)
            aes_response.raise_for_status()
            aes_data = aes_response.json()

            dynamic_keys = aes_data.get("dynamicKeys", [])
            if not dynamic_keys:
                print("AESキーが見つかりませんでした。")
                continue

            for key in tqdm(dynamic_keys, desc="進行状況", colour="green"):
                pak_name = key.get("name", "")
                match = re.search(r'(\d+)', pak_name)
                pak_id = match.group(1) if match else None

                if not pak_id:
                    print(f"無効なpak ID: {pak_name}")
                    continue

                # コスメティックデータを取得
                print(f"パックID {pak_id} のデータを取得中...")
                cosmetics_url = cosmetics_base_url.format(pak_id)
                cosmetics_response = requests.get(cosmetics_url)

                if cosmetics_response.status_code == 404:
                    print(f"パックID {pak_id} のデータは見つかりませんでした。404エラーが発生しました。")
                    continue
                cosmetics_response.raise_for_status()
                cosmetics_data = cosmetics_response.json()

                items = cosmetics_data.get("data", [])
                for item in items:
                    name = item.get("name", "不明")
                    icon = item.get("images", {}).get("icon", None)

                    if not icon:
                        print(f"アイテム {name} の画像が見つかりませんでした。")
                        continue

                    # 名前の処理と画像作成
                    clean_name = re.sub(r'[^a-zA-Z0-9]', '', name)
                    font_size = 60 if len(clean_name) >= 16 else 55
                    font = ImageFont.truetype(font_path, size=font_size)

                    print(f"アイテム {name} の画像をダウンロード中...")
                    image_response = requests.get(icon, stream=True)
                    image_response.raise_for_status()

                    item_image = Image.open(image_response.raw).convert("RGBA")
                    new_width, new_height = int(item_image.width * 4.3), int(item_image.height * 4.3)
                    item_image = item_image.resize((new_width, new_height))

                    # ベース画像と合成
                    base_image = Image.open("itemback.PNG").convert("RGBA")
                    base_image.paste(item_image, (0, 0), item_image)

                    name_image = Image.open("nameimage.PNG").convert("RGBA")
                    base_image.paste(name_image, (0, 0), name_image)

                    draw = ImageDraw.Draw(base_image)
                    text_width, text_height = draw.textbbox((0, 0), name, font=font)[2:4]
                    text_position = ((base_image.width - text_width) // 2, base_image.height - text_height - 120)
                    draw.text(text_position, name, font=font, fill=(255, 255, 255, 255))

                    save_path = os.path.join(decrypted_folder_name, f"{clean_name}.png")
                    base_image.save(save_path, format="PNG")
                    print(f"保存完了: {save_path}")

            print("複合化アイテムの処理が完了しました！")
        except requests.exceptions.RequestException as e:
            print(f"エラーが発生しました: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")

    elif choice == "6":
        print("ニュースフィードを取得中...")

        try:
            response = requests.get(newsapi_url)
            response.raise_for_status()
            data = response.json()

            content_items = data.get("data", {}).get("contentItems", [])
            if not content_items:
                print("APIレスポンスに対応出来ませんでした")
            else:
                for idx, item in enumerate(tqdm(content_items, desc="ニュースフィード処理中", colour="green")):
                    if isinstance(item, dict):
                        content_fields = item.get("contentFields", {})
                        for field_name in ["FullScreenTitle", "FullScreenBackground"]:
                            field = content_fields.get(field_name, {})
                            if isinstance(field, dict):
                                for img in field.get("Image", []):
                                    if isinstance(img, dict) and img.get("height") == 1080:
                                        image_url = img.get("url")
                                        if image_url:
                                            title = re.sub(r'[\\/*?:"<>|]', "_", content_fields.get("FullScreenTitle", "default_title"))
                                            file_name = f"{title}.jpg"
                                            if not os.path.exists(newssave_folder):
                                                os.makedirs(newssave_folder)
                                            save_path = os.path.join(newssave_folder, file_name)

                                            try:
                                                image_response = requests.get(image_url, stream=True)
                                                image_response.raise_for_status()
                                                with open(save_path, 'wb') as f:
                                                    for chunk in image_response.iter_content(1024):
                                                        f.write(chunk)
                                                print(f"{file_name} 保存完了: {save_path}")
                                            except requests.exceptions.RequestException as e:
                                                print(f"画像のダウンロード中にエラーが発生しました: {e}")
                                        else:
                                            print(f"{field_name} 画像URLが見つかりませんでした。")
            print("\n処理が完了しました。メニューに戻ります。")

        except requests.exceptions.RequestException as e:
            print(f"APIリクエスト中にエラーが発生しました: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")

            print("\n処理が完了しました。メニューに戻ります。")

    elif choice == "7":
        print("処理を開始します...")
        if not os.path.exists(mnemonicfolder_path):
            print(f"{mnemonicfolder_path} フォルダが存在しないため作成します...")
            os.makedirs(mnemonicfolder_path)
        try:
            print("APIからプレイリスト情報を取得中...")
            response = requests.get(mnemonicurl)
            response.raise_for_status()
            data = response.json()
            parent_links = data.get('data', {}).get('parentLinks', [])
            if not parent_links:
                print("プレイリストが見つかりませんでした。")
            else:
                for idx, link in enumerate(tqdm(parent_links, desc="プレイリスト画像処理中", colour="green")):
                    image_url = link.get('metadata', {}).get('image_url')
                    if image_url:
                        print(f"プレイリスト {idx + 1}: {image_url}")
                        print(f"画像 {idx + 1} をダウンロード中...")
                        try:
                            image_response = requests.get(image_url, stream=True)
                            image_response.raise_for_status()
                            image_filename = os.path.join(mnemonicfolder_path, f"プレイリスト画像：{idx + 1}.jpg")
                            with open(image_filename, 'wb') as file:
                                for chunk in image_response.iter_content(chunk_size=1024):
                                    if chunk:
                                        file.write(chunk)
                            print(f"プレイリスト画像：{idx + 1} が保存されました: {image_filename}")
                        except requests.exceptions.RequestException as e:
                            print(f"プレイリスト画像：{idx + 1} のダウンロード中にエラーが発生しました: {e}")
                    else:
                        print(f"リンク {idx + 1} 画像URLが見つかりませんでした。")
        except requests.exceptions.RequestException as e:
            print(f"エラーが発生しました: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")
    
    elif choice == "8":
        print("アイテム名を入力してください:")
        item_name = input("アイテム名: ").strip()

        if not item_name:
            print("アイテム名が入力されていません。")
            continue
        item_url = f"https://fortnite-api.com/v2/cosmetics/br/search?name={item_name}&language=ja&searchLanguage=ja"

        try:
            print(f"アイテム情報を取得中: {item_name}...")
            response = requests.get(item_url)
            response.raise_for_status()
            data = response.json()
            
            # 'data' キーが存在し、かつ中身がある場合
            if "data" not in data or not data["data"]:
                print(f"アイテム '{item_name}' の情報が見つかりませんでした。")
                continue

            # data["data"] がリストでなく辞書なので、直接取り出す
            item_data = data["data"]
            name = item_data.get("name", "不明")
            description = item_data.get("description", "不明")
            icon_url = item_data.get("images", {}).get("smallIcon", None)
            variants = item_data.get("variants", [])
            print(f"アイテム名: {name}")
            print(f"説明: {description}")
            
            # アイテム名のフォルダを作成
            folder_path = os.path.join(os.getcwd(), item_name)  # 現在のディレクトリにフォルダ作成
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"フォルダ '{item_name}' を作成しました。")

            # 背景画像（itemback.PNG）の読み込み
            background_image = Image.open("itemback.PNG").convert("RGBA")
            width, height = background_image.size

            # アイコン画像のダウンロードと保存
            if icon_url:
                print(f"{item_name}の画像をダウンロード中... ")
                image_response = requests.get(icon_url, stream=True)
                image_response.raise_for_status()
                item_image = Image.open(image_response.raw).convert("RGBA")
                item_image = item_image.resize((item_image.width * 4, item_image.height * 4))  # アイテム画像を4倍に拡大
                background_image.paste(item_image, (50, 50), item_image)  # アイテム画像を背景に重ねる
            name_image = Image.open("nameimage.PNG").convert("RGBA")
            background_image.paste(name_image, (width - name_image.width, 50), name_image)

            font = ImageFont.truetype("GENEIPOPLEPW-BK.TTF", 40)  # アイテム名と説明に使うフォント

            # テキストの描画(地獄)の開始
            draw = ImageDraw.Draw(background_image)

            # アイテム名
            draw.text((520, height - 190), name, font=font, fill=(300, 255, 255))
            # アイテムの説明
            draw.text((65, height - 100), description, font=font, fill=(255, 255, 255))

            final_image_path = os.path.join(folder_path, f"{name}_final_image.png")
            background_image.save(final_image_path)
            print(f"'{final_image_path}' に保存しました。")
        except requests.exceptions.RequestException as e:
            print(f"リクエスト中にエラーが発生しました: {e}")
            print(f"ステータスコード: {e.response.status_code if e.response else '不明'}")
            if e.response is not None:
                print(f"レスポンス内容: {e.response.text}")
        except Exception as e:
            import traceback
            print(f"予期しないエラーが発生しました: {e}")
            print("エラートレースバック:")
            traceback.print_exc()

    elif choice == "9":
        print("プログラムを終了します。")
        break

    else:
        print("無効な入力です。再度選択してください。")
