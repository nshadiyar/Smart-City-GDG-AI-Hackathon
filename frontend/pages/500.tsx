import React from 'react';

export default function Custom500() {
  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold">500 - Ошибка сервера</h1>
      <p>Произошла внутренняя ошибка сервера.</p>
      <a href="/" className="text-blue-600 hover:underline">Вернуться на главную</a>
    </div>
  );
}

