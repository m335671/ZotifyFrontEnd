<template>
  <div class="card settings-card">
    <h3 class="section-title">{{ t('settings_title') }}</h3>
    
    <div class="scroll-area">
      <div class="form-group">
        <label>{{ t('client_id') }}</label>
        <input 
          v-model="settings.client_id" 
          type="text" 
          placeholder="Your Client ID" 
          class="form-input"
        />
        <small class="hint">{{ t('client_id_hint') }}</small>
      </div>

      <div class="form-group">
        <label>{{ t('output_dir') }}</label>
        <input 
          v-model="settings.output_dir" 
          type="text" 
          placeholder="./downloads" 
          class="form-input"
        />
      </div>

      <div class="form-group">
        <label>{{ t('quality') }}</label>
        <select v-model="settings.quality" class="form-input">
          <option value="very_high">{{ t('q_very_high') }}</option>
          <option value="high">{{ t('q_high') }}</option>
          <option value="medium">{{ t('q_medium') }}</option>
          <option value="low">{{ t('q_low') }}</option>
        </select>
      </div>

      <div class="toggles-wrapper">
        <label class="toggle-row">
          <span>{{ t('realtime_mode') }}</span>
          <input type="checkbox" v-model="settings.realtime" class="toggle-switch" />
        </label>
        <label class="toggle-row">
          <span>{{ t('metadata') }}</span>
          <input type="checkbox" v-model="settings.embed_metadata" class="toggle-switch" />
        </label>
        <label class="toggle-row">
          <span>{{ t('lyrics') }}</span>
          <input type="checkbox" v-model="settings.download_lyrics" class="toggle-switch" />
        </label>
      </div>
      
      <div class="form-group">
        <label>{{ t('wait_time') }}</label>
        <input 
          v-model.number="settings.bulk_wait_time" 
          type="number" 
          min="5" 
          class="form-input input-short" 
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

const props = defineProps(['lang', 't']) // Reçoit les props de App.vue
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
    try { Object.assign(settings.value, JSON.parse(stored)) } catch (e) {}
  }
}

const saveSettings = () => {
  try {
    localStorage.setItem('zotify-settings', JSON.stringify(settings.value))
    saved.value = true
    status.value = props.t('save_auto')
    setTimeout(() => status.value = '', 2000)
  } catch (e) {
    saved.value = false
    status.value = props.t('save_error')
  }
}

onMounted(loadSettings)
watch(settings, saveSettings, { deep: true })
</script>

<style scoped>
.settings-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.section-title {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.scroll-area {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 0.5rem;
}

.form-group { margin-bottom: 1.2rem; }
.form-group label { display: block; font-weight: 500; margin-bottom: 0.4rem; font-size: 0.9rem; }
.hint { display: block; margin-top: 0.2rem; color: var(--text-secondary); font-size: 0.75rem; }

.toggles-wrapper {
  background: var(--bg-app); 
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.2rem;
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

.status-bar { margin-top: auto; height: 24px; text-align: center; }
.status-pill { font-size: 0.8rem; padding: 2px 10px; border-radius: 12px; background: var(--border); }
.status-pill.success { background: #dcfce7; color: #166534; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>