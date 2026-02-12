<template>
  <div id="app" class="app-layout">
    <header class="navbar">
      <div class="brand">
        <span class="logo-icon">🎵</span>
        <div class="brand-text">
          <h1>Zotify Web</h1>
          <span class="badge">v0.1</span>
        </div>
      </div>
      <div class="nav-links">
        <a href="https://github.com/m335671/ZotifyFrontEnd" target="_blank" class="github-link">
          GitHub
        </a>
      </div>
    </header>
    
    <main class="dashboard-grid">
      <aside class="sidebar">
        <Settings />
      </aside>
      <section class="content">
        <ZotifyDownloader />
      </section>
    </main>
  </div>
</template>

<script setup>
import Settings from './components/Settings.vue'
import ZotifyDownloader from './components/ZotifyDownloader.vue'
</script>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.navbar {
  height: 70px;
  background: white;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  flex-shrink: 0;
}

.brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-icon {
  font-size: 1.8rem;
}

.brand-text h1 {
  font-size: 1.2rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.badge {
  background: #f1f5f9;
  color: var(--text-secondary);
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 12px;
  margin-left: 8px;
  vertical-align: middle;
}

.github-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.github-link:hover {
  color: var(--accent);
}

.dashboard-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 320px 1fr; /* Sidebar fixe, reste fluide */
  gap: 2rem;
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
  overflow: hidden; /* Empêche le double scroll */
}

.sidebar, .content {
  height: 100%;
  overflow: hidden; /* Important pour que le scroll se fasse DANS la carte */
}

@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    overflow-y: auto;
  }
  .sidebar {
    height: auto;
  }
  .content {
    height: auto;
    min-height: 500px;
  }
}
</style>