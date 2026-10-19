import {defineConfig} from '@playwright/test';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../../',import.meta.url));
export default defineConfig({testDir:'.',testMatch:'*.spec.mjs',timeout:30000,workers:1,
  use:{baseURL:'http://127.0.0.1:8765',headless:true},
  webServer:{command:'python3 -m scripts.chengdu_slides.testing && python3 -m scripts.chengdu_slides.cli preview && python3 -m http.server 8765 --bind 127.0.0.1',cwd:root,
    url:'http://127.0.0.1:8765',reuseExistingServer:false,timeout:15000}});
