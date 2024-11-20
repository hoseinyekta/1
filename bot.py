from bale import Bot, CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

client = Bot(token="1562214393:dFPqfNhCKtsy7bWkkwbZgkK8N5coQSPy5hRwFzLH")

# ذخیره وضعیت کاربر
user_state = {}

@client.event
async def on_ready():
    print(client.user.username, "is Ready!")

@client.event
async def on_message(message: Message):
    user_id = message.chat.id

    if message.content == "/start":
        # درخواست نام و نام خانوادگی از کاربر
        await message.reply('نام و نام خانوادگی قرآن آموز را وارد کنید:')
        user_state[user_id] = {'status': 'awaiting_name'}

    elif user_state.get(user_id, {}).get('status') == 'awaiting_name':
        user_name = message.content

        # ایجاد دکمه‌های انتخاب دوره به صورت جداگانه
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(text="دوره 16", callback_data="course_16"), row=1)
        reply_markup.add(InlineKeyboardButton(text="دوره 17", callback_data="course_17"), row=2)
        reply_markup.add(InlineKeyboardButton(text="دوره 18", callback_data="course_18"), row=3)
        reply_markup.add(InlineKeyboardButton(text="دوره 19", callback_data="course_19"), row=4)
        reply_markup.add(InlineKeyboardButton(text="دوره 20", callback_data="course_20"), row=5)
        reply_markup.add(InlineKeyboardButton(text="دوره 21", callback_data="course_21"), row=6)

        # ارسال دکمه‌های انتخاب دوره
        await message.reply("لطفاً یکی از دوره‌های زیر را انتخاب کنید:", components=reply_markup)

        # ذخیره نام کاربر و تغییر وضعیت به انتظار انتخاب دوره
        user_state[user_id] = {'status': 'awaiting_course', 'name': user_name}

    elif user_state.get(user_id, {}).get('status') == 'awaiting_course':
        await message.reply("لطفاً یکی از دوره‌ها را از دکمه‌ها انتخاب کنید.")

    elif user_state.get(user_id, {}).get('status') == 'awaiting_photo' and message.photos:
        # دریافت عکس از کاربر
        await message.reply("ممنون که عکس را ارسال کردید!")

        # ایجاد دکمه برای شروع مرحله دوم
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(text="شروع مرحله دوم", callback_data="start_stage_2"))

        # ارسال دکمه مرحله دوم
        await message.reply("برای شروع مرحله دوم روی دکمه زیر کلیک کنید:", components=reply_markup)

        user_state[user_id] = {'status': 'awaiting_stage_2'}

@client.event
async def on_callback(callback: CallbackQuery):
    user_id = callback.message.chat.id

    # بررسی انتخاب دوره توسط کاربر
    if callback.data.startswith("course_") and user_state.get(user_id, {}).get('status') == 'awaiting_course':
        course_number = callback.data.split("_")[1]
        
        # خوش‌آمدگویی به کاربر با ذکر نام و دوره انتخابی
        user_name = user_state[user_id]['name']
        await callback.message.reply(f"آقای {user_name}، به دوره {course_number} خوش آمدید!")

        # ارسال لوکیشن خاص
        location_url = "https://www.google.com/maps?q=35.7449,51.4718"
        await callback.message.reply(f"برای مشاهده موقعیت مکانی به لینک زیر مراجعه کنید:\n{location_url}")

        # درخواست ارسال عکس از کاربر
        user_state[user_id] = {'status': 'awaiting_photo'}
        await callback.message.reply("لطفاً از محل مورد نظر عکسی ارسال کنید.")

    elif callback.data == "start_stage_2" and user_state.get(user_id, {}).get('status') == 'awaiting_stage_2':
        # درخواست توضیح در مورد دهه فجر
        await callback.message.reply("لطفاً به طور خلاصه دهه فجر را توضیح دهید.")
        
        # تغییر وضعیت کاربر به انتظار دریافت توضیحات
        user_state[user_id] = {'status': 'awaiting_fajr_info'}

    elif user_state.get(user_id, {}).get('status') == 'awaiting_fajr_info' and message.content:
        # دریافت توضیحات از کاربر در مورد دهه فجر
        user_info = message.content
        await message.reply(f"ممنون که توضیحات رو ارسال کردی:\n{user_info}")
        user_state[user_id] = {'status': 'completed'}

client.run()
