<template>
  <div class="card settings-card">
    <h3 class="section-title">⚙️ Configuration</h3>
    
    <div class="scroll-area">
      <div class="form-group">
        <label>Client ID Spotify</label>
        <input 
          v-model="settings.client_id" 
          type="text" 
          placeholder="Entrez votre Client ID" 
          class="form-input"
        />
        <small class="hint">Requis pour l'accès API</small>
      </div>

      <div class="form-group">
        <label>Dossier de sortie</label>
        <input  
          v-model="settings.output_dir" 
          type="text" 
          placeholder="./downloads" 
          class="form-input"
        />
      </div>

      <div class="form-group">
        <label>Qualité Audio</label>
        <select v-model="settings.quality" class="form-input">
          <option value="very_high">Très Haute (320kbps)</option>
          <option value="high">Haute</option>
          <option value="medium">Moyenne</option>
          <option value="low">Basse</option>
        </select>
      </div>

      <div class="toggles-wrapper">
        <label class="toggle-row">
          <span>Mode Temps Réel (Anti-ban)</span>
          <input type="checkbox" v-model="settings.realtime" class="toggle-switch" />
        </label>
        <label class="toggle-row">
          <span>Métadonnées & Cover</span>
          <input type="checkbox" v-model="settings.embed_metadata" class="toggle-switch" />
        </label>
        <label class="toggle-row">
          <span>Paroles (Lyrics)</span>
          <input type="checkbox" v-model="settings.download_lyrics" class="toggle-switch" />
        </label>
      </div>
      
      <div class="form-group">
        <label>Attente entre téléchargements (sec)</label>
        <input 
          v-model.number="settings.bulk_wait_time" 
          type="number" 
          min="5" 
          class="form-input"
        />
      </div>
    </div>

    <div class="status-bar">
      <transition name="fade">
        <span v-if="status" :class="['status-pill', { success: saved, error: !saved }]">
          {{ status }}
        </span>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const settings = ref({
  client_id: '',
  output_dir: './downloads',
  realtime: true,
  embed_metadata: true,
  download_lyrics: false,
  quality: 'high',
  bulk_wait_time: 30,
})

const saved = ref(false)
const status = ref('')

const loadSettings = () => {
  const stored = localStorage.getItem('zotify-settings')
  if (stored) {
    try {
      Object.assign(settings.value, JSON.parse(stored))
    } catch (e) { console.error(e) }
  }
}

const saveSettings = () => {
  try {
    localStorage.setItem('zotify-settings', JSON.stringify(settings.value))
    saved.value = true
    status.value = 'Sauvegardé automatiquement'
    setTimeout(() => status.value = '', 2000)
  } catch (e) {
    saved.value = false
    status.value = 'Erreur sauvegarde'
  }
}

onMounted(loadSettings)
watch(settings, saveSettings, { deep: true })
</script>

<style scoped>
.settings-card {
  display: flex;
  flex-direction: column;
}

.section-title {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.scroll-area {
  flex: 1;
  overflow-y: auto;
  padding-right: 0.5rem; /* Pour la scrollbar */
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.hint {
  display: block;
  margin-top: 0.25rem;
  color: var(--text-secondary);
  font-size: 0.8rem;
}

.toggles-wrapper {
  background: #f8fafc;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border);
}

.toggle-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  cursor: pointer;
  font-size: 0.9rem;
}

.status-bar {
  margin-top: 1rem;
  height: 24px;
  display: flex;
  justify-content: center;
}

.status-pill {
  font-size: 0.8rem;
  padding: 2px 10px;
  border-radius: 12px;
  background: #e2e8f0;
  color: var(--text-secondary);
}

.status-pill.success {
  background: #dcfce7;
  color: #166534;
}

/* Animations */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>