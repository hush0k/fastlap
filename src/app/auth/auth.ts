import { Component, OnInit, Inject, PLATFORM_ID, ChangeDetectorRef } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';

import { AuthService } from '../services/auth.service';

interface ValidationErrors {
  [key: string]: string;
}

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './auth.html',
  styleUrls: ['./auth.css'],
})
export class Auth implements OnInit {
  isSignupMode = false;
  loading = false;

  email = '';
  password = '';
  username = '';
  full_name = '';
  password2 = '';

  selectedAvatar: File | null = null;
  avatarPreview: string | null = null;

  validationErrors: ValidationErrors = {};

  loginErrorMessage = '';
  registerErrorMessage = '';

  private returnUrl = '/';

  constructor(
    private readonly authService: AuthService,
    private readonly router: Router,
    private readonly route: ActivatedRoute,
    private readonly cdr: ChangeDetectorRef,
    @Inject(PLATFORM_ID) private readonly platformId: Object,
  ) {}

  ngOnInit(): void {
    this.returnUrl = this.route.snapshot.queryParamMap.get('returnUrl') || '/';

    if (this.authService.isAuthenticated()) {
      this.router.navigateByUrl(this.returnUrl);
      return;
    }

    if (isPlatformBrowser(this.platformId)) {
      this.createParticles();
    }
  }

  toggleMode(): void {
    this.isSignupMode = !this.isSignupMode;
    this.validationErrors = {};
    this.loginErrorMessage = '';
    this.registerErrorMessage = '';
    this.resetForms();
  }

  clearLoginFieldError(field: string): void {
    delete this.validationErrors[field];
    this.loginErrorMessage = '';
  }

  clearRegisterFieldError(field: string): void {
    delete this.validationErrors[field];
    this.registerErrorMessage = '';
  }

  private resetForms(): void {
    this.email = '';
    this.password = '';
    this.username = '';
    this.full_name = '';
    this.password2 = '';
    this.selectedAvatar = null;
    this.avatarPreview = null;
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  private validatePassword(password: string): string | null {
    if (password.length < 8) return 'Password must be at least 8 characters';
    if (!/[A-Za-z]/.test(password)) return 'Password must contain a letter';
    if (!/\d/.test(password)) return 'Password must contain a number';
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      return 'Password must contain a special character';
    }
    return null;
  }

  private validateLoginForm(): boolean {
    this.validationErrors = {};
    this.loginErrorMessage = '';

    if (!this.email) {
      this.validationErrors['email'] = 'Email is required';
    } else if (!this.isValidEmail(this.email)) {
      this.validationErrors['email'] = 'Invalid email address';
    }

    if (!this.password) {
      this.validationErrors['password'] = 'Password is required';
    }

    return Object.keys(this.validationErrors).length === 0;
  }

  private validateRegisterForm(): boolean {
    this.validationErrors = {};
    this.registerErrorMessage = '';

    if (!this.email) {
      this.validationErrors['email'] = 'Email is required';
    } else if (!this.isValidEmail(this.email)) {
      this.validationErrors['email'] = 'Invalid email address';
    }

    if (!this.username || this.username.length < 3) {
      this.validationErrors['username'] = 'Username must be at least 3 characters';
    }

    const nameParts = this.full_name.trim().split(' ');
    if (!nameParts[0]) {
      this.validationErrors['full_name'] = 'Please enter your full name';
    }

    const passwordError = this.validatePassword(this.password);
    if (passwordError) {
      this.validationErrors['password'] = passwordError;
    }

    if (this.password !== this.password2) {
      this.validationErrors['password2'] = 'Passwords do not match';
    }

    if (!this.selectedAvatar) {
      this.validationErrors['avatar'] = 'Avatar is required';
    }

    return Object.keys(this.validationErrors).length === 0;
  }

  private parseFullName(): { first_name: string; last_name: string } {
    const parts = this.full_name.trim().split(' ');
    return {
      first_name: parts[0] ?? '',
      last_name: parts.slice(1).join(' ') ?? '',
    };
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    delete this.validationErrors['avatar'];

    if (!file) return;

    if (file.size > 2 * 1024 * 1024) {
      this.validationErrors['avatar'] = 'Avatar must be under 2MB';
      return;
    }

    if (!file.type.startsWith('image/')) {
      this.validationErrors['avatar'] = 'Avatar must be an image';
      return;
    }

    this.selectedAvatar = file;

    const reader = new FileReader();
    reader.onload = () => {
      this.avatarPreview = reader.result as string;
    };
    reader.readAsDataURL(file);
  }

  onSubmit(): void {
    if (!this.validateLoginForm()) return;

    this.loading = true;
    this.loginErrorMessage = '';

    this.authService.login(this.email, this.password).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigateByUrl(this.returnUrl);
      },
      error: (error) => {
        this.loading = false;
        this.loginErrorMessage = error?.message || 'Login failed. Please try again.';
      },
    });
  }

  onRegister(): void {
    if (!this.validateRegisterForm()) return;

    this.loading = true;
    this.registerErrorMessage = '';

    const { first_name, last_name } = this.parseFullName();

    const userData = {
      email: this.email,
      username: this.username,
      password: this.password,
      first_name,
      last_name,
    };

    this.authService.register(userData, this.selectedAvatar!).subscribe({
      next: () => {
        this.loading = false;

        const registeredEmail = this.email;

        this.validationErrors = {};
        this.registerErrorMessage = '';
        this.resetForms();

        alert('Account created successfully. Please sign in.');

        setTimeout(() => {
          this.email = registeredEmail;
          this.isSignupMode = false;
          this.cdr.detectChanges();
        }, 0);
      },
      error: (error) => {
        this.loading = false;
        this.registerErrorMessage = error?.message || 'Registration failed. Please try again.';

        if (error?.fieldErrors) {
          this.validationErrors = {
            ...this.validationErrors,
            ...error.fieldErrors,
          };
        }
      },
    });
  }

  private createParticles(): void {
    const container = document.getElementById('particles');
    if (!container) return;

    for (let i = 0; i < 50; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = Math.random() * 100 + '%';
      particle.style.animationDelay = Math.random() * 5 + 's';
      particle.style.animationDuration = 8 + Math.random() * 7 + 's';
      container.appendChild(particle);
    }
  }

  get passwordChecks() {
    return {
      length: this.password.length >= 8,
      letter: /[A-Za-z]/.test(this.password),
      number: /\d/.test(this.password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(this.password),
    };
  }
}
