from random import randint
from nicegui import app, ui
import os
from pathlib import Path

STATIC_DIR = Path(__file__).parent / 'static'
app.add_static_files('/static', STATIC_DIR)

@ui.page('/')
def main_page():
    ui.dark_mode().enable()

    ui.add_head_html('''
    <style>
    :root {
        /* Убраны кавычки у HEX-значений */
        --btn: #5440ad;
        --btn-hover: #2d1680;
    }
    body {
        margin: 0;
        padding: 0;
        overflow: hidden;
        background: linear-gradient(150deg, #01073b 0%, #000242 100%);
    }

    /* Стили для кнопок */
    .btn {
        background-color: var(--btn) !important;
        transition: background-color 0.2s ease;
    }
    .btn:hover {
        background-color: var(--btn-hover) !important;
    }

    /* Анимация всплытия текста */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(7px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeInUp 0.4s cubic-bezier(0.16, 0, 0.7, 0.4) forwards;
    }

    /* Движение фоновых кругов */
    @keyframes floatOne {
        0% { transform: translate(0px, 0px) scale(1); }
        50% { transform: translate(60px, 40px) scale(1.4); }
        100% { transform: translate(0px, 0px) scale(1); }
    }

    @keyframes floatTwo {
        0% { transform: translate(0px, 0px) scale(1); }
        50% { transform: translate(-50px, -60px) scale(1.15); }
        100% { transform: translate(0px, 0px) scale(1); }
    }

    @keyframes floatThree {
            0% { transform: translate(0px, 0px) scale(1); }
            50% { transform: translate(-0px, -0px) scale(1.15); }
            100% { transform: translate(0px, 0px) scale(1); }
    }

    /* Круги убраны на задний план через z-index: -1 */
    .bg-circle-1 {
        position: fixed;
        top: 2%;
        left: 27%;
        width: 480px;
        height: 480px;
        background: rgba(99, 102, 241, 0.22);
        border-radius: 50%;
        filter: blur(100px);
        animation: floatOne 14s ease-in-out infinite;
        pointer-events: none;
        z-index: -1;
    }

    .bg-circle-2 {
        position: fixed;
        bottom: 25%;
        right: 20%;
        width: 640px;
        height: 640px;
        background: rgba(236, 72, 153, 0.18);
        border-radius: 50%;
        filter: blur(110px);
        animation: floatTwo 18s ease-in-out infinite;
        pointer-events: none;
        z-index: -1;
    }

    .bg-circle-3 {
            position: fixed;
            top: 70%;
            left: 38%;
            width: 320px;
            height: 320px;
            background: rgba(255, 255, 255, 0.18);
            border-radius: 70%;
            filter: blur(70px);
            animation: floatThree 18s ease-in-out infinite;
            pointer-events: none;
            z-index: -1;
        }
    </style>
    ''')

    # Элементы заднего фона
    ui.element('div').classes('bg-circle-1')
    ui.element('div').classes('bg-circle-2')
    ui.element('div').classes('bg-circle-3')

    state = {'border': 100, 'riddle': None, 'attempts': 0}

    def update_text(label_element, new_text):
        label_element.text = new_text
        label_element.classes(remove='fade-in')
        ui.timer(0.01, lambda: label_element.classes(add='fade-in'), once=True)

    # --- ЛОГИКА ---

    def start_game():
        val = border_input.value
        if val is None or val <= 1 or val % 1 != 0:
            update_text(feedback, '⚠️ Введите целое число больше 1')
            return

        state['border'] = int(val)
        state['riddle'] = randint(1, state['border'])
        state['attempts'] = 0

        border_box.visible = False
        guess_box.visible = True
        restart_btn.visible = False

        guess_input.value = None
        update_text(title, f'Число от 1 до {state["border"]}')
        update_text(feedback, 'Введи свой вариант ниже 👇')

        # Возвращаем фокус в инпут ввода числа
        ui.timer(0.05, lambda: guess_input.run_method('focus'), once=True)

    def check_guess():
        val = guess_input.value
        border = state['border']

        if val is None or val % 1 != 0 or not (1 <= val <= border):
            update_text(feedback, f'⚠️ Число должно быть целым в диапазоне от 1 до {border}')
            guess_input.value = None
            guess_input.run_method('focus')
            return

        state['attempts'] += 1
        n = int(val)
        riddle = state['riddle']

        if n < riddle:
            update_text(feedback, 'Больше! ⬆️')
            guess_input.value = None
            guess_input.run_method('focus')
        elif n > riddle:
            update_text(feedback, 'Меньше! ⬇️')
            guess_input.value = None
            guess_input.run_method('focus')
        else:
            cnt = state['attempts']
            word = '-ей' if (cnt != 13 and cnt % 10 == 3) else '-ой'
            update_text(title, f'Угадано с {cnt}{word} попытки!')
            update_text(feedback, 'Отличная игра!')
            guess_box.visible = False
            restart_btn.visible = True

    def reset_game():
        border_box.visible = True
        guess_box.visible = False
        restart_btn.visible = False
        update_text(title, 'Угадай число')
        update_text(feedback, 'Укажи верхнюю границу диапазона')
        ui.timer(0.05, lambda: border_input.run_method('focus'), once=True)

    # --- ВЕРСТКА С ФЛЕКС-ЦЕНТРИРОВАНИЕМ ---

    with ui.column().classes(
        'w-full min-h-screen justify-center items-center text-center p-4 relative z-10'
    ):

        # Объединяем котиков и заголовок в один горизонтальный ряд
        with ui.row().classes('items-center justify-center gap-3 mb-2 fade-in'):
            ui.image('/static/cat.jpg').classes('w-12 h-12 object-contain')
            
            title = ui.label('Угадай число').classes(
                'text-3xl md:text-4xl font-extrabold text-indigo-400'
            )
            
            # Класс scale-x-[-1] зеркально разворачивает правого котика к заголовку
            ui.image('/static/cat.jpg').classes('w-12 h-12 object-contain')

        feedback = ui.label('Укажи верхнюю границу диапазона').classes(
            'text-slate-300 text-base font-medium mb-6 fade-in'
        )

        # Блок границы
        with ui.column().classes('w-full max-w-md items-center fade-in') as border_box:
            border_input = (
                ui.number(placeholder='Например: 100', value=100)
                .props('outlined dense input-class="text-center"')
                .classes('w-full mb-6')
                .on('keydown.enter', start_game)
            )
            ui.button('Загадать', color=None, on_click=start_game).classes(
                'w-full btn text-white font-bold py-3 rounded-2xl shadow-lg transition-colors'
            )

        # Блок отгадывания
        with ui.column().classes('w-full max-w-md items-center fade-in') as guess_box:
            guess_box.visible = False
            guess_input = (
                ui.number(placeholder='Твое число')
                .props('outlined dense input-class="text-center"')
                .classes('w-full mb-5')
                .on('keydown.enter', check_guess)
            )
            ui.button('Проверить', color=None, on_click=check_guess).classes(
                'w-full btn text-white font-bold py-3 rounded-2xl shadow-lg'
            )

        # Рестарт
        restart_btn = ui.button(
            'Сыграть ещё раз', color=None, on_click=reset_game
        ).classes(
            'w-full max-w-md btn text-white font-bold py-3 rounded-2xl fade-in'
        )
        restart_btn.visible = False

# port = int(os.environ.get('PORT', 8080))
# ui.run(title='Угадай число', host='0.0.0.0', port=port)

ui.run(title='Угадай число', port=8080)