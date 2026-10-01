import { Component, type ReactNode } from 'react';
import { ServerErrorPage } from '@/pages/ServerErrorPage';

interface ErrorBoundaryState {
  hasError: boolean;
}

export class ErrorBoundary extends Component<{ children: ReactNode }, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true };
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return (
        <main className="auth-shell">
          <div className="auth-panel">
            <ServerErrorPage onRetry={() => window.location.reload()} />
          </div>
        </main>
      );
    }

    return this.props.children;
  }
};
