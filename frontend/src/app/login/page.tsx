"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { BookOpen, GraduationCap, ShieldCheck, UserRound } from "lucide-react";

type Role = "admin" | "teacher" | "student";

export default function LoginPage() {
  const router = useRouter();
  const [role, setRole] = useState<Role>("admin");

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    router.push(role === "teacher" ? "/teacher" : role === "admin" ? "/admin" : "/");
  }

  return (
    <main className="login-shell">
      <section className="login-visual">
        <Link className="brand" href="/" aria-label="SmartCampus accueil">
          <span className="brand-mark"><GraduationCap size={22} /></span>
          <span>SmartCampus <b>AI</b></span>
        </Link>
        <div className="login-copy">
          <div className="eyebrow-inline">Espace institutionnel</div>
          <h1>Gérez votre campus, simplement.</h1>
          <p>Accédez aux outils adaptés à votre profil : pilotage administratif, gestion pédagogique ou accompagnement des étudiants.</p>
        </div>
        <div className="login-trust"><ShieldCheck size={16} /> Connexion sécurisée pour le personnel autorisé</div>
      </section>
      <section className="login-form-wrap">
        <form className="login-form" onSubmit={submit}>
          <div className="eyebrow-inline">Bienvenue</div>
          <h1>Connectez-vous</h1>
          <p>Sélectionnez votre profil puis accédez à votre espace.</p>
          <div className="role-picker" aria-label="Choisir un profil">
            <button type="button" className={role === "admin" ? "active" : ""} onClick={() => setRole("admin")}><ShieldCheck size={19} /> Administrateur</button>
            <button type="button" className={role === "teacher" ? "active" : ""} onClick={() => setRole("teacher")}><UserRound size={19} /> Enseignant</button>
            <button type="button" className={role === "student" ? "active" : ""} onClick={() => setRole("student")}><BookOpen size={19} /> Étudiant</button>
          </div>
          <div className="field"><label htmlFor="email">Adresse électronique</label><input id="email" type="email" placeholder="nom@smartcampus.tn" defaultValue="admin@smartcampus.tn" /></div>
          <div className="field"><label htmlFor="password">Mot de passe</label><input id="password" type="password" placeholder="Votre mot de passe" defaultValue="demo" /></div>
          <div className="login-options"><label><input type="checkbox" defaultChecked /> Se souvenir de moi</label><a href="#">Mot de passe oublié ?</a></div>
          <button className="login-submit" type="submit">Se connecter</button>
          <Link className="login-back" href="/">← Retour à l&apos;assistant</Link>
        </form>
      </section>
    </main>
  );
}
