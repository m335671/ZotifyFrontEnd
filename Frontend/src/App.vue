<template>
  <div id="app" class="app-layout">
    <header class="navbar">
      <div class="brand">
        <!-- Icône Logo SVG -->
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="logo-icon"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
        <div class="brand-text">
          <h1>Zotify Web</h1>
          <span class="badge">v0.2</span>
        </div>
      </div>
      
      <div class="nav-actions">
        <!-- Sélecteur de Langue (Menu Déroulant) -->
        <div class="lang-selector">
          <select v-model="lang" @change="changeLang" class="lang-select">
            <option value="en">English</option>
            <option value="fr">Français</option>
          </select>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="chevron-down"><path d="m6 9 6 6 6-6"/></svg>
        </div>
        
        <!-- Switch Thème (Lune/Soleil SVG) -->
        <button @click="toggleTheme" class="btn-icon" :title="t('switch_theme')">
          <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
        </button>

        <!-- Lien GitHub avec Icône -->
        <a href="https://github.com/m335671/ZotifyFrontEnd" target="_blank" class="github-link" title="GitHub">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
        </a>
      </div>
    </header>
    
    <main class="dashboard-grid">
      <aside class="sidebar">
        <Settings :lang="lang" :t="t" />
      </aside>
      <section class="content">
        <ZotifyDownloader :lang="lang" :t="t" />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Settings from './components/Settings.vue'
import ZotifyDownloader from './components/ZotifyDownloader.vue'
import translations from './translations.js'

const isDark = ref(false)
const lang = ref('en')

const t = (key) => translations[lang.value]?.[key] || key

const toggleTheme = () => {
  isDark.value = !isDark.value
  updateBodyClass()
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

const updateBodyClass = () => {
  if (isDark.value) document.body.classList.add('dark-mode')
  else document.body.classList.remove('dark-mode')
}

const changeLang = () => {
  localStorage.setItem('lang', lang.value)
}

onMounted(() => {
  const storedTheme = localStorage.getItem('theme')
  if (storedTheme === 'dark') {
    isDark.value = true
    updateBodyClass()
  } else if (!storedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDark.value = true
    updateBodyClass()
  }
  
  const storedLang = localStorage.getItem('lang')
  if (storedLang) lang.value = storedLang
})
</script>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.navbar {
  height: 64px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  flex-shrink: 0;
  transition: background 0.3s, border-color 0.3s;
}

.brand { display: flex; align-items: center; gap: 0.75rem; color: var(--text-primary); }
.brand-text h1 { font-size: 1.1rem; }
.badge {
  background: var(--border);
  color: var(--text-secondary);
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 8px;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.lang-selector {
  position: relative;
  display: flex;
  align-items: center;
}

.lang-select {
  appearance: none;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.4rem 2rem 0.4rem 0.8rem;
  font-size: 0.9rem;
  color: var(--text-primary);
  cursor: pointer;
  transition: border-color 0.2s;
}

.lang-select:hover {
  border-color: var(--text-secondary);
}

.lang-select:focus {
  outline: none;
  border-color: var(--accent);
}

.chevron-down {
  position: absolute;
  right: 8px;
  pointer-events: none;
  color: var(--text-secondary);
}

.btn-icon, .github-link {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.btn-icon:hover, .github-link:hover {
  background: var(--border);
  color: var(--text-primary);
}

.dashboard-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 1.5rem;
  padding: 1.5rem;
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  overflow: hidden; 
}

.sidebar, .content {
  height: 100%;
  overflow: hidden; 
  min-height: 0;
}

@media (max-width: 900px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    overflow-y: auto;
    height: auto;
    display: block; 
  }
  .sidebar { margin-bottom: 1.5rem; height: auto; }
  .content { height: 600px; }
}
</style>