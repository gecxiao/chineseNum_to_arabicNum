import pandas

common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                            '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
common_used_numerals = {}
special_symbol = {'百': 100, '千': 1000, '万': 10000, '亿': 100000000}
check_list = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九','十']
num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九']
more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']

for key in common_used_numerals_tmp:
    common_used_numerals[key] = common_used_numerals_tmp[key]


def get_specialcase_unit(oriStr):  # 得到正确单位
    last_num2 = oriStr[-2]  # 找到倒数第二位数
    correct_unit = int(special_symbol.get(last_num2) / 10)  # 最后一位应当乘上的倍数
    return correct_unit


def specialcase_one(string):  # 第一种特殊情况：五百八 （应为580而不是508）
    if string[-1] in num_str_start_symbol and string[-2] in special_symbol:
        return True
    return False
    # last_unit = int(special_symbol.get(str[-2])/10)


def specialcase_two(oriStr):  # 第二种特殊情况：以单位结尾
    if oriStr[-1] in special_symbol and len(oriStr) > 2:
        return True
    return False


def specialcase_three(oriStr):  # 第三种情况：倒数第二个是十且最后一位不是单位
    if len(oriStr)>=3:
        if oriStr[-2] == '十' and oriStr[-1] not in special_symbol and oriStr[-3] == '零':
            return True
    return False


def specialcase_four(oriStr):  # 第四种情况：倒数第二位是零
    if oriStr[-2] == '零':
        return True
    return False


def check_ten(string):  # 判断是否以‘十’开头
    if string[0] == '十':
        return True
    return False


def chinese2digits(string):
    total = 0
    mode = False  # check pure number or series
    temp = ''
    temp_val = 0
    max_unit = 0
    ten_case = False  # 如果出现10，有特殊情况
    if len(string)==1:
        return common_used_numerals_tmp.get(string[0])
    if (check_ten(string)):  # start with 十
        temp_val = 10
        if (len(string) == 2):
            total = 10 + common_used_numerals_tmp.get(string[1])
            mode = True
        else:
            for i in range(1, len(string)):
                if (string[i] in num_str_start_symbol):  # a number
                    temp_val += common_used_numerals_tmp.get(string[i])
                else:  # means str[i] is in 百，千，万, etc.
                    temp_unit = common_used_numerals_tmp.get(string[i])
                    if (max_unit < temp_unit):
                        max_unit = temp_unit
                    temp_val = temp_val * common_used_numerals_tmp.get(string[i])
                    total += temp_val
                    temp_val = 0
    else:
        for i in range(0, len(string)):
            if (string[i] in num_str_start_symbol):  # a number
                temp_val += common_used_numerals_tmp.get(string[i])
                if (ten_case):
                    total += temp_val
                    temp_val = 0
                temp = temp + str(common_used_numerals_tmp.get(string[i]))
            else:  # means str[i] is in 百，千，万, etc.
                mode = True
                if (string[i] == '十'):
                    ten_case = True
                temp_unit = common_used_numerals_tmp.get(string[i])
                if (max_unit < temp_unit):
                    max_unit = temp_unit
                temp_val = temp_val * common_used_numerals_tmp.get(string[i])
                total += temp_val
                temp_val = 0
    if mode is False:
        return temp
    else:
        if (specialcase_one(string)):
            unit = get_specialcase_unit(string)
            last_digit = common_used_numerals_tmp.get(string[-1])
            # total-=last_digit
            total = total + unit * last_digit
        if (specialcase_two(string)):
            unit = common_used_numerals_tmp.get(string[-1])
            if (unit == max_unit):
                total *= unit
        if (specialcase_three(string)):
            total += 10
        if (specialcase_four(string)):
            total += common_used_numerals_tmp.get(string[-1])
    return total


def changeChineseNumToArab(oriStr):
    lenStr = len(oriStr)
    aProStr = ''
    if lenStr == 0:
        return aProStr

    hasNumStart = False
    numberStr = ''
    for idx in range(lenStr):
        if oriStr[idx] in check_list:
            if not hasNumStart:
                hasNumStart = True

            numberStr += oriStr[idx]
        else:
            if hasNumStart:
                if oriStr[idx] in more_num_str_symbol:
                    numberStr += oriStr[idx]
                    continue
                else:
                    numResult = str(chinese2digits(numberStr))
                    numberStr = ''
                    hasNumStart = False
                    aProStr += numResult

            aProStr += oriStr[idx]
            pass
    if len(numberStr) > 0:
        resultNum = chinese2digits(numberStr)
        aProStr += str(resultNum)

    return aProStr


testStr = ['请回答屏幕上的问题请回答答案对应的数字距离您的地址最近的超市是一同心医药第四十二零售部二月薪生活超市三为民超市4万家乐超市']

for tstr in testStr:
    print(tstr + ' = ' + changeChineseNumToArab(tstr))
