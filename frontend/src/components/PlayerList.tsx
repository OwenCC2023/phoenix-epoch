import type { GameMembership } from '../types';

interface PlayerListProps {
  members: GameMembership[];
}

const roleBadge: Record<GameMembership['role'], string> = {
  player: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  gm: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
  observer: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
};

export default function PlayerList({ members }: PlayerListProps) {
  if (members.length === 0) {
    return <p className="text-gray-500 text-sm">No players have joined yet.</p>;
  }

  return (
    <ul className="space-y-2">
      {members.map((member) => (
        <li
          key={member.id}
          className="flex items-center justify-between bg-[#0f0f0f] border border-[#2a2a2a] rounded px-4 py-3"
        >
          <div>
            <span className="text-gray-200 text-sm font-medium">
              {member.display_name || member.username}
            </span>
            {member.display_name && (
              <span className="text-gray-500 text-xs ml-2">@{member.username}</span>
            )}
          </div>
          <span
            className={`text-xs font-medium px-2 py-0.5 rounded border ${roleBadge[member.role]}`}
          >
            {member.role}
          </span>
        </li>
      ))}
    </ul>
  );
}
