export interface ModifierDef {
  target: string;
  modifier_type: 'flat' | 'percentage';
  value: number;
  label: string;
}

export interface GovernmentTypeDef {
  key: string;
  name: string;
  description: string;
  modifiers: ModifierDef[];
}

export const GOVERNMENT_TYPES: GovernmentTypeDef[] = [
  {
    key: 'democracy',
    name: 'Democracy',
    description: 'Rule by the people through elected representatives.',
    modifiers: [
      { target: 'stability', modifier_type: 'flat', value: 5, label: '+5 Stability' },
      { target: 'research', modifier_type: 'percentage', value: 10, label: '+10% Research' },
      { target: 'manpower', modifier_type: 'percentage', value: -5, label: '-5% Manpower' },
    ],
  },
  {
    key: 'autocracy',
    name: 'Autocracy',
    description: 'Absolute rule by a single leader.',
    modifiers: [
      { target: 'manpower', modifier_type: 'percentage', value: 10, label: '+10% Manpower' },
      { target: 'wealth', modifier_type: 'percentage', value: 5, label: '+5% Wealth' },
      { target: 'stability', modifier_type: 'flat', value: -5, label: '-5 Stability' },
    ],
  },
  {
    key: 'theocracy',
    name: 'Theocracy',
    description: 'Rule guided by religious doctrine.',
    modifiers: [
      { target: 'stability', modifier_type: 'flat', value: 10, label: '+10 Stability' },
      { target: 'food', modifier_type: 'percentage', value: 5, label: '+5% Food' },
      { target: 'research', modifier_type: 'percentage', value: -10, label: '-10% Research' },
    ],
  },
  {
    key: 'junta',
    name: 'Military Junta',
    description: 'Rule by a military council.',
    modifiers: [
      { target: 'manpower', modifier_type: 'percentage', value: 15, label: '+15% Manpower' },
      { target: 'materials', modifier_type: 'percentage', value: 5, label: '+5% Materials' },
      { target: 'wealth', modifier_type: 'percentage', value: -10, label: '-10% Wealth' },
    ],
  },
  {
    key: 'tribal',
    name: 'Tribal Council',
    description: 'Decentralized rule by tribal elders.',
    modifiers: [
      { target: 'food', modifier_type: 'percentage', value: 10, label: '+10% Food' },
      { target: 'stability', modifier_type: 'flat', value: 5, label: '+5 Stability' },
      { target: 'energy', modifier_type: 'percentage', value: -10, label: '-10% Energy' },
    ],
  },
  {
    key: 'corporate',
    name: 'Corporate State',
    description: 'Rule by corporate interests and trade guilds.',
    modifiers: [
      { target: 'wealth', modifier_type: 'percentage', value: 15, label: '+15% Wealth' },
      { target: 'energy', modifier_type: 'percentage', value: 5, label: '+5% Energy' },
      { target: 'stability', modifier_type: 'flat', value: -5, label: '-5 Stability' },
    ],
  },
  {
    key: 'commune',
    name: 'Commune',
    description: 'Collective rule by all citizens equally.',
    modifiers: [
      { target: 'food', modifier_type: 'percentage', value: 10, label: '+10% Food' },
      { target: 'stability', modifier_type: 'flat', value: 10, label: '+10 Stability' },
      { target: 'wealth', modifier_type: 'percentage', value: -10, label: '-10% Wealth' },
    ],
  },
];

export const TERRAIN_TYPES: Record<string, { name: string; description: string }> = {
  plains: { name: 'Plains', description: 'Flat open land, good for farming.' },
  forest: { name: 'Forest', description: 'Wooded area with natural resources.' },
  mountains: { name: 'Mountains', description: 'Rugged terrain, rich in minerals.' },
  desert: { name: 'Desert', description: 'Arid land with energy potential.' },
  coastal: { name: 'Coastal', description: 'Seaside territory with trade access.' },
  urban_ruins: { name: 'Urban Ruins', description: 'Remnants of the old world, rich in salvage.' },
  wetlands: { name: 'Wetlands', description: 'Marshy terrain with abundant food sources.' },
  tundra: { name: 'Tundra', description: 'Frozen land, harsh but defensible.' },
};
