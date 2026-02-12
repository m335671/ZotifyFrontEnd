<template>
  <div class="card downloader-card">
    <div class="header-actions">
      <h2 class="card-title">{{ t('downloads_title') }}</h2>
      <button class="btn btn-sm btn-outline" @click="fetchJobs" :disabled="jobsLoading">
        <!-- Icone Refresh SVG -->
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16l5 5v-5"/></svg>
        {{ t('refresh') }}
      </button>
    </div>

    <!-- Zone de lancement -->
    <div class="input-zone">
      <form @submit.prevent="startDownload" class="download-bar">
        <select v-model="form.type" class="form-input type-select">
          <option value="track">{{ t('type_track') }}</option>
          <option value="album">{{ t('type_album') }}</option>
          <option value="playlist">{{ t('type_playlist') }}</option>
          <option value="episode">{{ t('type_podcast') }}</option>
        </select>
        
        <input
          v-model="form.url"
          type="text"
          required
          :placeholder="t('placeholder_url')"
          class="form-input url-input"
        />
        
        <button class="btn btn-primary" type="submit" :disabled="loading">
          <span v-if="!loading">{{ t('btn_download') }}</span>
          <span v-else>{{ t('btn_launching') }}</span>
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
            <th>{{ t('col_name') }}</th>
            <th>{{ t('col_type') }}</th>
            <th>{{ t('col_status') }}</th>
            <th class="text-right">{{ t('col_progress') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="jobs.length === 0">
            <td colspan="4" class="empty-state">{{ t('empty_state') }}</td>
          </tr>
          <tr v-for="job in jobs" :key="job.id">
            <td class="col-title" :title="job.url">
              {{ job.title || job.url }}
              <div class="date-sub">{{ formatDate(job.created_at) }}</div>
            </td>
            <td><span class="badge-type">{{ translateType(job.type) }}</span></td>
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

const props = defineProps(['lang', 't'])

// Ajoute ces clés dans ton translations.js si elles manquent :
// col_name: "Name / URL", col_type: "Type", col_status: "Status", col_progress: "Progress"
// col_name: "Nom / URL", col_type: "Type", col_status: "Statut", col_progress: "Progression"

const translateStatus = (status) => {
  const map = {
    running: props.t('status_running'),
    done: props.t('status_done'),
    error: props.t('status_error'),
    pending: props.t('status_pending')
  }
  return map[status] || status
}

const translateType = (type) => {
    const map = {
        track: props.t('type_track'),
        album: props.t('type_album'),
        playlist: props.t('type_playlist'),
        episode: props.t('type_podcast')
    }
    return map[type] || type
}

const formatDate = (dateStr) => {
    if(!dateStr) return ''
    return new Date(dateStr).toLocaleString(props.lang)
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:1337'
const form = ref({ url: '', type: 'track' })
const loading = ref(false)
const error = ref('')
const success = ref('')
const jobs = ref([])
const jobsLoading = ref(false)

const getSettings = () => {
  const stored = localStorage.getItem('zotify-settings')
  if (stored) {
    try { return JSON.parse(stored) } catch { return {} }
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
    type: form.value.type || 'track',
    client_id: settings.client_id || '',
    output_dir: settings.output_dir || './downloads',
    quality: settings.quality || 'high',
    realtime: settings.realtime !== false,
    embed_metadata: settings.embed_metadata !== false,
    download_lyrics: settings.download_lyrics || false,
    bulk_wait_time: settings.bulk_wait_time || 30,
  }

  try {
    const res = await axios.post(`${API_BASE}/download`, payload)
    success.value = res.data.message || 'Started.'
    form.value.url = ''
    fetchJobs()
  } catch (e) {
    console.error(e)
    error.value = e.response?.data?.detail || e.message || 'Error launching download.'
  } finally {
    loading.value = false
  }
}

const fetchJobs = async () => {
    jobsLoading.value = true
    try {
        const res = await axios.get(`${API_BASE}/jobs`)
        jobs.value = res.data.reverse()
    } catch (e) {
        console.error(e)
    } finally {
        jobsLoading.value = false
    }
}

onMounted(() => {
    fetchJobs()
    setInterval(fetchJobs, 5000) // Auto refresh
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
  margin-bottom: 1.5rem;
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
  background: var(--bg-card); /* Fond correct */
}

.jobs-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

/* FIX: Utiliser var(--bg-app) ou var(--bg-card) pour le header */
.jobs-table th {
  background: var(--bg-app); /* S'adapte au thème sombre/clair */
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--text-secondary);
  position: sticky;
  top: 0;
  border-bottom: 1px solid var(--border);
  z-index: 10; /* Reste au dessus */
}

.jobs-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
  color: var(--text-primary); /* Texte lisible en dark mode */
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
  background: rgba(37, 99, 235, 0.1); /* Transparent blue */
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
.status-indicator.running::before { background: #3b82f6; } 
.status-indicator.done::before { background: #22c55e; }    
.status-indicator.error::before { background: #ef4444; }   

.progress-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: flex-end;
}

.progress-bar {
  width: 100px;
  height: 6px;
  background: var(--border);
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

@media (max-width: 768px) {
    .download-bar {
        flex-direction: column;
    }
    .type-select, .url-input, .btn-primary {
        width: 100%;
    }
}
</style>