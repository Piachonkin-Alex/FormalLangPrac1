# Практикум №1
[![codecov](https://codecov.io/gh/Piachonkin-Alex/FormalLangPrac1/branch/main/graph/badge.svg?token=6L5DPCEEHB)](https://codecov.io/gh/Piachonkin-Alex/FormalLangPrac1)

## Постановка задачи
Дано регулярное выражение |α| и слово u ∈ {a, b, c}*. Найти длину самого длинного суффикса u, являющегося также суффиксом некоторого слова в L(α).

## Алгоритм решения задачи
Разобьем решение на 3 основных блока:
#### Построение НКА с не более чем однобуквенными переходами и одним конечным состоянием по регулярному выражению
Будем строить наш автомат аналогично восстановлению регулярного выражения в обратной польской записи через стек. Рассмотрим следующие возможные случаи:
- Автомат для регулярного выражения 1. Тогда, создаем автомат с одним состоянием без переходов.
- Автомат для регулярного выражения, являющегося буквой алфавита. Тогда, создаем автомат с двумя состояниями, одно из которых является стартовым, другое - конечным. Единственным переходом будет переход из стартового состояния в конечное по букве, данной в регулярном выражении.
- Автомат для конкатенации 2 регулярных выражений, для которых уже построены автоматы A и B соответственно. Тогда, создаем автомат С, состояниями которого будут все состояния автоматов A и B. Стартовым состоянием C будет стартовое состояние A, конечным состоянием C будет конечное состояние B. Переходами у С будут служить все переходы из автоматов из A и B, а также переход по пустому слову из конечного состояния A в стартовое состояние B.
- Автомат для суммы 2 регулярных выражений, для которых уже построены автоматы A и B соответственно. Тогда, создаем автомат С, состояниями которого будут все состояния автоматов A и B и новое стартовое и конечное состояния. Переходами у С будут служить все переходы из автоматов из A и B, а также 4 новых перехода по пустым словам: из нового стартового состояния в стартовое автомата A, из нового стартового состояния в стартовое автомата B, из конечного состояния автомата A в новое конечное и из конечного состояния автомата B в новое конечное.
- Автомат для регулярного выражения α*, когда построен автомат A для регулярного выражения α. Тогда, создаем автомат B, состояниями которого будут все состояния автомата A. Стартовым состоянием B будет стартовое состояние из A, оно же будет конечным. Переходами у B будут служить все переходы из A, а также переход по пустому слову из конечного состояния A в начальное состояние A.
#### Преобразование НКА с не более чем однобуквенными переходами и одним конечным состоянием в НКА с однобуквеннными переходами
Этот алгоритм является классическим. Для начала находим все однобуквенные ребра. Для этого, для каждого состояния DFS-ом находим пути вида переходы по пустому слову + один переход по букве. Затем, также DFS-ом смотрим какие состояния являются достижимыми из стартового, и только они попадают в преобразованный автомат. Затем удаляем все ребра, начало которых является недостижимым из стартового состояния. Наконец, находим все конечные состояния, проверив есть путь из пустых слов до конечного состояния в исходном автомате.
#### Нахождение длины самого длинного суффикса слова u, являющегося суффиксом некоторого слова, принимаемым НКА с однобуквенными переходами
Здесь мы используем динамическое программирование. Пустой суффикс может порождаться лишь в конечных состояниях автомата. Далее, проделываем следующую операцию. Считываем символ x следующего по длине суффикса. У нас есть множество состояний, в которые достижимы из прошлого суффикса. Для каждого из этих состояний мы ищем ребра, конец которых совпадает с этим состоянием и переход осуществляется по x. Все состояния, которые являются началами этих ребер, будут порождать суффикс новый суффикс. Осталось в конце лишь делать проверку, пусто ли множество таких состояний. Если да, то ответ - длина предыдущего суффикса, иначе мы переходим на новую итерацию.
## Оценка асимптотики
- Построение НКА с не более чем однобуквенными переходами и одним конечным состоянием по регулярному выражению - $O(|α|log|α|)$, так как согласно описанию, не считая базовых случаев, у нас на каждом символе сливаются состояния и переходы 2 автоматов (аналогично mergesort). Для следующих пунктов заметим, что число состояний и переходов равно O(|α|), так как на каждом шаге добавляется не более 2 новых состояний и4 новых переходов.
- Преобразование НКА с не более чем однобуквенными переходами и одним конечным состоянием в НКА с однобуквеннными переходами. Ввиду того, что число состояний и переходов равно O(|α|), очевидно что все серии DFS-ов будут работать за O(|α|^2). Заметим, что согласно правилам построения нашего НКА в предыдущем пункте, количество вподряд идущих пустых переходов не может превышать 3. А это значит, что однобуквенных ребер будет O(|α|). Следовательно, проверка всех ребер на достижимость будет занимать  O(|α|^2). Для следующего пункта также отметим, что число состояний и переходов осталось равно O(|α|).
- Нахождение длины самого длинного суффикса слова u, являющегося суффиксом некоторого слова, принимаемым НКА с однобуквенными переходам. Очевидно, что на каждой итерации происходит O(|α|^2) проверок (для каждого состояния предыдущего сууффикса по всем ребрам). Значит, асимптотика данного шага будет 
```
math O(|u||α|^2)
```
##### Итоговая асимптотика -- O(|u||α|^2)
## Параметры запуска

### Требования перед запуском
Требуется установить Poetry версии не меньше 1.1.0. Это можно сделать следующей командой:
```bash
-curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
Все остальные пакеты будут установлены с помощью
```bash
poetry install
```
### Запуск программы
Для того, чтобы запустить программу, которая принимает на вход 2 строки, первая из которых является регулярным выражением, вторая является некоторым словом, и выдает длину самого длинного суффикса слова, являющегося также суффиксом некоторого слова данного регулярного выражения, введите
```bash
poetry run task main
```
### Запуск тестов
Для того, чтобы запустить тесты, введите
```bash
poetry run task test
```
