# Альтернативный сервис для отслеживания посылок post.kz.
***
* url/track 
    * 400 - посылка отсутствует в бд
    * 201 - посылка собрана, и ожидает отправки
    * 200 - посылка отправлена
* url/add/track 
  * 200 - трек добавления
  * 400 - трек уже существует