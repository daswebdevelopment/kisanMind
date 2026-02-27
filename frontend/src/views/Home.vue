<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'

const message = ref('Checking API status...')
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

onMounted(async () => {
  try {
    const response = await axios.get(`${apiUrl}/health`)
    message.value = response.data?.status === 'ok'
      ? 'KisanMind API is running'
      : 'KisanMind API health check failed'
  } catch {
    message.value = 'Unable to connect to KisanMind API'
  }
})
</script>

<template>
  <section>
    <h2>Home</h2>
    <p>{{ message }}</p>
  </section>
</template>
