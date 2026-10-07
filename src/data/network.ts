import type { ImageMetadata } from 'astro';

export type ProfessionalType = 'wedding-planner' | 'location';

export type RegionKey = 'toscana' | 'centro-italia' | 'nord-italia' | 'sud-italia-isole';

export interface Professional {
  id: string;
  slug: string;
  type: ProfessionalType;
  region: RegionKey;
  area: { it: string; en: string };
  name: string;
  description: { it: string; en: string };
  image?: ImageMetadata;
  imageAlt?: { it: string; en: string };
  instagram?: string;
  website?: string;
  featured?: boolean;
}

export const regionLabels: Record<RegionKey, { it: string; en: string }> = {
  'toscana':            { it: 'Toscana',             en: 'Tuscany'                  },
  'centro-italia':      { it: 'Centro Italia',        en: 'Central Italy'            },
  'nord-italia':        { it: 'Nord Italia',          en: 'Northern Italy'           },
  'sud-italia-isole':   { it: 'Sud Italia e Isole',  en: 'Southern Italy & Islands' },
};

export const typeLabels: Record<ProfessionalType, { it: string; en: string }> = {
  'wedding-planner': { it: 'Wedding Planner', en: 'Wedding Planner' },
  'location':        { it: 'Location',        en: 'Venue'           },
};

export const professionals: Professional[] = [];

export function professionalsOfType(type: ProfessionalType): Professional[] {
  return professionals.filter(p => p.type === type);
}

export function byRegion(type: ProfessionalType): Array<{ region: RegionKey; items: Professional[] }> {
  const order: RegionKey[] = ['toscana', 'centro-italia', 'nord-italia', 'sud-italia-isole'];
  return order
    .map(region => ({ region, items: professionals.filter(p => p.type === type && p.region === region) }))
    .filter(g => g.items.length > 0);
}
