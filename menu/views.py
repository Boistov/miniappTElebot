from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MenuItem, Order, OrderItem
import telebot
import json

# Telegram Bot Token
BOT_TOKEN = "7466824505:AAH3FfBXa9lYWsDZhPO1b5wn23NZmR-7e5Y"
bot = telebot.TeleBot(BOT_TOKEN)

# View Menu
def menu_view(request):
    """Serve the dynamic menu."""
    menu_items = MenuItem.objects.all()
    return render(request, "menu.html", {"menu_items": menu_items})

# Handle Order Placement
@csrf_exempt
def place_order(request):
    """Receive order data from the Mini App."""
    if request.method == "POST":
        try:
            data = request.body.decode("utf-8")
            order_data = json.loads(data)
            
            customer_name = order_data.get("customer_name")
            chat_id = order_data.get("chat_id")
            items = order_data.get("items")  # [{id: 1, quantity: 2}, ...]

            if not (customer_name and chat_id and items):
                return JsonResponse({"error": "Invalid order data"}, status=400)

            # Create the Order
            order = Order.objects.create(customer_name=customer_name, chat_id=chat_id)

            # Add Items to Order
            total_price = 0
            for item in items:
                menu_item = MenuItem.objects.get(id=item["id"])
                quantity = item["quantity"]
                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)
                total_price += menu_item.price * quantity

            # Update Total Price
            order.total_price = total_price
            order.save()

            # Notify the Restaurant
            bot.send_message(chat_id, f"Order received! Total: ${total_price:.2f}")

            return JsonResponse({"status": "Order placed successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)
