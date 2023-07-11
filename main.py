import re
import datetime
from collections import OrderedDict  # @TODO убрать неиспользуемый импорт

def create_racer_abbreviations_dict(
        file_name):  # @TODO добавить аннотации к атрибутам функции и к выводу функции (https://peps.python.org/pep-0008/#function-annotations)
    """Retrieves {'abbreviation': (name, team)}" format dict from abbreviations.txt"""  # @TODO комментарии не по PEP8 (https://peps.python.org/pep-0008/#comments) + abbreviations.txt нужно заменить на "file" так как функция примет файл с любым названием
    abbreviations_dict = {}
    # @TODO нужно иметь обработчик ошибок для случаев, когда файл отсутствует, поврежден или содержит непредвиденные данные (https://docs.python.org/3/tutorial/errors.html?highlight=exceptions)
    with open(file_name, 'r') as fn:  # @TODO что такое fn? лучше использовать file, также нужно добавить encoding
        for line in fn:
            matchObj = re.match(r'^(\w+)_([a-zA-Z\s]+)_([a-zA-Z\s]+)$', line)  # @TODO имя переменной не по PEP8 (https://peps.python.org/pep-0008/#function-and-variable-names)
            # group(1) is abbreviation, i.e 'SVM'
            abbreviations_dict[matchObj.group(1)] = (
                matchObj.group(2),  # name of a pilot
                matchObj.group(3).rstrip(),  # team
            )
    return abbreviations_dict


# @TODO сначала нужно объявить все функции а потом уже с ними манипулировать
# {'abbreviation of pilot': ('name of pilot, 'team')}
abbr_dict = create_racer_abbreviations_dict(  # @TODO лишний перевод строки уменьшает читаемость
    'abbreviations.txt') # @ TODO Названия файлов и некоторые параметры, такие как количество позиций до разделительной линии, зашиты в коде. Это может сделать код менее гибким для изменений. Лучше передавать такие параметры как аргументы функций или конфигурационные параметры


# returns timing log from start.log or end.log in {'abbreviation': time} format # @TODO комментарии для функции не по PEP8 (https://peps.python.org/pep-0008/#comments)
def retrieve_timings_from_log(
        file_name):  # @TODO добавить аннотации к атрибутам функции и к выводу функции (https://peps.python.org/pep-0008/#function-annotations)
    timing_log = {}
    with open(file_name, 'r') as fn:  # @TODO что такое fn? лучше использовать file, также нужно добавить encoding
        for line in fn:
            # matches 2 groups: abbreviation of a racer and time
            matchObj = re.match(r'^([A-Z]+).*(\d{2}:\d+:\d+\.\d+)$', line)  # @TODO имя переменной не по PEP8 (https://peps.python.org/pep-0008/#function-and-variable-names)
            # converts time from a string to datetime object # @TODO убрать неинформативный комментарий, то что тут указано понятно из кода
            lap_time = datetime.datetime.strptime(  # @TODO лишний перевод строки уменьшает читаемость
                matchObj.group(2).rstrip(), '%H:%M:%S.%f')
            # adds key, value to a timing_log # @TODO убрать неинформативный комментарий, то что тут указано понятно из кода
            timing_log[matchObj.group(1)] = lap_time
    return timing_log


# @TODO сначала нужно объявить все функции а потом уже с ними манипулировать
start_timings = retrieve_timings_from_log('start.log')
end_timings = retrieve_timings_from_log('end.log')


def sorted_individual_results(start_timings_, end_timings_, abbr_dict_, reverse_order=False):  # @TODO добавить аннотации к атрибутам функции и к выводу функции (https://peps.python.org/pep-0008/#function-annotations)
    # @TODO abbr_dict_ объявлен но нигде не используется, также _ в конце имени оставлять не нужно (https://peps.python.org/pep-0008/#function-and-variable-names)
    """
    Receives start and end timings and returns an OrderedDict with
    {abbreviations:timedeltas}
    """  # @TODO комментарии не по PEP8 (https://peps.python.org/pep-0008/#comments)
    # creating dict with best lap results
    lap_results = {key: end_timings_[key] - start_timings_.get(key, 0) # @TODO end_timings_[key] может возвращать ошибку если end_timings_ не содержит ключа key
                   for key in start_timings_.keys()}
    sorted_results = dict(
        sorted(lap_results.items(), key=lambda x: x[1], reverse=reverse_order))
    return sorted_results


# @TODO сначала нужно объявить все функции а потом уже с ними манипулировать
sorted_lap_results = sorted_individual_results(
    start_timings, end_timings, abbr_dict)


# prints result board to a console # @TODO комментарии для функции не по PEP8 (https://peps.python.org/pep-0008/#comments)
def print_result_board(
        sorted_lap_results_):  # @TODO _ в конце имени оставлять не нужно (https://peps.python.org/pep-0008/#function-and-variable-names)
    # @TODO добавить аннотации к атрибутам функции и к выводу функции (https://peps.python.org/pep-0008/#function-annotations)
    counter = 1  # @TODO вместо новой переменной можно использовать enumerate (https://docs.python.org/3/library/functions.html?highlight=enumerate#enumerate)
    for key, value in sorted_lap_results_.items():
        racer_name = abbr_dict[key][0] # @ TODO лучше передать abbr_dict в качестве аргумента функции, так как использование глобальных переменных внутри функции делает их неявными
        team_name = abbr_dict[key][1] # @ TODO лучше передать abbr_dict в качестве аргумента функции, так как использование глобальных переменных внутри функции делает их неявными
        best_time = str(value)[2:-3] # @ TODO не очевидное преобразование времени, лучше использовать что-то явное или написать комментарий
        print(("{: <3} {: <18} | {: <30}  | {}".format(
            str(counter) + '.', racer_name, team_name, best_time))) # @TODO Вместо форматирования строки через format, можно использовать f-строки Python, которые обеспечивают более читаемый и интуитивно понятный синтаксис для форматирования строк.
        if counter == 15:
            print(
                '----------------------------------------------------------------------')
        counter += 1


print_result_board(sorted_lap_results)

# @TODO Функции sorted_individual_results и print_result_board нужно объединить в одну, так как первая используется для сортировки результатов а вторая для того чтобы их вывести в консоль, в данном подходе мы делаем 2 полных прохода по всем результатам, хотя достаточно одного
# @TODO манипулирование функциями должно происходить в блоке if __name__ == '__main__' если мы находимся в корневом файле (так как у нас 1 файл то он и является корневым)

