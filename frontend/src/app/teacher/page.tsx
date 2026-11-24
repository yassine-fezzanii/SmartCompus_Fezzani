"use client";

import Link from "next/link";
import { Bell, BookOpen, CalendarDays, GraduationCap, LayoutDashboard, Settings, Users, ClipboardCheck, Search, ChevronRight } from "lucide-react";

const classes = [
  ["Développement Web", "L3 Informatique", "08:30", "#168c91"],
  ["Bases de données", "L2 Génie logiciel", "10:30", "#4d73a7"],
  ["Intelligence artificielle", "M1 IA & Data", "13:30", "#8069b5"],
];

export default function TeacherDashboard() {
  return (
    <main className="portal-shell portal-layout">
      <aside className="sidebar">
        <Link className="sidebar-brand" href="/"><span className="brand-mark"><GraduationCap size={21} /></span><strong>SmartCampus <span>AI</span></strong></Link>
        <nav className="sidebar-nav" aria-label="Enseignant">
          <Link className="active" href="/teacher"><LayoutDashboard size={17} /><span>Tableau de bord</span></Link>
          <Link href="/teacher"><BookOpen size={17} /><span>Mes cours</span></Link>
          <Link href="/teacher"><Users size={17} /><span>Étudiants</span></Link>
          <Link href="/teacher"><CalendarDays size={17} /><span>Emploi du temps</span></Link>
          <Link href="/teacher"><ClipboardCheck size={17} /><span>Notes &amp; évaluations</span></Link>
          <Link href="/teacher"><Settings size={17} /><span>Paramètres</span></Link>
        </nav>
        <div className="sidebar-profile"><div className="avatar">HB</div><div><strong>Dr. H. Ben Ali</strong><small>Enseignant</small></div></div>
      </aside>
      <section className="portal-main">
        <header className="portal-topbar"><h2>Espace enseignant</h2><div className="topbar-actions"><button aria-label="Rechercher"><Search size={16} /></button><button aria-label="Notifications"><Bell size={16} /></button></div></header>
        <div className="portal-content">
          <div className="page-heading"><div><span className="eyebrow-inline">Vendredi 20 novembre</span><h1>Bonjour, Dr. Ben Ali</h1><p>Votre journée pédagogique en un coup d&apos;œil.</p></div><button className="primary-button"><ClipboardCheck size={16} /><span>Ajouter une évaluation</span></button></div>
          <div className="stats-grid">
            <div className="stat-card"><div><small>Cours cette semaine</small><strong>12</strong></div><div className="stat-icon"><BookOpen size={20} /></div></div>
            <div className="stat-card"><div><small>Étudiants</small><strong>148</strong></div><div className="stat-icon blue"><Users size={20} /></div></div>
            <div className="stat-card"><div><small>Travaux à corriger</small><strong>28</strong></div><div className="stat-icon orange"><ClipboardCheck size={20} /></div></div>
            <div className="stat-card"><div><small>Taux de présence</small><strong>91%</strong></div><div className="stat-icon violet"><CalendarDays size={20} /></div></div>
          </div>
          <div className="dashboard-grid">
            <div className="panel">
              <div className="panel-heading"><h3>Emploi du temps — semaine</h3><button>Cette semaine <ChevronRight size={12} /></button></div>
              <div className="schedule-grid">
                {["Lundi","Mardi","Mercredi","Jeudi","Vendredi"].map((day, dayIndex) => <div className="schedule-day" key={day}><strong>{day}</strong>{classes.filter((_, index) => (index + dayIndex) % 3 !== 1).slice(0, dayIndex === 4 ? 2 : 1).map(([name, section, time, color]) => <div className="course" key={`${day}-${name}`} style={{ borderLeftColor: color }}><b>{name}</b><small>{section} · {time}</small></div>)}</div>)}
              </div>
            </div>
            <div className="panel">
              <div className="panel-heading"><h3>Cours du jour</h3><Link href="/teacher">Voir tout</Link></div>
              <div className="activity-list">{classes.map(([name, section, time]) => <div className="activity-row" key={name}><div className="avatar"><BookOpen size={15} /></div><div><strong>{name}</strong><small>{section} · Salle B12</small></div><span className="status ok">{time}</span></div>)}</div>
            </div>
          </div>
          <div className="panel table-panel">
            <div className="panel-heading"><h3>Évaluations récentes</h3><Link href="/teacher">Gérer les notes</Link></div>
            <table className="data-table"><thead><tr><th>Évaluation</th><th>Classe</th><th>Remise</th><th>Statut</th></tr></thead><tbody>
              <tr><td>Projet React / FastAPI</td><td>L3 Informatique</td><td>22/11/2026</td><td><span className="status wait">À corriger</span></td></tr>
              <tr><td>Contrôle SQL</td><td>L2 Génie logiciel</td><td>18/11/2026</td><td><span className="status ok">Publié</span></td></tr>
              <tr><td>Mini-projet IA</td><td>M1 IA &amp; Data</td><td>15/11/2026</td><td><span className="status ok">Publié</span></td></tr>
            </tbody></table>
          </div>
        </div>
      </section>
    </main>
  );
}
