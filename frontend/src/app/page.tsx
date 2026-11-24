"use client";

import { FormEvent, useState } from "react";
import {
  ArrowUp,
  BookOpen,
  CalendarDays,
  GraduationCap,
  MessageCircle,
  RotateCcw,
  ShieldCheck,
  Sparkles,
  UserRound,
} from "lucide-react";
import Link from "next/link";

type Message = { role: "user" | "assistant"; content: string };
const suggestions = ["Quelles formations sont disponibles ?", "Quelles sont les conditions d’admission ?", "Comment fonctionne la préinscription ?"];
const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [notice, setNotice] = useState("");

  async function sendMessage(text: string) {
    const value = text.trim();
    if (!value || busy) return;
    setInput("");
    setNotice("");
    setMessages((current) => [...current, { role: "user", content: value }]);
    setBusy(true);
    try {
      const response = await fetch(`${apiUrl}/chat`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: value, session_id: sessionId }),
      });
      if (!response.ok) throw new Error("Le service de conversation est momentanément indisponible.");
      const data: { reply: string; session_id?: string } = await response.json();
      if (data.session_id) setSessionId(data.session_id);
      setMessages((current) => [...current, { role: "assistant", content: data.reply }]);
    } catch {
      setNotice("Impossible de joindre l’API. Vérifiez que le backend est démarré, puis réessayez.");
      setMessages((current) => current.slice(0, -1));
    } finally { setBusy(false); }
  }

  function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); void sendMessage(input); }
  function reset() { setMessages([]); setSessionId(null); setNotice(""); }

  return (
    <main className="shell">
      <header className="topbar">
        <Link className="brand" href="/" aria-label="SmartCampus AI, accueil"><span className="brand-mark"><GraduationCap size={22} /></span><span>SmartCampus <b>AI</b></span></Link>
        <nav aria-label="Navigation principale">
          <a href="#formations"><BookOpen size={16} /> Formations</a>
          <a href="#preinscription"><CalendarDays size={16} /> Préinscription</a>
          <Link className="staff-link" href="/login"><UserRound size={15} /> Espace personnel</Link>
        </nav>
      </header>
      <section className="chat-card" aria-label="Assistant d’orientation">
        <div className="chat-heading">
          <div>
            <div className="eyebrow"><ShieldCheck size={13} /> VOTRE ORIENTATION, EN CLAIR</div>
            <h1>Bonjour, que souhaitez-vous explorer&nbsp;?</h1>
            <p>Posez vos questions sur les formations et les démarches d’admission.</p>
          </div>
          <button className="icon-button" onClick={reset} aria-label="Nouvelle conversation" title="Nouvelle conversation"><RotateCcw size={18} /></button>
        </div>
        {messages.length === 0 ? <div className="welcome"><div className="assistant-icon"><Sparkles size={21} /></div><p>Je peux vous aider à découvrir les parcours et les étapes de candidature.</p><div className="suggestions">{suggestions.map((question) => <button key={question} onClick={() => void sendMessage(question)}>{question}<ArrowUp size={14} /></button>)}</div></div> : <div className="messages" aria-live="polite">{messages.map((message, index) => <div className={`message ${message.role}`} key={`${index}-${message.role}`}><span>{message.role === "assistant" ? "Assistant" : "Vous"}</span><p>{message.content}</p></div>)}{busy && <div className="typing" aria-label="Réponse en cours"><i /><i /><i /></div>}</div>}
        {notice && <p className="error" role="alert">{notice}</p>}
        <form className="composer" onSubmit={submit}><label className="sr-only" htmlFor="question">Votre question</label><input id="question" value={input} onChange={(event) => setInput(event.target.value)} placeholder="Écrivez votre question…" disabled={busy} /><button type="submit" disabled={!input.trim() || busy} aria-label="Envoyer"><ArrowUp size={19} /></button></form>
        <div className="disclaimer"><MessageCircle size={14} /> Réponses de démonstration, générées sans intelligence artificielle.</div>
      </section>
      <footer><span>SmartCampus AI · Orientation universitaire</span><span>Les informations affichées sont fournies à titre de démonstration.</span></footer>
      <span id="formations" className="sr-only">Catalogue des formations en préparation</span><span id="preinscription" className="sr-only">Préinscription en préparation</span>
    </main>
  );
}
