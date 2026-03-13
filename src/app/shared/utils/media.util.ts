import { environment } from '../../../environments/environment';

export function resolveMediaUrl(path: string | null | undefined): string {
  if (!path) {
    return 'placeholders/image-placeholder.png';
  }

  if (path.startsWith('http')) {
    return path;
  }

  return `${environment.mediaUrl}${path}`;
}
