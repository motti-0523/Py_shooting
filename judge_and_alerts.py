def isValid(brackets):
    stack = []
    opening_brackets = "({["
    closing_brackets = ")}]"
    brackets_map = {')': '(', '}': '{', ']': '['}
    #opening_bracketsの各要素をkeyとする辞書型の作成（openingに"(","{","["をkeyとして渡し、対応する値を0として初期化）
    pair_count = {opening: 0 for opening in opening_brackets}
    flag = 1

    if len(brackets) % 2 != 0:
        error_message = f"エラー：括弧の数が奇数になっています。適切に括弧を閉じることができません"
        return False, error_message

    for char in brackets:
        if char in opening_brackets:
            #開き括弧をスタックに格納
            stack.append(char)
            #対応する括弧のカウントを一増やす
            pair_count[char] += 1
        elif char in closing_brackets:
            #対応する括弧のカウントを一減らす
            pair_count[brackets_map[char]] -= 1
            #スタック内に開き括弧があるか、開き括弧があった際に、スタックからポップさせて一致するかを確認
            if not stack or brackets_map[char] != stack.pop():
                #一致しなければflag=0にして、より詳しいエラー分類に進める
                flag = 0
            
    if flag == 0:
        for opening, count in pair_count.items():
            if count != 0:
                error_message = f"エラー：開き括弧と閉じ括弧で適切にペアを作れません"
                return False, error_message
            else:
                error_message = f"エラー：開き括弧と閉じ括弧の順番が一致しません"
                return False, error_message
    else:
        return True, "正常"

while True:
    s = input("括弧を入力してください（０を入力すると終了します）：")
    if s == "0":
        break
    else:
        value, message = isValid(s)
        if value:
            #True = 正常は自明なので省略（プロトタイプ宣言の返り値の数が一致しなくなるため用意はしている）
            print(f"{s}: {value}")
        else:
            print(f"{s}: {value} ({message})")
