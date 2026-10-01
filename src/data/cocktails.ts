import type { ImageMetadata } from 'astro';
import type { Localized } from '@/i18n/ui';

/**
 * COCKTAIL LIST — data-driven.
 * Source: brochure "La nostra cocktail list — I classici". Profiles and alcohol
 * levels (1–5) are taken from the brochure. No recipes are published.
 *
 * To add a cocktail: drop a photo in src/assets/images/cocktails/<slug>.jpg
 * (4:3 recommended) and append an entry. The image is matched by slug automatically.
 */
export type CocktailCategory = 'classics' | 'signature' | 'spritz' | 'martini' | 'sour' | 'tropical' | 'aperitivo';

export const cocktailCategories: { id: CocktailCategory; label: Localized; blurb: Localized }[] = [
  {
    id: 'classics',
    label: { it: 'Classici', en: 'Classics' },
    blurb: { it: 'Le grandi ricette di sempre, eseguite con metodo.', en: 'The great recipes, executed with method.' },
  },
  {
    id: 'signature',
    label: { it: 'Signature', en: 'Signatures' },
    blurb: {
      it: 'Drink creati e nominati sulla vostra storia o sull’identità del brand.',
      en: 'Drinks created and named after your story or your brand identity.',
    },
  },
  {
    id: 'spritz',
    label: { it: 'Spritz', en: 'Spritz' },
    blurb: { it: 'Aperol, Campari, Hugo, Limoncello, Passion Fruit.', en: 'Aperol, Campari, Hugo, Limoncello, Passion Fruit.' },
  },
  {
    id: 'martini',
    label: { it: 'Martini', en: 'Martini' },
    blurb: { it: 'Coppe fredde, linee pulite.', en: 'Chilled coupes, clean lines.' },
  },
  {
    id: 'sour',
    label: { it: 'Sour', en: 'Sour' },
    blurb: { it: 'Equilibrio tra agrume, dolcezza e struttura.', en: 'Balance between citrus, sweetness and structure.' },
  },
  {
    id: 'tropical',
    label: { it: 'Tropical', en: 'Tropical' },
    blurb: { it: 'Freschi, dinamici, da festa.', en: 'Fresh, lively, made for the party.' },
  },
  {
    id: 'aperitivo',
    label: { it: 'Aperitivo italiano', en: 'Italian aperitivo' },
    blurb: { it: 'Il rito italiano, dal Negroni al Bellini.', en: 'The Italian ritual, from Negroni to Bellini.' },
  },
];

export interface Cocktail {
  slug: string;
  name: string;
  categories: CocktailCategory[];
  profile: Localized;
  /** 1–5, as printed in the brochure */
  alcohol: 1 | 2 | 3 | 4 | 5;
  variants?: string;
  image?: ImageMetadata;
  /** Show in the curated homepage/teaser gallery */
  featured?: boolean;
}

const images = import.meta.glob<{ default: ImageMetadata }>('/src/assets/images/cocktails/*.{jpg,jpeg,png,webp,avif}', {
  eager: true,
});
function img(slug: string): ImageMetadata | undefined {
  const key = Object.keys(images).find((k) => k.split('/').pop()?.replace(/\.\w+$/, '') === slug);
  return key ? images[key].default : undefined;
}

const P = (it: string, en: string): Localized => ({ it, en });

