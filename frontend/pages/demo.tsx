import React, { useState } from 'react';
import ScenarioButtons from '../components/ScenarioButtons';
import ChatPanel from '../components/ChatPanel';

export default function DemoPage() {
  const [text, setText] = useState('');

  return (
    <div className="max-w-3xl mx-auto p-4 flex flex-col gap-4">
      <h1 className="text-2xl font-bold">Demo-сценарии</h1>
      <ScenarioButtons onChoose={(t) => setText(t)} />
      <ChatPanel defaultText={text} />
    </div>
  );
}


