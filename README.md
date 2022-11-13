# TextRegognition
Распознавание текста на фотографии
Цель работы: 
1) Обучить нейронную сеть
2) Применить обученную нейросеть для распознавания текста на фотографии
3) Реализовать перевод текста на фотографии

 Обучение.
Попытаемся обучить сверточную нейронную сеть. Для обучения возьмем датасет EMNIST. Код в файле neuron_learning.py. Обучение будем проводить с функцией активации ReLu, обучение заняло около 13 часов, точность в конце обучения достигала 0,805. Обученную модель сохраняем в папке под именем neuron.h5.
 Проверка.
Для начала надо обработать изображение для распознавания текста. Разобьем текст на картинке с помощью функций библиотеки cv2 (Предварительно необходимо установить такие библиотеки: cv2, numpy, keras, tensorflow, idx2numpy, matplotlib, впоследствии pytesseract и googletrans). Код в файле detect.py. Функцией letters_extract разбиваем строку на буквы. Далее функция emnist_predict_img получает на вход букву, которой ставит в соответствие наиболее похожий (по мнению только что обученной нейронной сети) символ - один из 62 символов алфавита EMNIST.
Затем функция img_to_str формирует строку из символов, полученных применением функции emnist_predict_img отдельно к каждой букве исходной картинки. 
Видим, что нейронная сеть не самая точная, может распознать избранный набор заглавных латинских букв, со строчными беда. Для перевода текста не подойдет. Вспоминаем, что существует библиотека tesseract и пишем 3 строчки кода в tess.py.
 Перевод.
Для перевода полученной строки на различные языки мира, воспользуемся библиотекой googletrans. Код представлен в файле translater.py. 
