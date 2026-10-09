import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешает сайту отправлять запросы на сервер

# Данные вашего бота
TELEGRAM_BOT_TOKEN = "8971080508:AAE1lfKSin_j-MbaJiiNwC0k_Dy-zbFh7Sc"
TELEGRAM_CHAT_ID = "678554572"  # Ваш ID в Telegram


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        response = requests.post(url, json=payload)
        res_data = response.json()
        print("Ответ от Telegram:", res_data)
        return res_data
    except Exception as e:
        print("Ошибка при отправке в Telegram:", e)
        return None


@app.route("/api/order", methods=["POST"])
def handle_order():
    data = request.json or {}
    print("Получены данные заказа:", data)

    customer_name = data.get("name", "Не указано")
    phone = data.get("phone", "Не указано")
    address = data.get("address", "Не указано")
    items = data.get("items", [])
    total = data.get("total", 0)

    # Собираем список товаров (учитываем ключ 'title' или 'name')
    items_list = []
    for item in items:
        title = item.get("title") or item.get("name") or "Товар"
        qty = item.get("quantity", 1)
        price = item.get("price", 0)
        items_list.append(f"• {title} — {qty} шт. ({price * qty} сом)")

    items_text = (
        "\n".join(items_list) if items_list else "Список товаров пуст"
    )

    message = (
        f"🛍 <b>НОВЫЙ ЗАКАЗ С САЙТА!</b>\n\n"
        f"👤 <b>Покупатель:</b> {customer_name}\n"
        f"📞 <b>Телефон:</b> {phone}\n"
        f"📍 <b>Адрес:</b> {address}\n\n"
        f"📦 <b>Состав заказа:</b>\n{items_text}\n\n"
        f"💰 <b>Итого к оплате:</b> {total} сом"
    )

    send_telegram_message(message)
    return jsonify({"status": "success", "message": "Заказ успешно отправлен!"})


if __name__ == "__main__":
    print("Сервер запущен и ждет заказов...")
    app.run(port=5000, debug=True)