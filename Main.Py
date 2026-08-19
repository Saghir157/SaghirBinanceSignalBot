import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "اپنا_بوٹ_ٹوکن_یہاں_لکھیں"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1 Minute Candle", callback_data="tf_1m")],
        [InlineKeyboardButton("5 Minute Candle", callback_data="tf_5m")],
        [InlineKeyboardButton("15 Minute Candle", callback_data="tf_15m")],
        [InlineKeyboardButton("30 Minute Candle", callback_data="tf_30m")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Binance Candle Prediction Bot\n\nپہلے Candle Timeframe منتخب کریں:",
        reply_markup=reply_markup
    )

async def select_prediction_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    timeframe = query.data.replace("tf_", "")
    context.user_data["timeframe"] = timeframe
    
    keyboard = [
        [InlineKeyboardButton("1 منٹ پہلے", callback_data="pred_1")],
        [InlineKeyboardButton("2 منٹ پہلے", callback_data="pred_2")],
        [InlineKeyboardButton("5 منٹ پہلے", callback_data="pred_5")],
        [InlineKeyboardButton("10 منٹ پہلے", callback_data="pred_10")],
        [InlineKeyboardButton("15 منٹ پہلے", callback_data="pred_15")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"Timeframe: {timeframe}\n\nاب Prediction Time منتخب کریں:",
        reply_markup=reply_markup
    )

async def show_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    pred_time = query.data.replace("pred_", "")
    timeframe = context.user_data.get("timeframe", "15m")
    symbol = "BTCUSDT"
    
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={timeframe}&limit=10"
    
    try:
        response = requests.get(url)
        candles = response.json()
        
        closes = [float(c[4]) for c in candles]
        last_close = closes[-1]
        avg = sum(closes[-5:]) / 5
        
        if last_close > avg:
            direction = "اوپر (Bullish)"
            strength = "مضبوط"
        else:
            direction = "نیچے (Bearish)"
            strength = "کمزور"
        
        message = f"""
Symbol: {symbol}
Candle Timeframe: {timeframe}
Prediction Time: {pred_time} منٹ پہلے

Last Close Price: {last_close}
Average (last 5): {round(avg, 2)}

Prediction:
اگلی کینڈل {direction} جانے کا امکان ہے
Strength: {strength}

نوٹ: یہ بنیادی analysis ہے، حقیقی مارکیٹ میں فرق ہو سکتا ہے۔
"""
        await query.edit_message_text(text=message)
        
    except Exception as e:
        await query.edit_message_text(text="ایرر آیا ہے۔ دوبارہ کوشش کریں۔")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(select_prediction_time, pattern="^tf_"))
    app.add_handler(CallbackQueryHandler(show_prediction, pattern="^pred_"))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
