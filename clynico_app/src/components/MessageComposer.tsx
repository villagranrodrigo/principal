import { useEffect, useState } from 'react';
import type { MessagingChannel } from '../types';

interface MessageComposerProps {
  onSend: (subject: string, body: string, channel: MessagingChannel) => Promise<void>;
  defaultChannel: MessagingChannel;
  disabled?: boolean;
}

const CHANNEL_OPTIONS: MessagingChannel[] = ['chat', 'sms'];

export function MessageComposer({ onSend, defaultChannel, disabled }: MessageComposerProps) {
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [channel, setChannel] = useState<MessagingChannel>(defaultChannel);
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);

  useEffect(() => {
    setChannel(defaultChannel);
  }, [defaultChannel]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!subject || !body) {
      setFeedback('Completa asunto y mensaje antes de enviar.');
      return;
    }
    setLoading(true);
    setFeedback(null);
    try {
      await onSend(subject, body, channel);
      setFeedback('Mensaje enviado correctamente.');
      setSubject('');
      setBody('');
    } catch (error) {
      console.error(error);
      setFeedback('No se pudo enviar el mensaje. Verifica la consola.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="message-composer" onSubmit={handleSubmit}>
      <h3>Enviar mensaje</h3>
      <label>
        Asunto
        <input value={subject} onChange={(event) => setSubject(event.target.value)} disabled={disabled || loading} />
      </label>
      <label>
        Mensaje
        <textarea value={body} onChange={(event) => setBody(event.target.value)} disabled={disabled || loading} />
      </label>
      <label>
        Canal
        <select value={channel} onChange={(event) => setChannel(event.target.value as MessagingChannel)} disabled={disabled || loading}>
          {CHANNEL_OPTIONS.map((option) => (
            <option key={option} value={option}>
              {option.toUpperCase()}
            </option>
          ))}
        </select>
      </label>
      <button className="primary" type="submit" disabled={disabled || loading}>
        {loading ? 'Enviando…' : 'Enviar mensaje'}
      </button>
      {feedback && <small>{feedback}</small>}
    </form>
  );
}
