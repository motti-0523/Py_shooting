def isValid(brackets):
    stack = []
    opening_brackets = "({["
    closing_brackets = ")}]"
    brackets_map = {')': '(', '}': '{', ']': '['}

    for char in brackets:
        if char in opening_brackets:
            #開き括弧をスタックに格納
            stack.append(char)
        elif char in closing_brackets:
            #スタック内に開き括弧があるか、開き括弧があった際に、スタックからポップさせて一致するかを確認
            if not stack or brackets_map[char] != stack.pop():
                return False
    #スタック内に開き括弧が残っていないか＝すべての開き括弧に対応する閉じ括弧があるかを確認
    return len(stack) == 0

while True:
    s = input("括弧を入力してください（０を入力すると終了します）：")
    if s == "0":
        break
    else:
        print(f"{s}: {isValid(s)}")
