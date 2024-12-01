from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MenuItem, Order, OrderItem
import telebot
import json

# Telegram Bot Token
BOT_TOKEN = "7466824505:AAH3FfBXa9lYWsDZhPO1b5wn23NZmR-7e5Y"
bot = telebot.TeleBot(BOT_TOKEN)

# Serve Menu
def menu_view(request):
    menu_items = MenuItem.objects.all()
    return render(request, "menu.html", {"menu_items": menu_items})

# Place Order
@csrf_exempt
def place_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            # Extract and validate data
            customer_name = data.get("customer_name")
            chat_id = data.get("chat_id")
            items = data.get("items")

            if not (customer_name and chat_id and items):
                return JsonResponse({"error": "Invalid order data"}, status=400)

            # Create Order
            order = Order.objects.create(customer_name=customer_name, chat_id=chat_id)
            total_price = 0

            for item in items:
                try:
                    menu_item = MenuItem.objects.get(id=item["id"])
                except MenuItem.DoesNotExist:
                    return JsonResponse({"error": f"Item ID {item['id']} not found"}, status=400)

                quantity = item["quantity"]
                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)
                total_price += menu_item.price * quantity

            # Update total price and save order
            order.total_price = total_price
            order.save()

            # Notify the user
            bot.send_message(chat_id, f"Order placed! Total: ${total_price:.2f}")

            return JsonResponse({"status": "Order placed successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
