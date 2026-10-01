export const taskBoardPage = {
  heading(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('heading', { name: /tareas académicas/i });
  },

  titleInput(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByLabelText(/título de la tarea/i);
  },

  submit(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('button', { name: /agregar tarea|agregando/i });
  },

  list(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('list', { name: /lista de tareas/i });
  },

  item(title: string): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('checkbox', { name: title });
  },

  alert(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('alert');
  },

  emptyState(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('status');
  },

  create(title: string): void {
    this.titleInput().clear().type(title);
    this.submit().click();
  },

  assertVisible(title: string): void {
    this.item(title).should('be.visible').and('not.be.checked');
    this.list().should('contain.text', title);
    this.titleInput().should('have.value', '');
  },
};
