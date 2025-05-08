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
        await message.answer("Please choose either: Buy or Sell.")
        return
    await state.update_data(type=message.text)
    await message.answer("Enter currency pair (e.g. USD/EUR):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(HedgeStates.pair)

@router.message(HedgeStates.pair)
async def hedge_pair(message: Message, state: FSMContext):
    await state.update_data(pair=message.text.upper())
    await message.answer("Enter amount (e.g. 10000):")
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
