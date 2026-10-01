export const dashboardPage = {
  heading(name: string | RegExp): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('heading', { name });
  },

  userCard(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.get('.user-card');
  },

  logout(): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('button', { name: /cerrar sesión/i });
  },

  navItem(label: string | RegExp): Cypress.Chainable<JQuery<HTMLElement>> {
    return cy.findByRole('link', { name: label });
  },

  assertAuthenticated(heading: string | RegExp, fullName?: string): void {
    this.heading(heading).should('be.visible');
    cy.findByRole('button', { name: /cerrar sesión/i }).should('be.visible');
    if (fullName) {
      this.userCard().should('contain.text', fullName);
    }
  },
};
