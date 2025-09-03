document.addEventListener('DOMContentLoaded', () => {
    const qs = (s) => document.querySelector(s);

    // Получаем все нужные элементы со страницы
    const registerSection = qs('#register-section');
    const loginSection = qs('#login-section');

    const registerForm = qs('#register-form');
    const loginForm = qs('#login-form');

    const registerResult = qs('#register-result');
    const loginResult = qs('#login-result');

    const toLoginLink = qs('#to-login');
    const toRegisterLink = qs('#to-register');

    // Функция для переключения между секциями
    function show(section) {
        if (!section) return;
        [registerSection, loginSection].forEach(s => s && s.classList.add('hidden'));
        section.classList.remove('hidden');
    }

    // Навигация между формами
    if (toLoginLink) {
        toLoginLink.addEventListener('click', (e) => {
            e.preventDefault();
            show(loginSection);
        });
    }

    if (toRegisterLink) {
        toRegisterLink.addEventListener('click', (e) => {
            e.preventDefault();
            show(registerSection);
        });
    }

    // Обработчик формы регистрации
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            registerResult.textContent = '';
            registerResult.classList.remove('error');
            const form = new FormData(registerForm);
            const payload = Object.fromEntries(form.entries());

            // Добавляем недостающие поля, которые не вводятся пользователем
            payload.number = 0; // Значение по умолчанию для номера
            payload['ʕ·ᴥ·ʔ'] = new Date().toISOString().split('T')[0]; // Текущая дата в формате YYYY-MM-DD

            try {
                const res = await fetch(`${window.API_BASE}/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data?.detail || 'Ошибка регистрации');
                registerResult.textContent = `Успех! Теперь вы можете войти.`;
                show(loginSection);
            } catch (err) {
                registerResult.textContent = err.message;
                registerResult.classList.add('error');
            }
        });
    }

    // Обработчик формы входа
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            loginResult.textContent = '';
            loginResult.classList.remove('error');
            const form = new FormData(loginForm);
            const payload = Object.fromEntries(form.entries());
            try {
                const res = await fetch(`${window.API_BASE}/login_user`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data?.detail || 'Неверный логин или пароль');

                // Сохраняем токен в localStorage для возможного использования на других страницах.
                // Backend возвращает токен в поле 'token'.
                localStorage.setItem('token', data.token);
                window.location.href = 'main.html';
            } catch (err) {
                loginResult.textContent = err.message;
                loginResult.classList.add('error');
            }
        });
    }

    // При загрузке страницы, показываем форму регистрации
    show(registerSection);
});