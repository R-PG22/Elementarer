from janome.tokenizer import Tokenizer

# 形態素解析器の初期化
tokenizer = Tokenizer()


def kata2hira(text):
    """小文字（ァ〜ヶ）を含むすべてのカタカナをひらがなに変換"""
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in text)


def is_kanji(char):
    """文字が漢字（または々）かどうかを判定"""
    return "一" <= char <= "龥" or char == "々"


def convert_text(text, allowed_kanji):
    result = []

    # 文章を単語（形態素）単位に分割して処理
    for token in tokenizer.tokenize(text):
        surface = token.surface  # 元の表記（例：「神社」「食べる」）
        reading = token.reading  # カタカナの読み（例：「ジンジャ」「タベル」）

        # 読みが取得できない記号・英数字などはそのまま出力
        if reading == "*":
            result.append(surface)
            continue

        # 単語内に未習得漢字が含まれているか確認
        has_unallowed_kanji = any(
            is_kanji(c) and c not in allowed_kanji for c in surface
        )

        # 未習得漢字が含まれていなければ元の表記のまま
        if not has_unallowed_kanji:
            result.append(surface)
            continue

        # --- 未習得漢字が含まれている場合の変換処理 ---
        hiragana_reading = kata2hira(reading)

        # 文字数と読みの長さが一致する場合（例：「1文字＝ひらがな1文字」のケース）
        if len(surface) == len(hiragana_reading):
            converted_token = ""
            for i, char in enumerate(surface):
                if is_kanji(char) and char not in allowed_kanji:
                    converted_token += hiragana_reading[i]
                else:
                    converted_token += char
            result.append(converted_token)
        else:
            # 「神社（ジンジャ）」のように漢字1文字に対して複数の読みがある場合、
            # 文字単位の分割崩れを防ぐため単語全体の読みを採用する
            result.append(hiragana_reading)

    return "".join(result)


# --- メイン処理 ---
# ファイルの読み込み
with open("input.txt", "r", encoding="utf-8") as f:
    input_text = f.read()

with open("elementary_kanji.txt", "r", encoding="utf-8") as g:
    # 高速検索のため set 型に変換
    elementary_kanji = set(g.read())

# 変換の実行と結果の出力
result_text = convert_text(input_text, elementary_kanji)
print(result_text)

# 必要に応じてファイル保存する場合
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(result_text)