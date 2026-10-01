/// <reference types="vitest/config" />
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath, URL } from 'node:url';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      port: 3000,
      strictPort: true,
    },
    build: {
      sourcemap: env.NODE_ENV !== 'production',
    },
    esbuild: {
      drop: mode === 'production' ? ['console', 'debugger'] : [],
    },
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: ['./src/tests/setup/vitest.setup.ts'],
      css: true,
      include: ['src/tests/**/*.test.{ts,tsx}'],
      pool: 'threads',
      maxWorkers: 1,
      fileParallelism: false,
      isolate: false,
      coverage: {
        provider: 'v8',
        reporter: ['text', 'html'],
        include: [
          'src/components/TaskForm.tsx',
          'src/components/TaskList.tsx',
          'src/components/TaskBoard.tsx',
          'src/services/taskService.ts',
          'src/utils/validators.ts',
        ],
      },
    },
  };
});
