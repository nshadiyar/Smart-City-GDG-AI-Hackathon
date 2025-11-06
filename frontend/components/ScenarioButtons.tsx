import React from 'react';

type Props = {
  onChoose: (text: string) => void;
};

export default function ScenarioButtons({ onChoose }: Props) {
  const scenarios = [
    { label: '30–60 мин возле Mega Silk Way', text: 'Mega Silk Way, 60 min, walk, coffee' },
    { label: 'Тихое кафе с розеткой', text: 'тихое кафе с розеткой' },
    { label: 'С ребёнком поблизости', text: 'с ребёнком поблизости' },
    { label: 'Необычное на ночь', text: 'необычное на ночь' },
  ];

  return (
    <div className="flex flex-wrap gap-2">
      {scenarios.map((s) => (
        <button
          key={s.label}
          className="border rounded-md px-3 py-2 hover:bg-gray-50"
          onClick={() => onChoose(s.text)}
        >
          {s.label}
        </button>
      ))}
    </div>
  );
}


