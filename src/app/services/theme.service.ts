import { Injectable, Renderer2, RendererFactory2 } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { STORAGE_KEYS } from '../core/config/app.constants';

export type Theme = 'light' | 'dark';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
  private readonly renderer: Renderer2;
  private readonly themeSubject = new BehaviorSubject<Theme>('dark');

  readonly theme$ = this.themeSubject.asObservable();

  constructor(rendererFactory: RendererFactory2) {
    this.renderer = rendererFactory.createRenderer(null, null);
    this.initializeTheme();
  }

  getCurrentTheme(): Theme {
    return this.themeSubject.value;
  }

  toggleTheme(): void {
    this.setTheme(this.themeSubject.value === 'dark' ? 'light' : 'dark');
  }

  setTheme(theme: Theme): void {
    this.renderer.removeClass(document.body, 'light-theme');
    this.renderer.removeClass(document.body, 'dark-theme');
    this.renderer.addClass(document.body, `${theme}-theme`);

    localStorage.setItem(STORAGE_KEYS.THEME, theme);
    this.themeSubject.next(theme);
  }

  private initializeTheme(): void {
    const savedTheme = localStorage.getItem(STORAGE_KEYS.THEME) as Theme | null;

    if (savedTheme === 'light' || savedTheme === 'dark') {
      this.setTheme(savedTheme);
      return;
    }

    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    this.setTheme(prefersDark ? 'dark' : 'light');

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (event) => {
      const manuallySavedTheme = localStorage.getItem(STORAGE_KEYS.THEME);
      if (!manuallySavedTheme) {
        this.setTheme(event.matches ? 'dark' : 'light');
      }
    });
  }
}
