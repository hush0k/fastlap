export interface NewsTag {
  id: number;
  name: string;
  slug: string;
}

export interface ArticleAuthor {
  id: number;
  username: string;
  first_name?: string;
  last_name?: string;
}

export interface ArticleListItem {
  id: number;
  name: string;
  slug: string;
  author: ArticleAuthor;
  cover_image: string | null;
  tags: NewsTag[];
  series: { id: number; name: string }[];
  published_at: string | null;
  is_published: boolean;
  views_count: number;
  content: string;
}

export interface ArticleDetail {
  id: number;
  name: string;
  slug: string;
  author: ArticleAuthor;
  content: string;
  cover_image: string | null;
  tags: NewsTag[];
  series: { id: number; name: string }[];
  published_at: string | null;
  is_published: boolean;
  views_count: number;
}

export interface ArticleQueryParams {
  limit?: number;
  offset?: number;
}
