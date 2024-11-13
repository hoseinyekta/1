from bale import Bot, Update, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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
        user_state[user_id] = 'awaiting_name'

    elif user_state.get(user_id) == 'awaiting_name':
        user_name = message.content

        # ایجاد دکمه‌های انتخاب دوره به صورت جداگانه
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(text="دوره 16", callback_data="course_16"))
        reply_markup.add(InlineKeyboardButton(text="دوره 17", callback_data="course_17"))
        reply_markup.add(InlineKeyboardButton(text="دوره 18", callback_data="course_18"))
        reply_markup.add(InlineKeyboardButton(text="دوره 19", callback_data="course_19"))
        reply_markup.add(InlineKeyboardButton(text="دوره 20", callback_data="course_20"))
        reply_markup.add(InlineKeyboardButton(text="دوره 21", callback_data="course_21"))

        # ارسال دکمه‌های انتخاب دوره
        await message.reply("لطفاً یکی از دوره‌های زیر را انتخاب کنید:", components=reply_markup)

        # ذخیره نام کاربر و تغییر وضعیت به انتظار انتخاب دوره
        user_state[user_id] = {'status': 'awaiting_course', 'name': user_name}

@client.event
async def on_callback(callback: CallbackQuery):
    user_id = callback.message.chat.id

    # بررسی انتخاب دوره توسط کاربر
    if callback.data.startswith("course_") and user_state.get(user_id, {}).get('status') == 'awaiting_course':
        course_number = callback.data.split("_")[1]
        
        # خوش‌آمدگویی به کاربر با ذکر نام و دوره انتخابی
        user_name = user_state[user_id]['name']
        await callback.message.reply(f"آقای {user_name}، به دوره {course_number} خوش آمدید!")

        # ایجاد دکمه شروع چالش
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(text="شروع چالش", callback_data="start_challenge"))

        # ارسال پیام و دکمه برای شروع چالش
        await callback.message.reply("برای شروع چالش روی دکمه زیر کلیک کنید:", components=reply_markup)

        # تغییر وضعیت کاربر به انتظار شروع چالش
        user_state[user_id] = {'status': 'awaiting_choice'}

    elif callback.data == "start_challenge" and user_state.get(user_id, {}).get('status') == 'awaiting_choice':
        location_url = "https://www.google.com/maps?q=35.7449,51.4718"
        await callback.message.reply(f"برای مشاهده موقعیت مکانی به لینک زیر مراجعه کنید:\n{location_url}")

        # درخواست ارسال عکس از کاربر
        user_state[user_id] = {'status': 'awaiting_photo'}
        await callback.message.reply("لطفاً از محل مورد نظر عکسی ارسال کنید.")

    elif callback.data == "start_stage_2":
        # ارسال عکس برج میلاد
        image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjnqUXWsVY47slqhdINrNTLA40y5F_R2lddw&s"
        await callback.message.send_photo(image_url)

        # درخواست اطلاعات در مورد برج میلاد
        await callback.message.reply("حالا هر چیزی که در مورد این سازه می‌دونی برای من بنویس.")
        user_state[user_id] = {'status': 'awaiting_milad_info'}

@client.event
async def on_message(message: Message):
    user_id = message.chat.id

    # دریافت عکس کاربر
    if user_state.get(user_id, {}).get('status') == 'awaiting_photo' and message.photos:
        await message.reply("ممنون که عکس را ارسال کردید!")

        # ایجاد دکمه برای شروع مرحله دوم
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(InlineKeyboardButton(text="شروع مرحله دوم", callback_data="start_stage_2"))

        # ارسال دکمه مرحله دوم
        await message.reply("برای شروع مرحله دوم روی دکمه زیر کلیک کنید:", components=reply_markup)

        user_state[user_id] = {'status': 'awaiting_stage_2'}

    elif user_state.get(user_id, {}).get('status') == 'awaiting_milad_info' and message.content:
        user_info = message.content
        await message.reply(f"ممنون که اطلاعات رو ارسال کردی:\n{user_info}")
        user_state[user_id] = {'status': 'completed'}

client.run()
