export const loginPage = {
  visit(): Cypress.Chainable<unknown> {
    return cy.visit('/login');
  },

  title(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('heading', { name: /iniciar sesión/i });
  },

  email(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByLabelText(/correo electrónico/i);
  },

  password(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByLabelText(/contraseña/i);
  },

  submit(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('button', { name: /ingresar|ingresando/i });
  },

  alert(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('alert');
  },

  fill(email: string, password: string): void {
    this.email().clear().type(email);
    this.password().clear().type(password, { log: false });
  },

  submitForm(): void {
    this.submit().click();
  },

  login(email: string, password: string): void {
    this.visit();
    this.title().should('be.visible');
    this.fill(email, password);
    this.submitForm();
  },
};
