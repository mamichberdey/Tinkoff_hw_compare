import numpy as np
import sys
import os
import ast

dir_path = os.path.dirname(__file__) # пути к файлам через os для кроссплатформернности

class Edit_txt: # класс для работы с файлами
    
    def __init__(self, input_file, output_file) -> None: # при инициализации класса необходимы пути к исходным файлам
        self.input_file = input_file
        self.output_file = output_file
        self.input_file_path = os.path.join(dir_path, self.input_file)
        self.output_file_path = os.path.join(dir_path, self.output_file)
    
    def txt_to_list(self): # преобразуем данные из input.txt в список из пар путей
        with open(self.input_file_path) as f: # считываем данные с input.txt
            input_data = f.readlines()
            
        for i, line in enumerate(input_data): # переоформим readlines в список списков
            input_data[i] = line.split()
            
        return input_data
    
    def list_to_scores(self, out_arr): # записываем out_arr в scores.txt
        
        with open(self.output_file_path, "w") as f: 
            f.writelines(line + '\n' for line in out_arr)

class Metrika: # класс для оценивания метрики

    def __init__(self) -> None:
        pass
    
    def lev(str1, str2): # функция для вычисления расстояниея Левенштейна
        if len(str1)*len(str2)==0:
            return max(len(str1), len(str2))
        len1 = len(str1)
        len2 = len(str2)
        F = np.zeros((len1, len2), dtype=int)
        F[:,0] = np.arange(0, len1)
        F[0,:] = np.arange(0, len2)

        for i in range(1, len1):
            for j in range(1, len2):
                if str1[i-1] == str2[j-1]:
                    F[i][j] = F[i-1][j-1]
                else:
                    F[i][j] = 1+min(F[i-1][j], F[i][j-1], F[i-1][j-1])
        
        return F[len1-1][len2-1]

    def ans_prob(str1, str2): # вероятность того, что тексты одинаковы
        return 1-Metrika.lev(str1, str2)/len(max(str1, str2))
    
if __name__ == "__main__":
    
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    
    data_set = Edit_txt(input_file, output_file)
    
    input_data = data_set.txt_to_list()
    
    ans_list=[]
    
    for path_1, path_2 in input_data: # цикл попарно сравнивающий исходные коды
        fir_file_path = os.path.join(dir_path, str(path_1))
        sec_file_path = os.path.join(dir_path, str(path_2))
        
        with open(fir_file_path) as f: #предобработка текста
            fir_tree = ast.dump(ast.parse(f.read()))
        
        with open(sec_file_path) as f:
            sec_tree = ast.dump(ast.parse(f.read()))
            
        ans_list.append(str(Metrika.ans_prob(fir_tree, sec_tree)))
        data_set.list_to_scores(ans_list) # запишем в файл результаты
     
       
        
    
    