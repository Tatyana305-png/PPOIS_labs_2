// Основной JavaScript файл
// Утилиты для всего приложения

// Функция для отображения уведомлений
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem;
        border-radius: 0.5rem;
        background: var(--darker);
        border: 1px solid var(--border);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;

    if (type === 'success') {
        notification.style.borderColor = 'var(--secondary)';
        notification.style.color = 'var(--secondary)';
    } else if (type === 'error') {
        notification.style.borderColor = 'var(--danger)';
        notification.style.color = 'var(--danger)';
    }

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Добавляем анимации в CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Функция для копирования текста в буфер обмена
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Скопировано в буфер обмена!', 'success');
    } catch (err) {
        showNotification('Не удалось скопировать', 'error');
    }
}

// Обработчики для всех страниц
document.addEventListener('DOMContentLoaded', () => {
    // Добавляем кнопки копирования для блоков с кодом
    document.querySelectorAll('pre, .code-editor').forEach(block => {
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        block.parentNode.insertBefore(wrapper, block);
        wrapper.appendChild(block);

        const copyBtn = document.createElement('button');
        copyBtn.textContent = '📋 Копировать';
        copyBtn.className = 'copy-btn';
        copyBtn.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            padding: 0.25rem 0.5rem;
            font-size: 0.75rem;
            background: var(--primary);
            border: none;
            border-radius: 0.25rem;
            color: white;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.3s;
        `;

        wrapper.addEventListener('mouseenter', () => {
            copyBtn.style.opacity = '1';
        });

        wrapper.addEventListener('mouseleave', () => {
            copyBtn.style.opacity = '0';
        });

        copyBtn.addEventListener('click', () => {
            copyToClipboard(block.textContent);
        });

        wrapper.appendChild(copyBtn);
    });
});