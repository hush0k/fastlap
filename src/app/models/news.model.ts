export type NewsTag = 'Breaking' | 'Rumor' | 'Official' | 'Analysis';

export interface NewsItem {
  id: string;
  title: string;
  summary: string;
  content: string;
  publishedAt: string;
  posterUrl: string;
  author: string;
  tag?: NewsTag;
}

export const NEWS_DATA: NewsItem[] = [
  {
    id: 'n1',
    title: 'Pre-season testing insights',
    summary: 'Long runs reveal surprising tire degradation patterns.',
    content:
      'Detailed technical breakdown of fuel loads, tire wear and aero efficiency observed during testing...',
    publishedAt: '2026-02-20T10:00:00Z',
    posterUrl: '/news/poster1.jpg',
    author: 'FastLap Editorial',
    tag: 'Analysis',
  },
  {
    id: 'n2',
    title: 'New aero upgrades introduced',
    summary: 'Teams debut updated front wings ahead of race weekend.',
    content:
      'Several teams introduced updated front wing geometries aimed at increasing front-end stability...',
    publishedAt: '2026-02-18T14:30:00Z',
    posterUrl: '/news/poster2.jpg',
    author: 'FastLap Editorial',
    tag: 'Official',
  },
];
