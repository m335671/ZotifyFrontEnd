<template>
  <div class="card downloader-card">
    <div class="header-actions">
      <h2 class="card-title">Téléchargements</h2>
      <button class="btn btn-sm btn-outline" @click="fetchJobs" :disabled="jobsLoading">
        🔄 Actualiser
      </button>
    </div>

    <!-- Zone de lancement -->
    <div class="input-zone">
      <form @submit.prevent="startDownload" class="download-bar">
        <select v-model="form.type" class="form-input type-select">
          <option value="track">Musique</option>
          <option value="album">Album</option>
          <option value="playlist">Playlist</option>
          <option value="episode">Podcast</option>
        </select>
        
        <input
          v-model="form.url"
          type="text"
          required
          placeholder="Collez votre lien Spotify ici..."
          class="form-input url-input"
        />
        
        <button class="btn btn-primary" type="submit" :disabled="loading">
          <span v-if="!loading">Télécharger</span>
          <span v-else>...</span>
        </button>
      </form>
      
      <div v-if="error" class="alert alert-error">{{ error }}</div>
      <div v-if="success" class="alert alert-success">{{ success }}</div>
    </div>

    <!-- Liste des Jobs -->
    <div class="jobs-container">
      <table class="jobs-table">
        <thead>
          <tr>
            <th>Nom / URL</th>
            <th>Type</th>
            <th>Statut</th>
            <th class="text-right">Progression</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="jobs.length === 0">
            <td colspan="4" class="empty-state">Aucun téléchargement récent</td>
          </tr>
          <tr v-for="job in jobs" :key="job.id">
            <td class="col-title" :title="job.url">
              {{ job.title || job.url }}
              <div class="date-sub">{{ formatDate(job.created_at) }}</div>
            </td>
            <td><span class="badge-type">{{ job.type }}</span></td>
            <td>
              <span class="status-indicator" :class="job.status">
                {{ translateStatus(job.status) }}
              </span>
            </td>
            <td class="text-right">
              <div class="progress-wrapper">
                <span class="progress-text">{{ job.progress }}%</span>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: job.progress + '%' }"></div>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const form = ref({
  url: '',
  type: 'track',
})

const loading = ref(false)
const error = ref('')
const success = ref('')
const jobs = ref([])
const jobsLoading = ref(false)

const getSettings = () => {
  const stored = localStorage.getItem('zotify-settings')
  if (stored) {
    try {
      return JSON.parse(stored)
    } catch {
      return {}
    }
  }
  return {}
}

const startDownload = async () => {
  error.value = ''
  success.value = ''
  loading.value = true

  const settings = getSettings() 
  
  const payload = {
    url: form.value.url,
    type: form.value.type || 'track', // Valeur par défaut si vide
    client_id: settings.client_id || '',
    output_dir: settings.output_dir || './downloads',
    quality: settings.quality || 'high',
    realtime: settings.realtime !== false,
    embed_metadata: settings.embed_metadata !== false,
    download_lyrics: settings.download_lyrics || false,
    bulk_wait_time: settings.bulk_wait_time || 30,
  }

  try {
    // Envoie ce payload unique
    const res = await axios.post(`${API_BASE}/download`, payload)
    success.value = res.data.message || 'Téléchargement démarré.'
    form.value.url = ''
    fetchJobs()
  } catch (e) {
    console.error(e) // Affiche l'erreur complète dans la console du navigateur
    error.value = e.response?.data?.detail || e.message || 'Erreur lors du lancement.'
  } finally {
    loading.value = false
  }
}


const fetchJobs = async () => {
  jobsLoading.value = true
  try {
    const res = await axios.get(`${API_BASE}/jobs`)
    jobs.value = res.data || []
  } catch (e) {
    console.error(e)
  } finally {
    jobsLoading.value = false
  }
}

const formatDate = (value) => {
  if (!value) return ''
  return new Date(value).toLocaleString('fr-FR')
}

onMounted(() => {
  fetchJobs()
})
</script>

<style scoped>
.downloader-card {
  display: flex;
  flex-direction: column;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.download-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.type-select {
  width: 140px;
  flex-shrink: 0;
}

.url-input {
  flex: 1;
}

.alert {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
.alert-error { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
.alert-success { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }

/* Table Styling */
.jobs-container {
  flex: 1;
  overflow: auto;
  border: 1px solid var(--border);
  border-radius: 8px;
}

.jobs-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.jobs-table th {
  background: #f8fafc;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--text-secondary);
  position: sticky;
  top: 0;
  border-bottom: 1px solid var(--border);
}

.jobs-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

.col-title {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 500;
}

.date-sub {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 2px;
}

.badge-type {
  background: #eff6ff;
  color: var(--accent);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  text-transform: capitalize;
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.status-indicator::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #cbd5e1;
}
.status-indicator.running::before { background: #3b82f6; } /* Bleu */
.status-indicator.done::before { background: #22c55e; }    /* Vert */
.status-indicator.error::before { background: #ef4444; }   /* Rouge */

.progress-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: flex-end;
}

.progress-bar {
  width: 100px;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--accent);
  transition: width 0.3s ease;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-secondary);
}
.btn-outline:hover {
  border-color: var(--accent);
  color: var(--accent);
}
</style>
