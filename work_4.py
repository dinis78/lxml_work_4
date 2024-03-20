import requests
from lxml import etree
import csv

# URL страницы для парсинга
url = 'https://news.mail.ru'

# Заголовки HTTP-запроса
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}

try:
    # Отправляем GET-запрос на сайт и получаем HTML-содержимое
    response = requests.get(url, headers=headers)
    
    # Создаем объект парсера XML
    parser = etree.HTMLParser()
    
    # Парсим HTML-содержимое
    tree = etree.fromstring(response.content, parser)
    
    # Выражение XPath для выбора блоков с картинками
    image_blocks_xpath = '//div[@class="newsitem newsitem_height_fixed js-ago-wrapper"]//img'
    
    # Выражение XPath для выбора блоков под картинками
    text_blocks_xpath = '//div[@class="newsitem newsitem_height_fixed js-ago-wrapper"]//span[@class="newsitem__title-inner"]'
    
    # Инициализируем список для сохранения данных
    data = []
    
    # Итерируемся по блокам с картинками
    for block in tree.xpath(image_blocks_xpath)[:5]:
        # Получаем ссылку на изображение
        image_url = block.attrib.get('src')
        
        # Получаем заголовок новости
        title = block.attrib.get('alt')
        
        # Добавляем данные в список
        data.append({'Image URL': image_url, 'Title': title})
    
    # Итерируемся по блокам под картинками
    for block in tree.xpath(text_blocks_xpath)[:8]:
        # Получаем заголовок новости
        title = block.text
        
        # Добавляем данные в список
        data.append({'Title': title})
    
    # Сохраняем данные в CSV-файл
    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Image URL', 'Title'])
        writer.writeheader()
        writer.writerows(data)
        
    print('Данные успешно сохранены в файл data.csv')

except (requests.RequestException, etree.XMLSyntaxError) as e:
    print('Произошла ошибка при выполнении запроса или парсинга HTML:', e)