const list: Omit<Cocktail, 'image'>[] = [
  { slug: 'spritz', name: 'Spritz', categories: ['spritz', 'aperitivo'], profile: P('Fresco, agrumato', 'Fresh, citrusy'), alcohol: 2, variants: 'Aperol · Campari · Hugo · Limoncello', featured: true },
  { slug: 'negroni', name: 'Negroni', categories: ['aperitivo', 'classics'], profile: P('Intenso, strutturato', 'Intense, structured'), alcohol: 5, featured: true },
  { slug: 'espresso-martini', name: 'Espresso Martini', categories: ['martini'], profile: P('Intenso, morbido', 'Intense, smooth'), alcohol: 4, featured: true },
  { slug: 'pornstar-martini', name: 'Pornstar Martini', categories: ['martini'], profile: P('Fruttato, dolce', 'Fruity, sweet'), alcohol: 3, featured: true },
  { slug: 'dry-martini', name: 'Cocktail Martini (Dry)', categories: ['martini', 'classics'], profile: P('Secco, intenso', 'Dry, intense'), alcohol: 5 },
  { slug: 'margarita', name: 'Margarita / Tommy’s', categories: ['sour'], profile: P('Secco, intenso', 'Dry, intense'), alcohol: 4, featured: true },
  { slug: 'sour', name: 'Whiskey · Vodka · Gin · Tequila Sour', categories: ['sour'], profile: P('Agrumato', 'Citrusy'), alcohol: 4, featured: true },
  { slug: 'daiquiri', name: 'Daiquiri', categories: ['sour', 'tropical'], profile: P('Fresco, bilanciato', 'Fresh, balanced'), alcohol: 4, variants: 'Classic · Strawberry · Passion · Mango' },
  { slug: 'cosmopolitan', name: 'Cosmopolitan', categories: ['martini', 'sour'], profile: P('Agrumato, fruttato', 'Citrusy, fruity'), alcohol: 3 },
  { slug: 'gin-fizz', name: 'Gin Fizz', categories: ['sour', 'classics'], profile: P('Fresco, agrumato', 'Fresh, citrusy'), alcohol: 3 },
  { slug: 'mojito', name: 'Mojito', categories: ['tropical'], profile: P('Fresco, agrumato, mentolato', 'Fresh, citrusy, minty'), alcohol: 2, variants: 'Classic · Passion · Fragola · Mango', featured: true },
  { slug: 'caipirinha', name: 'Caipirinha', categories: ['tropical'], profile: P('Fresco, intenso', 'Fresh, intense'), alcohol: 4, variants: 'Caipiroska · Caipirissima · Caipirita' },
  { slug: 'pina-colada', name: 'Piña Colada', categories: ['tropical'], profile: P('Dolce, tropicale', 'Sweet, tropical'), alcohol: 3 },
  { slug: 'paloma', name: 'Paloma', categories: ['tropical'], profile: P('Fresco, agrumato', 'Fresh, citrusy'), alcohol: 3 },
  { slug: 'cuba-libre', name: 'Cuba Libre', categories: ['tropical', 'classics'], profile: P('Fresco, dissetante', 'Fresh, thirst-quenching'), alcohol: 3 },
  { slug: 'americano', name: 'Americano', categories: ['aperitivo'], profile: P('Leggero, amaro', 'Light, bitter'), alcohol: 2 },
  { slug: 'americano-sbagliato', name: 'Americano Sbagliato', categories: ['aperitivo'], profile: P('Leggero, amaro', 'Light, bitter'), alcohol: 2 },
  { slug: 'garibaldi', name: 'Garibaldi', categories: ['aperitivo'], profile: P('Morbido, amaro', 'Soft, bitter'), alcohol: 2 },
  { slug: 'bellini', name: 'Bellini', categories: ['aperitivo'], profile: P('Fruttato, leggero', 'Fruity, light'), alcohol: 2, featured: true },
  { slug: 'rossini', name: 'Rossini', categories: ['aperitivo'], profile: P('Fruttato, leggero', 'Fruity, light'), alcohol: 2 },
  { slug: 'mimosa', name: 'Mimosa', categories: ['aperitivo', 'classics'], profile: P('Agrumato, leggero', 'Citrusy, light'), alcohol: 2 },
  { slug: 'french-75', name: 'French 75', categories: ['classics', 'sour'], profile: P('Fresco, agrumato', 'Fresh, citrusy'), alcohol: 3 },
  { slug: 'gin-tonic', name: 'Gin Tonic · Lemon · Soda', categories: ['classics'], profile: P('Fresco, secco, dissetante', 'Fresh, dry, thirst-quenching'), alcohol: 3, featured: true },
  { slug: 'vodka-tonic', name: 'Vodka Tonic · Lemon · Soda', categories: ['classics'], profile: P('Neutro, dissetante', 'Neutral, thirst-quenching'), alcohol: 3 },
  { slug: 'moscow-mule', name: 'Moscow Mule', categories: ['classics'], profile: P('Fresco, speziato', 'Fresh, spiced'), alcohol: 3, variants: 'London · Jalisco · Kentucky' },
  { slug: 'old-fashioned', name: 'Old Fashioned', categories: ['classics'], profile: P('Intenso, strutturato', 'Intense, structured'), alcohol: 5, featured: true },
  { slug: 'manhattan', name: 'Manhattan', categories: ['classics'], profile: P('Intenso, secco', 'Intense, dry'), alcohol: 5 },
  { slug: 'long-island', name: 'Long Island Iced Tea', categories: ['classics'], profile: P('Fresco, dolce', 'Fresh, sweet'), alcohol: 5 },
  { slug: 'black-russian', name: 'Black Russian', categories: ['classics'], profile: P('Intenso, morbido', 'Intense, smooth'), alcohol: 4 },
  { slug: 'screwdriver', name: 'Screwdriver', categories: ['classics'], profile: P('Fresco, agrumato', 'Fresh, citrusy'), alcohol: 3 },
];

export const cocktails: Cocktail[] = list.map((c) => ({ ...c, image: img(c.slug) }));
export const featuredCocktails = cocktails.filter((c) => c.featured);
