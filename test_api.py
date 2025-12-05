#!/usr/bin/env python3
"""
Скрипт для тестирования API и поиска багов
"""
import requests
import time
import json

BASE_URL = "https://apitests.nyc.wf"
USERNAME = "admin"
PASSWORD = "qazWSXedc"

def test_authorization():
    """Тестирование эндпоинта авторизации"""
    print("\n=== Тестирование авторизации ===")
    
    # Успешная авторизация
    print("\n1. Успешная авторизация")
    response = requests.post(
        f"{BASE_URL}/authorization",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        },
        data={
            "username": USERNAME,
            "password": PASSWORD
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("token")
        balance = data.get("balance")
        print(f"Token: {token}")
        print(f"Balance: {balance}")
        return token, balance
    return None, None

def test_transaction(token, amount=10.00):
    """Тестирование транзакций"""
    print(f"\n=== Тестирование транзакции на сумму {amount} ===")
    
    response = requests.post(
        f"{BASE_URL}/transaction",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "X-Api-Key": token
        },
        data={
            "action": "withdraw",
            "amount": str(amount)
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        return response.json().get("balance")
    return None

def test_logout(token):
    """Тестирование logout"""
    print("\n=== Тестирование logout ===")
    
    response = requests.get(
        f"{BASE_URL}/logout",
        headers={
            "Accept": "application/json",
            "X-Api-Key": token
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    return response.status_code == 200

def test_negative_cases():
    """Тестирование негативных сценариев"""
    print("\n=== Негативные тесты ===")
    
    # Авторизация с неверным паролем
    print("\n1. Авторизация с неверным паролем")
    response = requests.post(
        f"{BASE_URL}/authorization",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        },
        data={
            "username": USERNAME,
            "password": "wrongpassword"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Транзакция без токена
    print("\n2. Транзакция без токена")
    response = requests.post(
        f"{BASE_URL}/transaction",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        },
        data={
            "action": "withdraw",
            "amount": "10.00"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Транзакция с невалидным токеном
    print("\n3. Транзакция с невалидным токеном")
    response = requests.post(
        f"{BASE_URL}/transaction",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "X-Api-Key": "invalid_token_12345"
        },
        data={
            "action": "withdraw",
            "amount": "10.00"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Транзакция с суммой больше баланса
    print("\n4. Транзакция с суммой больше баланса")
    token, _ = test_authorization()
    if token:
        response = requests.post(
            f"{BASE_URL}/transaction",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "X-Api-Key": token
            },
            data={
                "action": "withdraw",
                "amount": "20000.00"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    print("Начало тестирования API")
    print("=" * 50)
    
    # Основные тесты
    token, initial_balance = test_authorization()
    
    if token:
        # Тест транзакции
        new_balance = test_transaction(token, 10.00)
        if new_balance:
            print(f"\nБаланс изменился: {initial_balance} -> {new_balance}")
        
        # Тест logout
        test_logout(token)
        
        # Попытка использовать токен после logout
        print("\n=== Попытка использовать токен после logout ===")
        test_transaction(token, 10.00)
    
    # Негативные тесты
    test_negative_cases()
    
    print("\n" + "=" * 50)
    print("Тестирование завершено")

