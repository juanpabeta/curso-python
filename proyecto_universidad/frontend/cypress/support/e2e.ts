/// <reference path="./index.d.ts" />

import '@testing-library/cypress/add-commands';
import './commands';
import { registerGlobalHooks } from './hooks';

registerGlobalHooks();

Cypress.on('uncaught:exception', (error) => {
  if (/Network Error|Failed to fetch|Load failed/i.test(error.message)) {
    return false;
  }

  return true;
});
