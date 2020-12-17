Ссылка на работающий проект https://sleepy-waters-05131.herokuapp.com/
# API Reference

Аутентификация реализована с использованием [JWT](https://jpadilla.github.io/django-rest-framework-jwt/),
для аутентификации пользователя в каждый запрос необходимо вставлять заголовок с именем "Authorization"
и значением "JWT \<token\>".

## Users

1. Аутентификация/получение токена
    - uri="token-auth/"
    - method=POST
    - expected_format=JSON
    - expected_fields={"username", "password"}
    - response_format=JSON
    - response_fields={"token", "user": {"id", "username"}}

2. Обновление токена/получение нового токена
    - uri="token-refresh/"
    - method=POST
    - expected_format=JSON
    - expected_fields={"token"}
    - response_format=JSON
    - response_fields={"token", "user": {"id", "username"}}

3. Верификация токена (токен в ответе тот же)
    - uri="token-verify/"
    - method=POST
    - expected_format=JSON
    - expected_fields={"token"}
    - response_format=JSON
    - response_fields={"token", "user": {"id", "username"}}

4. Регистрация, создание нового пользователя
    - uri="users/users/"
    - method=POST
    - expected_format=JSON
    - expected_fields={"username", "password", "avatar"} (avatar не обязательно)
    - response_format=JSON
    - response_fields={"token", "id", "username", "avatar"}
    
5. Получение всех пользователей (аутентификация не требуется)
    - uri="users/users/"
    - method=GET
    - response_format=JSON
    - response_fields={{"id1", "username1", "avatar1"}, {"id2", "username2", "avatar2"}, ...}
    
6. Получение контактов пользователя
    - uri="users/contacts/"
    - method=GET
    - response_format=JSON
    - response_fields={{"id1", "username1", "avatar1", "last_message_text1"},
    {"id2", "username2", "avatar2", "last_message_text2"}, ...}
    
7. Добавление пользователя в контакты
    - uri="users/contacts/"
    - method=POST
    - expected_format=JSON
    - expected_fields={"id"}
    - response_format=JSON
    - response_fields={"success"}

8. Удаление пользователя с id=contact_id из контактов
    - uri="users/contacts/contact_id/"
    - method=DELETE
    - response_format=JSON
    - response_fields={"success"}
    
9. Получение данных текущего пользователя
    - uri="users/current-user/"
    - method=GET
    - response_format=JSON
    - response_fields={"id", "username", "avatar"}
    
## Messages

1. Получение сообщений с пользователем с id=contact_id
    - uri="messages/messages/?contact_id=some_id"
    - method=GET
    - response_format=JSON
    - response_fields={{"id1", "recipient_id1", "text1", "datetime1", "read1", "edited1"},
    {"id2", "recipient_id2", "text2", "datetime2", "read2", "edited2"}, ...}

2. Создание сообщения
    - uri="messages/messages/"
    - method=POST
    - expected_format=JSON
    - expected_fields={"recipient_id", "text", "datetime"}
    - response_format=JSON
    - response_fields={"id", "recipient_id", "text", "datetime", "read", "edited"}

3. Изменение сообщения с id=message_id
    - uri="messages/messages/message_id/"
    - method=PUT
    - expected_format=JSON
    - expected_fields={"text", "read", "edited, "deleted"} (обязателно только text)
    - response_format=JSON  
    - response_fields={"id", "recipient_id", "text", "datetime", "read", "edited", "deleted"}

4. Удаление сообщения с id=message_id (отправителем сообщения должен быть текущий
аутентифицированный пользователь)
    - uri="messages/messages/message_id/"
    - method=DELETE
