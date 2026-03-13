import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavigationEnd, Router, RouterLink, RouterLinkActive } from '@angular/router';
import { filter, Subscription } from 'rxjs';

import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {
  faBars,
  faFlag,
  faGear,
  faHelmetSafety,
  faMoon,
  faNewspaper,
  faSignOutAlt,
  faSun,
  faTrophy,
  faTimes,
  faUser,
} from '@fortawesome/free-solid-svg-icons';

import { AuthService } from '../services/auth.service';
import { Theme, ThemeService } from '../services/theme.service';

type UserData = {
  first_name?: string;
  last_name?: string;
  email?: string;
} | null;

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive, FontAwesomeModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar implements OnInit, OnDestroy {
  currentTheme: Theme = 'dark';

  isAuthenticated = false;
  isMobileMenuOpen = false;
  isUserDropdownOpen = false;
  userData: UserData = null;

  faSun = faSun;
  faMoon = faMoon;
  faBars = faBars;
  faTimes = faTimes;
  faFlag = faFlag;
  faHelmetSafety = faHelmetSafety;
  faNewspaper = faNewspaper;
  faTrophy = faTrophy;
  faUser = faUser;
  faGear = faGear;
  faSignOutAlt = faSignOutAlt;

  private readonly subscriptions = new Subscription();

  constructor(
    private readonly themeService: ThemeService,
    private readonly authService: AuthService,
    private readonly router: Router,
  ) {
    this.currentTheme = this.themeService.getCurrentTheme();
  }

  ngOnInit(): void {
    this.subscriptions.add(
      this.themeService.theme$.subscribe((theme) => {
        this.currentTheme = theme;
      }),
    );

    this.subscriptions.add(
      this.authService.isAuthenticated$.subscribe((isAuth) => {
        this.isAuthenticated = isAuth;
        this.userData = isAuth ? this.authService.getUserData() : null;

        if (!isAuth) {
          this.isUserDropdownOpen = false;
        }
      }),
    );

    this.subscriptions.add(
      this.router.events
        .pipe(filter((event) => event instanceof NavigationEnd))
        .subscribe(() => this.closeAllMenus()),
    );
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  toggleTheme(): void {
    this.themeService.toggleTheme();
  }

  toggleMobileMenu(): void {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;

    if (this.isMobileMenuOpen) {
      this.isUserDropdownOpen = false;
    }
  }

  toggleUserMenu(): void {
    this.isUserDropdownOpen = !this.isUserDropdownOpen;

    if (this.isUserDropdownOpen) {
      this.isMobileMenuOpen = false;
    }
  }

  closeMobileMenu(): void {
    this.isMobileMenuOpen = false;
  }

  closeAllMenus(): void {
    this.isMobileMenuOpen = false;
    this.isUserDropdownOpen = false;
  }

  logout(): void {
    this.authService.logout();
    this.closeAllMenus();
  }

  get themeIcon() {
    return this.currentTheme === 'dark' ? this.faSun : this.faMoon;
  }

  get themeText(): string {
    return this.currentTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
  }

  get userInitials(): string {
    if (this.userData?.first_name && this.userData?.last_name) {
      return `${this.userData.first_name[0]}${this.userData.last_name[0]}`.toUpperCase();
    }

    if (this.userData?.email) {
      return this.userData.email[0].toUpperCase();
    }

    return 'U';
  }
}
