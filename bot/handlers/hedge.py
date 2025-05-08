from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.handlers.states import HedgeStates  # import FSM states

router = Router()

@router.message(F.text == "🛡 Hedge")
async def start_hedge(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Buy")], [KeyboardButton(text="Sell")]],
        resize_keyboard=True
    )
    await message.answer("Please choose hedge type:", reply_markup=keyboard)
    await state.set_state(HedgeStates.type)

@router.message(HedgeStates.type)
async def hedge_type(message: Message, state: FSMContext):
    if message.text not in ["Buy", "Sell"]:
        await message.answer("Please choose one of the buttons: Buy or Sell.")
        return
    await state.update_data(type=message.text)

    # New: currency pair options
    pair_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="USD/EUR")],
            [KeyboardButton(text="USD/UAH")],
            [KeyboardButton(text="EUR/PLN")],
            [KeyboardButton(text="Custom pair")]
        ],
        resize_keyboard=True
    )
    await message.answer("Select currency pair:", reply_markup=pair_keyboard)
    await state.set_state(HedgeStates.pair)

@router.message(HedgeStates.pair)
async def hedge_pair(message: Message, state: FSMContext):
    text = message.text.upper()

    if text == "CUSTOM PAIR":
        await message.answer("Please type your custom currency pair (e.g. GBP/JPY):", reply_markup=ReplyKeyboardRemove())
        await state.update_data(pair_mode="custom")  # flag to indicate manual input
        return

    data = await state.get_data()
    if data.get("pair_mode") == "custom":
        # Save whatever the user typed as custom pair
        await state.update_data(pair=text)
        await message.answer("Enter amount (e.g. 10000):")
        await state.set_state(HedgeStates.amount)
        return

    # For predefined pairs
    if text not in ["USD/EUR", "USD/UAH", "EUR/PLN"]:
        await message.answer("Please choose a valid pair from the list or tap 'Custom pair'.")
        return

    await state.update_data(pair=text)
    await message.answer("Enter amount (e.g. 10000):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(HedgeStates.amount)

@router.message(HedgeStates.amount)
async def hedge_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(',', ''))
        await state.update_data(amount=amount)
    except ValueError:
        await message.answer("Please enter a valid numeric amount.")
        return

    data = await state.get_data()
    await message.answer(
        f"✅ Hedge request created:\n"
        f"Type: {data['type']}\n"
        f"Pair: {data['pair']}\n"
        f"Amount: {data['amount']}\n"
        f"(Later this will be saved to DB or sent to admin)"
    )
    await state.clear()
