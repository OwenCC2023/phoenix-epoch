export interface TraitDef {
  key: string;
  name: string;
  description: string;
  pairIndex: number;
}

export interface TraitPair {
  traits: [TraitDef, TraitDef];
}

const trait = (key: string, name: string, description: string, pairIndex: number): TraitDef => ({
  key, name, description, pairIndex,
});

export const TRAIT_PAIRS: TraitPair[] = [
  {
    traits: [
      trait('internationalist', 'Internationalist', 'Embraces foreign cooperation. Better diplomacy and trade, but citizens expect inclusive policies.', 0),
      trait('nationalist', 'Nationalist', 'Prioritises the homeland. Stronger domestic bonuses but worse foreign relations.', 0),
    ],
  },
  {
    traits: [
      trait('spiritualist', 'Spiritualist', 'Faith guides the nation. Higher stability and population growth but slower research.', 1),
      trait('positivist', 'Positivist', 'Science and reason above all. Faster research but less social cohesion.', 1),
    ],
  },
  {
    traits: [
      trait('libertarian', 'Libertarian', 'Minimal government interference. Lower upkeep, but harder to enforce policies.', 2),
      trait('authoritarian', 'Authoritarian', 'Strong central control. Faster policy changes and higher manpower, but lower growth.', 2),
    ],
  },
  {
    traits: [
      trait('pacifist', 'Pacifist', 'Rejects military solutions. Lower military costs, but restricted arms production.', 3),
      trait('militarist', 'Militarist', 'Military strength is national strength. Better arms output but higher instability.', 3),
    ],
  },
  {
    traits: [
      trait('devious', 'Devious', 'The ends justify the means. Better espionage but worse diplomatic reputation.', 4),
      trait('honorable', 'Honorable', 'Deals are sacred. Better diplomatic reputation but vulnerable to espionage.', 4),
    ],
  },
  {
    traits: [
      trait('egalitarian', 'Egalitarian', 'All citizens are equal. Higher growth and stability, but less research output.', 5),
      trait('elitist', 'Elitist', 'Merit and talent rise to the top. Better research and specialisation, but lower growth.', 5),
    ],
  },
  {
    traits: [
      trait('collectivist', 'Collectivist', 'The community comes first. Lower government building costs, but policy constraints.', 6),
      trait('individualist', 'Individualist', 'Individual freedom drives innovation. Better commerce but higher government costs.', 6),
    ],
  },
  {
    traits: [
      trait('industrialist', 'Industrialist', 'Production above all. Urban provinces thrive, but rural areas suffer.', 7),
      trait('ecologist', 'Ecologist', 'Harmony with nature. Rural provinces produce more, but urban areas are penalised.', 7),
    ],
  },
  {
    traits: [
      trait('modern', 'Modern', 'Embrace the new world. Faster research and communications, but less stability.', 8),
      trait('traditionalist', 'Traditionalist', 'Preserve what works. Higher stability and food output, but slower to adapt.', 8),
    ],
  },
];

export const ALL_TRAITS: Record<string, TraitDef> = {};
for (const pair of TRAIT_PAIRS) {
  for (const t of pair.traits) {
    ALL_TRAITS[t.key] = t;
  }
}
