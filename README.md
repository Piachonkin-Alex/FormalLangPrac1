# Практикум №1
[![codecov](https://codecov.io/gh/Piachonkin-Alex/FormalLangPrac1/branch/main/graph/badge.svg?token=6L5DPCEEHB)](https://codecov.io/gh/Piachonkin-Alex/FormalLangPrac1)

## Постановка задачи
Дано регулярное выражение α и слово u ∈ {a, b, c}*. Найти длину самого длинного суффикса u, являющегося также суффиксом некоторого слова в L(α).

## Алгоритм решения
Разобьем решение на 3 основных блока:
#### Построение НКА с не более чем однобуквенными переходами и одним конечным состоянием по регулярному выражению
Будем строить наш автомат аналогично восстановлению регулярного выражения в обратной польской записи через стек. Рассмотрим следующие возможные случаи:
- Автомат для регулярного выражения 1. Тогда, создаем автомат с одним состоянием без переходов.
- Автомат для регулярного выражения, являющегося буквой алфавита. Тогда, создаем автомат с двумя состояниями, одно из которых является стартовым, другое - конечным. Единственным переходом будет переход из стартового состояния в конечное по букве, данной в регулярном выражении.
- Автомат для конкатенации 2 регулярных выражений, для которых уже построены автоматы A и B соответственно. Тогда, создаем автомат С, состояниями которого будут все состояния автоматов A и B. Стартовым состоянием C будет стартовое состояние A, конечным состоянием C будет конечное состояние B. Переходами у С будут служить все переходы из автоматов из A и B, а также переход по пустому слову из конечного состояния A в стартовое состояние B.
- Автомат для суммы 2 регулярных выражений, для которых уже построены автоматы A и B соответственно. Тогда, создаем автомат С, состояниями которого будут все состояния автоматов A и B и новое стартовое и конечное состояния. Переходами у С будут служить все переходы из автоматов из A и B, а также 4 новых перехода по пустым словам: из нового стартового состояния в стартовое автомата A, из нового стартового состояния в стартовое автомата B, из конечного состояния автомата A в новое конечное и из конечного состояния автомата B в новое конечное.
- Автомат для регулярного выражения α*, когда построен автомат A для регулярного выражения α. Тогда, создаем автомат B, состояниями которого будут все состояния автомата A. Стартовым состоянием B будет стартовое состояние из A, оно же будет конечным. Переходами у B будут служить все переходы из A, а также переход по пустому слову из конечного состояния A в начальное состояние A.
#### Преобразование НКА с не более чем однобуквенными переходами и одним конечным состоянием в НКА с однобуквеннными переходами
Этот алгоритм является классическим. Для начала находим все однобуквенные ребра. Для этого, для каждого состояния дфсом находим пути вида переходы по пустому слову + один переход по букве. Затем, смотрим какие состояния являются достижимыми из стартового, и только они попадают в преобразованный автомат. Затем удаляем все ребра, начало которых является недостижимым из стартового состояния. Нако
