export function formatShortDate(value: string | Date): string {
  const date = new Date(value);

  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
  });
}
