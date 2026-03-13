import { Routes } from '@angular/router';

import { HomePage } from './home-page/home-page';
import { Teams } from './teams/teams';
import { Drivers } from './drivers/drivers';
import { News } from './news/news';
import { Tournaments } from './tournaments/tournaments';
import { Auth } from './auth/auth';
import { PublicGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    component: HomePage,
    title: 'FastLap F1 - Home',
  },
  {
    path: 'teams',
    component: Teams,
    title: 'Teams - FastLap F1',
  },
  {
    path: 'drivers',
    component: Drivers,
    title: 'Drivers - FastLap F1',
  },
  {
    path: 'news',
    component: News,
    title: 'News - FastLap F1',
  },
  {
    path: 'tournaments',
    component: Tournaments,
    title: 'Tournaments - FastLap F1',
  },
  {
    path: 'auth',
    component: Auth,
    canActivate: [PublicGuard],
    title: 'Sign In - FastLap F1',
  },
  {
    path: '**',
    redirectTo: '',
  },
];
