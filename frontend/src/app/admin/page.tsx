"use client";

import Link from "next/link";
import {
  Bell, BookOpen, GraduationCap, LayoutDashboard, Settings, Users,
  Building2, UserPlus, ClipboardCheck, Search, ChevronRight,
} from "lucide-react";

const activities = [
  ["YA", "Yassine A.", "Nouveau dossier étudiant", "Il y a 8 min", "wait"],
  ["MN", "Meriem N.", "Modification de filière", "Il y a 24 min", "ok"],
  ["KB", "Khalil B.", "Préinscription validée", "Il y a 1 h", "ok"],
];

export default function AdminDashboard() {
  return (
    <main className="portal-shell portal-layout">
      <aside className="sidebar">
        <Link className="sidebar-brand" href="/"><span className="brand-mark"><GraduationCap size={21} /></span><strong>SmartCampus <span>AI</span></strong></Link>
        <nav className="sidebar-nav" aria-label="Administration">
          <Link className="active" href="/admin"><LayoutDashboard size={17} /><span>Vue d&apos;ensemble</span></Link>
          <Link href="/admin"><Users size={17} /><span>Utilisateurs</span></Link>
          <Link href="/admin"><BookOpen size={17} /><span>Formations</span></Link>
          <Link href="/admin"><Building2 size={17} /><span>Départements</span></Link>
          <Link href="/admin"><ClipboardCheck size={17} /><span>Préinscriptions</span></Link>
          <Link href="/admin"><Settings size={17} /><span>Paramètres</span></Link>
        </nav>
        <div className="sidebar-profile"><div className="avatar">YA</div><div><strong>Yassine Admin</strong><small>Administrateur</small></div></div>
      </aside>
      <section className="portal-main">
        <header className="portal-topbar"><h2>Administration</h2><div className="topbar-actions"><button aria-label="Rechercher"><Search size={16} /></button><button aria-label="Notifications"><Bell size={16} /></button></div></header>
        <div className="portal-content">
          <div className="page-heading"><div><span className="eyebrow-inline">Tableau de bord</span><h1>Bonjour, Yassine</h1><p>Voici l&apos;activité de votre établissement aujourd&apos;hui.</p></div><button className="primary-button"><UserPlus size={16} /><span>Ajouter un utilisateur</span></button></div>
          <div className="stats-grid">
            <div className="stat-card"><div><small>Étudiants</small><strong>1 284</strong></div><div className="stat-icon"><Users size={20} /></div></div>
            <div className="stat-card"><div><small>Enseignants</small><strong>86</strong></div><div className="stat-icon blue"><UserPlus size={20} /></div></div>
            <div className="stat-card"><div><small>Formations</small><strong>24</strong></div><div className="stat-icon orange"><BookOpen size={20} /></div></div>
            <div className="stat-card"><div><small>Préinscriptions</small><strong>342</strong></div><div className="stat-icon violet"><ClipboardCheck size={20} /></div></div>
          </div>
          <div className="dashboard-grid">
            <div className="panel">
              <div className="panel-heading"><h3>Évolution des préinscriptions</h3><button>Cette année <ChevronRight size={12} /></button></div>
              <div className="bar-chart">
                {[42,58,46,72,64,86,78,92,68,74,88,96].map((height, index) => <div className="bar-item" key={index}><div className="bar" style={{ height: `${height}%` }} /><span>{["Jan","Fév","Mar","Avr","Mai","Jun","Jul","Aoû","Sep","Oct","Nov","Déc"][index]}</span></div>)}
              </div>
            </div>
            <div className="panel">
              <div className="panel-heading"><h3>Activités récentes</h3><Link href="/admin">Voir tout</Link></div>
              <div className="activity-list">{activities.map(([initials, name, action, time, status]) => <div className="activity-row" key={name}><div className="avatar">{initials}</div><div><strong>{name}</strong><small>{action} · {time}</small></div><span className={`status ${status}`}>{status === "ok" ? "Validé" : "En attente"}</span></div>)}</div>
            </div>
          </div>
          <div className="panel table-panel">
            <div className="panel-heading"><h3>Dernières préinscriptions</h3><Link href="/admin">Voir toutes les demandes</Link></div>
            <table className="data-table"><thead><tr><th>Candidat</th><th>Formation</th><th>Date</th><th>Statut</th></tr></thead><tbody>
              <tr><td>Amine Ben Salah</td><td>Licence Informatique</td><td>20/11/2026</td><td><span className="status wait">En attente</span></td></tr>
              <tr><td>Salma Trabelsi</td><td>Master IA &amp; Data</td><td>19/11/2026</td><td><span className="status ok">Validé</span></td></tr>
              <tr><td>Nour Mansour</td><td>Licence Génie logiciel</td><td>18/11/2026</td><td><span className="status ok">Validé</span></td></tr>
            </tbody></table>
          </div>
        </div>
      </section>
    </main>
  );
}
