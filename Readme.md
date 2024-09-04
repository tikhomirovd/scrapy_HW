### Описание
Этот проект представляет собой скрапер для сайта Litres, разработанный с использованием Scrapy, а также анализ собранных данных в Jupyter Notebook. 

Клонируем репозиторий
```bash
git clone https://github.com/tikhomirovd/scrapy_HW.git
```

Устанавливаем необходимые зависимости
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Запуск паука
```
cd litres_scraper
scrapy crawl litres -o books.csv
```

### Результаты и анализ
Ознакомиться с результатом остальных заданиях можно [тут](https://github.com/tikhomirovd/scrapy_HW/blob/master/Experiment.ipynb)