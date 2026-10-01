import { defineConfig } from 'cypress';
import { profiles } from './cypress/config/environments';

const profileName = process.env.CYPRESS_profile ?? 'local';
const profile = profiles[profileName] ?? profiles.local;

const baseUrl = process.env.CYPRESS_BASE_URL ?? process.env.CYPRESS_baseUrl ?? profile.baseUrl;
const apiUrl = process.env.CYPRESS_apiUrl ?? profile.apiUrl;

export default defineConfig({
  e2e: {
    baseUrl,
    specPattern: 'cypress/e2e/**/*.cy.ts',
    supportFile: 'cypress/support/e2e.ts',
    fixturesFolder: 'cypress/fixtures',
    screenshotsFolder: 'cypress/screenshots',
    videosFolder: 'cypress/videos',
    viewportWidth: 1440,
    viewportHeight: 900,
    defaultCommandTimeout: 8000,
    requestTimeout: 10000,
    responseTimeout: 20000,
    pageLoadTimeout: 15000,
    retries: {
      runMode: 2,
      openMode: 0,
    },
    video: false,
    screenshotOnRunFailure: true,
    chromeWebSecurity: false,
    env: {
      profile: profiles[profileName] ? profileName : 'local',
      apiUrl,
      baseUrl,
      maxResponseMs: Number(process.env.CYPRESS_maxResponseMs ?? profile.maxResponseMs),
      slowBackendMs: Number(process.env.CYPRESS_slowBackendMs ?? 1800),
      timeoutBackendMs: Number(process.env.CYPRESS_timeoutBackendMs ?? 2500),
      authTokenKey: 'universidad.session.token',
      authUserKey: 'universidad.session.user',
    },
    setupNodeEvents(_on, config) {
      const selectedName = String(config.env.profile ?? profileName);
      const selected = profiles[selectedName] ?? profiles.local;
      const envBaseUrl = typeof config.env.baseUrl === 'string' ? config.env.baseUrl : undefined;
      const envApiUrl = typeof config.env.apiUrl === 'string' ? config.env.apiUrl : undefined;

      config.baseUrl = process.env.CYPRESS_BASE_URL ?? process.env.CYPRESS_baseUrl ?? envBaseUrl ?? selected.baseUrl;
      config.env.profile = profiles[selectedName] ? selectedName : 'local';
      config.env.apiUrl = process.env.CYPRESS_apiUrl ?? envApiUrl ?? selected.apiUrl;
      config.env.baseUrl = config.baseUrl;
      config.env.maxResponseMs = Number(config.env.maxResponseMs ?? selected.maxResponseMs);
      return config;
    },
  },
});
