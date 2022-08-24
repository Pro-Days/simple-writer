import re


fw = open("output.txt", 'w', encoding="UTF-8")  # 작성할 파일
try:
    fr = open("input.txt", 'r', encoding="UTF-8")  # 읽을 파일
except:
    fw.write("*오류* 입력 파일이 존재하지 않습니다.")  # 읽을 파일이 존재하지 않을 경우
else:
    txts = fr.readlines()  # 읽을 파일 텍스트 모두 읽기

    variable = {}  # 변수 속 리스트 저장
    ## {a: [0, 1, 2], b: ["a", "b", "c"], c: ["d", "e", "f"]}
    line_num_dic = {}  # 시작줄, 끝줄
    loop_count = {}  # 진행중인 줄, 끝날 줄

    for loop_num in range(len(txts)):
        line = txts[loop_num].strip()

        if line[0:2] == "//" and line[-1:-3:-1] == "//":  # 변수 지정하는 줄
            lines = line.replace(" ", "")[2:-2].split(";")  # //, 삭제, ;를 기준으로 구분
            var_temp = []
            # print(lines)
            for i in lines:
                var_temp.append(i.split("=")[0])  # 변수와 리스트 속 변수 구분
                if "=" in i:
                    line_var = i.split("=")[0]
                    line_val = i.split("=")[1]

                    if "~" in line_val and "(" in line_val and ")" in line_val:  # 숫자
                        line_vals = line_val.replace(
                            "(", "").replace(")", "").split("~")
                        for0 = int(line_vals[0])
                        for1 = int(line_vals[1])
                        line_val = []
                        for j in range(for0, for1+1):
                            line_val.append(j)
                        variable[line_var] = line_val

                    if "[" in line_val and "]" in line_val:  # 변수지정
                        line_val = line_val.replace(
                            "[", "").replace("]", "").split(",")
                        variable[line_var] = line_val
            if "=" in line:  # 변수 지정하는 줄
                var_temp1 = ";".join(var_temp)
                # print(var_temp1)
                line_num_dic[var_temp1] = loop_num  # 변수 시작점 지정

            else:  # 변수 끝나는 줄
                # print(213123123132)
                var_temp1 = ";".join(var_temp)
                # print(var_temp1)
                for loop_var in line_num_dic:
                    if var_temp1 == loop_var:
                        temp = [line_num_dic[loop_var], loop_num]
                        line_num_dic[var_temp1] = temp
    # print(line_num_dic)

    run_dic = True
    no_val = []
    for num_dic in line_num_dic:
        if type(line_num_dic[num_dic]) != list:  # 시작점 또는 끝점이 지정되지 않은 경우 실행 x
            no_val.append(num_dic)
            run_dic = False

    show_error = []
    show_error_b = False
    if run_dic:
        line_num = 0
        for i in line_num_dic:
            temp = i.split(";")
            # print(temp)
            for j in temp:
                try:
                    loop_count[j] = [1, len(variable[temp[0]])]  # 진행중인 줄, 끝 줄 지정
                except:
                    show_error.append(j)
                    show_error_b = True
            # print(loop_count)
        while line_num < len(txts):
            line = txts[line_num].strip()

            if line[0:2] == "//" and line[-1:-3:-1] == "//":  # 변수 줄
                lines = line.replace(" ", "")[2:-2].split(";")
                var_temp = []
                if "=" in line:  # 시작변수
                    for i in lines:
                        var_temp.append(i.split("=")[0])
                    var_temp = ";".join(var_temp)
                    temp = var_temp.split(";")
                    for j in temp:
                        try:
                            loop_count[j] = [1, len(variable[temp[0]])]
                        except:
                            show_error.append(j)
                            show_error_b = True

                    temp = temp[0]
                    try:
                            loop_count[var_temp] = [1, len(variable[temp])]
                    except:
                        show_error.append(var_temp)
                        show_error_b = True
                    

                    # print(loop_count)

            for i in line_num_dic:
                if line[0:2] != "//" and line[-1:-3:-1] != "//":  # 일반 줄
                    # i1 = 0
                    # print(len(line))
                    found = re.search('<(.+?)>', line)  # <> 안에 있는 문자 찾기
                    if found:
                        while_loop = True
                    else:
                        while_loop = False
                        
                    while while_loop:
                        var = found.group(1)
                        if var in variable:
                            found = found.group(0)
                            found_num = line.find(found)
                            try:
                                line = line[:found_num] + \
                                    str(variable[var]
                                        [loop_count[var][0]-1]) + line[found_num + len(found):]

                                found = re.search('<(.+?)>', line)  # <> 속 문자가 추가로 있을 경우
                                if found:
                                    while_loop = True
                                else:
                                    while_loop = False
                                # for i1 in range(len(line)):
                                #     if line[i1] == "{":
                                #         for i2 in range(i1, len(line)):
                                #             if line[i2] == "}":
                                #                 var = line[i1+1:i2]
                                #                 # print(variable[var][loop_count[var][0]-1])
                                #                 # print(line[:i1+1])
                                #                 line = line[:i1+1] + \
                                #                     str(variable[var]
                                #                         [loop_count[var][0]-1]) + line[i2:]
                                #                 # print(line)
                                #                 break
                                #     i1 += 1
                            except:
                                show_error.append(var)
                                show_error_b = True
                                while_loop = False
                        else:
                            show_error.append(var)
                            show_error_b = True
                            while_loop = False

                try:
                    if line_num == line_num_dic[i][1] and loop_count[i][0] != loop_count[i][1]:  # 작성해야 하는 경우
                        # print(loop_count[i][0])
                        # print(loop_count[i][1])
                        line_num = line_num_dic[i][0]
                        # print(loop_count)
                        if i.find(";") != -1:
                            i_split = i.split(";")
                            for j_split in i_split:
                                loop_count[j_split][0] = loop_count[i][0] + 1
                        loop_count[i][0] = loop_count[i][0] + 1

                        # print(str(loop_count)+"\n")
                except:
                    show_error.append(i)
                    show_error_b = True
                    while_loop = False

            if line[0:2] != "//" and line[-1:-3:-1] != "//":  # 작성하는 줄
                # print(line)
                fw.write(line + "\n")  #파일에 작성
            line_num += 1

    else:
        for i in no_val:
            show_error.append(i)
        show_error_b = True


    if show_error_b:  # 에러가 있을 경우
        show_error = list(set(show_error))
        fw.close()
        fw = open("output.txt", 'w', encoding="UTF-8")  # 작성파일 다시열기
        fw.write("*오류* 입력 데이터가 올바르지 않습니다. (" + ", ".join(show_error) + ")\n")