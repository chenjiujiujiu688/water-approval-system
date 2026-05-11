import os from "node:os";
import path from "node:path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  cacheDir: path.join(os.tmpdir(), "water-approval-vite-cache"),
  server: {
    host: "0.0.0.0",
    port: 5173
  }
});
