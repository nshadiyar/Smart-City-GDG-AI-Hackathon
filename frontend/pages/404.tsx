import React from 'react';

export default function Custom404() {
  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold">404 - Страница не найдена</h1>
      <p>Запрашиваемая страница не существует.</p>
      <a href="/" className="text-blue-600 hover:underline">Вернуться на главную</a>
    </div>
  );
}

