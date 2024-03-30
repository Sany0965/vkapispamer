import requests
from colorama import Fore, Style  

def get_user_friends(token):
    try:
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params={
                'access_token': token,
                'v': '5.131',
                'fields': 'first_name,last_name'  
            }
        )
        data = response.json()
        if 'response' in data:
            return data['response']['items']
        else:
            if 'error' in data:
                print("Ошибка при получении списка друзей:", data['error']['error_msg'])
            else:
                print("Произошла неизвестная ошибка при получении списка друзей.")
            return []
    except Exception as e:
        print("Произошла ошибка при обращении к API:", e)
        return []

def main():
    while True:
        token = input("Введите токен ВКонтакте: ")
        user_friends = get_user_friends(token)
        
        if not user_friends:
            print("Не удалось получить список друзей. Проверьте токен и повторите попытку.")
            continue

        print("Список ваших друзей и их ID:")
        for i, friend in enumerate(user_friends, 1):
            print(f"{i}. {friend['first_name']} {friend['last_name']} (id: {friend['id']})")

        friend_numbers_input = input("Введите номера друзей, которым хотите отправить сообщение (через пробел), или * для отправки всем: ")
        friend_numbers = [int(num) for num in friend_numbers_input.split() if num.isdigit()]
        
        selected_friends = []
        for num in friend_numbers:
            if num > 0 and num <= len(user_friends):
                selected_friends.append(user_friends[num - 1]['id'])

        if '*' in friend_numbers_input:
            selected_friends = [friend['id'] for friend in user_friends]
        
        if not selected_friends:
            print("Не выбраны друзья для отправки сообщения.")
            continue

        message = input("Введите текст сообщения: ")

        success = send_vk_messages(selected_friends, message, token)
        if success:
            print(Fore.GREEN + "Сообщение успешно отправлено!" + Style.RESET_ALL)
            print("tg:@pizzaway")
        else:
            print("Ошибка при отправке сообщения. Пожалуйста, попробуйте снова.")

        if input("Хотите продолжить (да/нет)? ").lower() != 'да':
            break

def send_vk_messages(user_ids, message, token):
    success = True
    for user_id in user_ids:
        response = requests.post(
            'https://api.vk.com/method/messages.send',
            data={
                'peer_id': user_id,
                'message': message,
                'random_id': 0,
                'access_token': token,
                'v': '5.131'
            }
        )
        if not response.ok or 'error' in response.json():
            success = False
    return success

if __name__ == "__main__":
    main()
